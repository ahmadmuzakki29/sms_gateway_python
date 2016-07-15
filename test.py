#!/usr/bin/env python
import time,datetime
import threading
import traceback
import sys
class MyThread(threading.Thread):
	
	def run(self):
		try:
			super(MyThread,self).run()
		except Exception as e:
			print e
			exc_type, exc_value, exc_traceback = sys.exc_info()
			traceback.print_tb(exc_traceback)
			print datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
			
	
def target():
	i = 0
	while True:
		print i
		i+=1 
		time.sleep(0.5)
		if i==10:
			raise Exception("eksepsi")

if __name__ =='__main__':
	
	main_ev = threading.Event()
	
	MyThread(target=target).start()
	
		