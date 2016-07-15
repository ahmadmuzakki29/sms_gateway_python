from connection import Connection

class m_ak(Connection):
	
	def cek_no_ak(self,kecamatan,no_ak):
		sql = "select no_pendaftaran from tbpencarikerja where no_pendaftaran='"+no_ak+"' and kecamatan='"+kecamatan+"'"
		
		result = self.query(sql)
		if result:
			return result[0][0]
		else:
			return False
	
	def cek_kecamatan(self,kecamatan):
		sql = "select kecamatan from _listkecamatan where kecamatan = '"+kecamatan+"'"
		
		result = self.query(sql)
		if result:
			return result[0][0]
		else:
			return False
	
	def update(self,kecamatan,no_pendaftaran,values):
		val = self.get_val_update(values)
		
		val = val[:-1]
		sql = "update tbpencarikerja set "+val+" where no_pendaftaran='"+no_pendaftaran+"' and kecamatan='"+kecamatan+"'"
		
		result = self.execute(sql)
		return result

