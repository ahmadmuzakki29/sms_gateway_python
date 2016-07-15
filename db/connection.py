#!/usr/bin/env python

import MySQLdb as mdb

from warnings import filterwarnings


class Connection:
	host = 'localhost'
	user = ''
	password = ''
	database = ''
	
	con = None
	def __init__(self):
		filterwarnings('ignore', category = mdb.Warning)
		self.open()
	
	def get_cursor(self):
		return self.cursor
	
	def get_val(self,values):
		col = ""
		val = ""
		for key,vals in values.iteritems():
			col += "`"+key+"`,"
			val += "'"+vals+"',"
		return col,val
	
	def get_val_update(self,values):
		
		val = ""
		for key,vals in values.iteritems():
			val += "`"+key+"`='"+vals+"',"
		return val
	
	def open(self):
		self.con = mdb.connect(self.host, self.user,self.password,self.database)
		self.cursor = self.con.cursor()
	
	def close(self):
		if self.con.open:
			self.cursor.close()
			self.con.close()
	
	def commit(self):
		self.con.commit()
	
	def execute(self,sql): #execute non query

		result = self.cursor.execute(sql)
		self.commit()
		return result
	
	def query(self,sql): #execute query
		cur = self.cursor

		result = cur.execute(sql)
		
		if result:
			return cur.fetchall()
		else:
			return False
		
	def escape(self,word):
		word = str(word)
		return word
		#return 	self.con.escape_string(word);
