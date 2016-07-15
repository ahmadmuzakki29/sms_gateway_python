from db.m_service import m_service
# service adalah kelas untuk handle request yang tidak bisa langsung dibalas
# contoh: cek pulsa
class Service:
	service_number = ["555"]
	def is_service_number(self,number):
		for num in self.service_number:
			if num==number:
				return True
		return False
	
	def save_service(self,number,msg):
		self.model = m_service()
		self.model.save_service(number,msg)
		
	def parse(self,number,msg):
		if number=="555" :
			self.cek_pulsa(msg)
			
	def cek_pulsa(self,msg):
		self.model = m_service()
		numbers = self.model.get_cekpulsa_request()
		if not numbers : return
		
		if msg.split(" ")[:1][0]!="Saldo" :
			return
			
		msg = msg.split(" ")[-3:]
		pulsa = msg[0]
		masaaktif = msg[2]
		masaaktif = masaaktif[-2:]+"-"+masaaktif[4:6]+"-"+masaaktif[:4]
		
		msg = "Sisa pulsa: "+pulsa+" Masa aktif sampai: "+masaaktif
		
		self.model.response_pulsa(numbers,msg)
		
		
