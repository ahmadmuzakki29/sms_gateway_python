from db.m_aduan import m_aduan
import datetime
class Aduan():
	jml_field = 4
	format = "\n\nFormat : ADUAN<spasi>kecamatan#NIK#nama#isi_aduan"

	
	def parse(self,no_tlp,string):
		self.model = m_aduan()
		parsed = string.split("#")
		if not len(parsed)==self.jml_field:
			return "Maaf format salah"+self.format
		
		kec = parsed[0].strip() #kecamatan
		kec = self.cek_kecamatan(kec)
		cek = kec[0]
		if not cek == True:
			return cek+self.format
		kecamatan = kec[1]
		
		nik = parsed[1].strip() #NIK
		cek = self.cek_nik(nik)
		if not cek == True:
			return nik+self.format
		
		nama = parsed[2].strip() #nama
		cek = self.cek_nama(nama)
		if not cek == True:
			return nama+self.format
		
		aduan = parsed[3].strip()
		i = datetime.datetime.now()
		tgl = " %s/%s/%s" %(i.year, i.month ,i.day)
		values = {"kecamatan":kecamatan,"nik":nik,"alamat":kecamatan,"tanggal":tgl,"telepon":no_tlp,"nama":nama,"isi":aduan}
		self.model.insert(values)
		self.model.close()
		return "Aduan anda sudah kami terima, Untuk memantau tindak lanjut dari aduan anda akses www.sipatensidoarjo.com"
	
	
	
	def cek_kecamatan(self,kecamatan):
		kecamatan = self.model.cek_kecamatan(kecamatan)
		if kecamatan:
			return [True,kecamatan]
		else:
			return ["Kecamatan yang anda masukkan tidak terdaftar, cek kembali"]
	
	def cek_nik(self,nik):
		if nik.isdigit():
			return True
		else:
			return "NIK yang anda masukkan salah, cek kembali"
	
	def cek_nama(self,nama):
		if len(nama)<30:
			return True
		else:
			return "Nama anda terlalu panjang, cek kembali"
	
