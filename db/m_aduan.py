from connection import Connection

class m_aduan(Connection):
	
	def cek_kecamatan(self,kecamatan):
		sql = "select kecamatan from _listkecamatan where kecamatan = '"+kecamatan+"'"
		
		result = self.query(sql)
		if result:
			return result[0][0]
		else:
			return False
	
	def insert(self,values):
		values.update({"petugas":"SMS"})
		col,val = self.get_val(values)
		
		col = col[:-1]
		val = val[:-1]
		sql = "insert into pengaduan("+col+") values("+val+")"
		
		result = self.execute(sql)
		return result

