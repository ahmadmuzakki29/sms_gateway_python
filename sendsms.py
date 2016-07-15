#!/usr/bin/env python
import serial
import sys
import getopt


def main(argv):
	number = ''
	message = ''
	

	try:
		opts,args = getopt.getopt(argv,"hn:m:")
	except getopt.GetoptError:
		print 'usage: sendsms.py -n <number> -m <message>'
		sys.exit(2)

	if len(argv) < 2:
		print 'usage: sendsms.py -n <number> -m <message>'
		sys.exit()

	for opt, arg in opts:
		if opt == '-h':
			print 'sendsms.py -n <number> -m <message>'
			sys.exit()
		elif opt in ("-n"):
			number = arg
		elif opt in ("-m"):
			message = arg

	
	phone = serial.Serial("/dev/ttyUSB0",  115200, timeout=5)
	try:
		
		phone.write('AT+CMGS="' + number.encode() + '"\r')
		phone.write(message.encode() + "\x1a")
	finally:
		phone.close()

