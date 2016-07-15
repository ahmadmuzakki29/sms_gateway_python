from connection import Connection


class m_receivesms(Connection):
	
	def reply(self,number,text,sender="sms"):
		sql = "insert into sms_out(recipient,msg,sender) values('"+self.escape(number)+"','"+self.escape(text)+"','"+self.escape(sender)+"')"
		self.execute(sql)
		
	
	def savesms(self,number,text,recipient="sms"):
		sql = "insert into sms_in(sender,text,recipient) values('"+self.escape(number)+"','"+self.escape(text)+"','"+self.escape(recipient)+"')"
		self.execute(sql)


class m_sendsms(Connection):

	def get_unsent(self):
		sql = "select * from sms_out where sent=0 and attempt < 3 limit 1"
		
		result = self.query(sql)
		return result[0] if result else result
	
	def set_sent(self,id):
		sql = "update sms_out set sent=1, sent_time=now() where id='"+str(id)+"'"
		self.execute(sql)
	
	def add_attempt(self,id):
		sql = "update sms_out set attempt=attempt+1 where id='"+str(id)+"'"
		self.execute(sql)
