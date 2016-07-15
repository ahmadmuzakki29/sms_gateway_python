#!/usr/bin/env python
# -*- coding: utf-8 -*-

#untuk restart modem "minicom sms"
import serial,sys
import getopt
import StringIO
import time, datetime
import threading,traceback

from aduan import Aduan
from ak1 import Ak1
from db.model import *
from service import Service

from pdu import decodeSmsPdu, encodeSmsSubmitPdu

class Vividict(dict):
	def __missing__(self, key):
		value = self[key] = type(self)()
		return value

class MyThread(threading.Thread):
	def __init__(self,target,args):
		self.main_ev = args[0]
		super(MyThread, self).__init__(target=target,args=args)
   
   
	def run(self):
		try:
			super(MyThread,self).run()
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()			
			traceback.print_exception(exc_type,exc_value,exc_traceback)
			sys.stderr.write(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')+"\n\n")
			
			self.main_ev.clear()
			

class SmsCenter:
	
	
	notif_code = "+CMT: "
	_smsRef = 0
	msgs = Vividict()
	threads = Vividict()
	events = Vividict()
	m_sendsms = m_sendsms()
	m_receivesms = m_receivesms()
	sms = []
	in_msg = []
	sent_code = ""
	aduan = Aduan()
	ak1 = Ak1()
	service = Service()
	def __init__(self):
		port = "/dev/ttyUSB0"
		speed = 115200
		
		try:
			main_ev = threading.Event()
			main_ev.set()

			self.phone = False

			self.phone = serial.Serial(port,  speed, timeout=.1)
			self.phone.write('AT\r')
			self.phone.write('AT+CMGF=0\r')
			self.phone.write('AT+CNMI=2,2,2,1,1\r')
			
			
			MyThread(target=self.cek_notif,args=(main_ev,)).start() # cek notifikasi
			MyThread(target=self.sendsms,args=(main_ev,)).start() # kirim sms
			MyThread(target=self.receivesms,args=(main_ev,)).start() # terima sms
			MyThread(target=self.readsms,args=(main_ev,)).start() # proses sms diterima"""
			
			while main_ev.is_set():
				time.sleep(2)
				pass
		except serial.serialutil.SerialException as se:
			with open("log","a") as f:
				f.write("\nmodem tidak terkoneksi")
			print "modem tidak terkoneksi"
			if self.phone:
				self.phone.close()
		except KeyboardInterrupt:
			
			main_ev.clear()
			self.m_sendsms.close()
			if self.phone:
				self.phone.close()
			print "\nExiting..."
		except Exception as e:
			
			print e
			main_ev.clear()
			self.m_sendsms.close()
			if self.phone:
				self.phone.close()
			print "\nExiting..."
		
	def cek_notif(self,ev):
		while ev.is_set():
			line = self.phone.readline()

			if line.startswith("+CMGS:"): #SENT MESSAGE
				self.sent_code = line
			elif line.startswith("+CMT: "): #INCOMING MESSAGE
				msg = self.phone.readline().strip()
				self.in_msg.append(msg)
				
			time.sleep(3)
	
	def receivesms(self,main_ev):
		
		while main_ev.is_set():
			
			if len(self.in_msg)>0:
				
				msg = self.in_msg.pop(0)
				pdu = decodeSmsPdu(msg)
				if 'udh' in pdu:
					udhs = pdu['udh']
					udh = next(iter(udhs))
					
					number = pdu['number']
					data = udh.data
					id,count,index = data
					self.msgs[number][id][index] = pdu['text']
					
					if len(self.msgs[number][id])==count:
						msg = ""
						for i in self.msgs[number][id]:
							msg += self.msgs[number][id][i]
						self.sms.append({'number':number,'msg':msg})
					else:
						if number in self.events and id in self.events[number]: #kalo sudah ada lanjutkan
							e = self.events[number][id]
							e.set()
							e.clear()
							t = threading.Thread(target=self.del_corrupted_msg,args=(number,id))
							t.start()
						else: # membuat thread
							e = threading.Event()
							t = threading.Thread(target=self.del_corrupted_msg,args=(number,id))
							self.events[number][id] = e
							t.start()
				else:
					number = pdu['number']
					text = pdu['text']
					self.sms.append({'number':number,'msg':text})
			time.sleep(1)

	def sendsms(self,main_ev):
		while main_ev.is_set():
			self.m_sendsms.open()
			data = self.m_sendsms.get_unsent()
			if data:
				id,number,msg = data[0],data[2],data[3]
				pdus = encodeSmsSubmitPdu(number, msg, reference=self._smsRef)
				result = "ERROR"
				pdu_count = 0
				for pdu in pdus:
					self.phone.write('AT+CMGS='+str(pdu.tpduLength)+'\r')
					self.phone.write(str(pdu)+'\x1a')
					pdu_count +=1
					for i in range(60): #timeout 10s
						time.sleep(1)
						if self.sent_code:
							result = self.sent_code
							self.sent_code = ""
							break
					else:
						result=="ERROR"
						if pdu_count==1:
							break
				if not result == "ERROR":
					reference = int(result[7:])
					self._smsRef = reference + 1
					if self._smsRef > 200:
						self._smsRef = 0
					self.m_sendsms.set_sent(id)
				else:
					self.m_sendsms.add_attempt(id)
				
			self.m_sendsms.close()
			time.sleep(2)

	def del_corrupted_msg(self,number,id):
		count = len(self.msgs[number][id])
		e = self.events[number][id]
		e.wait(30)
		#e.wait(3)
		
		if count==len(self.msgs[number][id]):
			del self.msgs[number][id]
			del self.events[number][id]
	
	def readsms(self,main_ev):
		while main_ev.is_set():
			
			if len(self.sms)>0:
				self.m_receivesms.open()
				sms = self.sms.pop(0)
				number = str(sms['number'].encode('utf8'))
				text = str(sms['msg'].encode('utf8'))
				#print number,text
				
				recipient = "SMS"
				self.m_receivesms.savesms(number,text,recipient)
				
				if self.service.is_service_number(number):
					self.service.parse(number,text)
				elif text.lower().startswith('aduan '):
					text = text[len('aduan '):]
					reply = self.aduan.parse(number,text)
					self.m_receivesms.reply(number,reply,"ADUAN")
					recipient = "ADUAN"
				elif text.lower().startswith('updatebekerja '):
					text = text[len('updatebekerja '):]
					reply = self.ak1.parse(number,text)
					self.m_receivesms.reply(number,reply,"AK1")
					recipient = "AK1"
				elif text.lower().startswith('cek '):
					text = text[len('cek '):]
					self.service.save_service(number,text)
					
				
				self.m_receivesms.close()
			
			time.sleep(1)
		
	
if __name__ =='__main__':
	SmsCenter()
	
