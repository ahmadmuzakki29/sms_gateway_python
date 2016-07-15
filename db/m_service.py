from connection import Connection


class m_service(Connection):
	
	def save_service(self,number,msg):
		self.open()
		sql = "insert into sms_service(number,msg) values('"+str(number)+"','"+str(msg)+"')"
		result = self.execute(sql)
		
		sql = "update sms_out set sent=0, attempt=0 where id=2"
		result = self.execute(sql)
		self.close()
		return result
	
	def get_cekpulsa_request(self):
		self.open()
		sql = "select number from sms_service where msg='pulsa' and replied=0"
		result = self.query(sql)
		self.close()
		if not result : return result
		
		number = []
		for num in result:
			number.append(num[0])
		return number
	
	def response_pulsa(self,numbers,msg):
		self.open()
		sql = "insert into sms_out(recipient,msg,sender) values"
		for num in numbers:
			update = "update sms_service set replied=1,reply_time=now() where number='"+num+"' and msg='pulsa'"
			self.execute(update)
			sql += "('"+num+"','"+msg+"','PULSA'),"
		sql = sql[:-1]
		self.execute(sql)
		self.close()
		
