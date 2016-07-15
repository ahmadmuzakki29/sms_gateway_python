from db.m_ak import m_ak
import datetime
class Ak1():
	jml_field = 5
	format = "\n\nFormat :  UPDATEBEKERJA<spasi>kecamatan#nomorAK1#perusahaan#posisi#gaji"
	
	
	def parse(self,no_tlp,string):
		self.model = m_ak()
		parsed = string.split("#")
		if not len(parsed)==self.jml_field:
			return "Maaf format salah"+self.format
		
		
		kec = parsed[0].strip() #kecamatan
		kec = self.cek_kecamatan(kec)
		cek = kec[0]
		if not cek == True:
			return cek+self.format
		kecamatan = kec[1]
		
		no_ak = parsed[1].strip() #no_ak
		no_ak = self.cek_no_ak(kecamatan,no_ak)
		cek = no_ak[0]
		if not cek == True:
			return cek+self.format
		no_ak = no_ak[1]
		
		perusahaan = parsed[2].strip()
		posisi = parsed[3].strip()
		gaji = parsed[4].strip()
		
		i = datetime.datetime.now()
		tgl = " %s/%s/%s" %(i.year, i.month ,i.day)
		values = {"telepon":no_tlp,"nama_perusahaan":perusahaan,"mulai_bekerja":tgl,"posisi_diterima":posisi,"gaji":gaji}
		self.model.update(kecamatan,no_ak,values)
		self.model.close()
		return "Update status pekerjaan anda sudah kami terima, untuk info lowongan kerja kunjungi www.sipatensidoarjo.com"
		
	
	def cek_kecamatan(self,kecamatan):
		kecamatan = self.model.cek_kecamatan(kecamatan)
		if kecamatan:
			return [True,kecamatan]
		else:
			return ["Kecamatan yang anda masukkan tidak terdaftar, cek kembali"]
	
	def cek_no_ak(self,kecamatan,no_ak):
		no_ak = self.model.cek_no_ak(kecamatan,no_ak)
		if no_ak:
			return [True,no_ak]
		else:
			return ["Nomor AK1 yang anda masukkan tidak terdaftar di kecamatan "+kecamatan+", cek kembali"]
	
	
	
