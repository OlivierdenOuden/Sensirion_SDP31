#*****************************************************************#
#
#	SDP31 Pressure sensor read I2C port
#
#	Based on; https://github.com/DataDrake/SDP3x-Arduino/blob/master/SDP3x.cpp
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Jul. 2018
#
#****************************************************************#

#modules
import smbus
from time import sleep

SDP31_MODEL = 0

class SDP31(object):
	#hex/byte commants 
	_SDP31_ADDR			= 0x21
	_SDP31_RESET		= 0x0006
	_SDP31_STOP			= 0x3FF9

	_SDP31_D1_cont_avg	= 0x3603
	_SDP31_D1_cont_ser	= 0x3608
	_SDP31_D2_cont_avg	= 0x3615
	_SDP31_D2_cont_ser	= 0x361E

	_SDP31_D1_trig		= 0x3624
	_SDP31_D2_trig		= 0x362F
	
	def _init_(self, model=SDP31_MODEL, bus=1):
		self._model = model

		self._D1 = 0
		self._D2 = 0

	def init(self):
		self._bus.write_byte(self._SDP31_ADDR, self._SDP31_RESET)

		sleep(0.2)

		return True

	def read(self, measurment=1):
		if self._bus is None:
			print('No bus!')

			return False

		if measurment == 0:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D1_cont_avg)

			sleep(0.2)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)
		elif measurment == 1:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D1_cont_ser)

			sleep(0.2)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)
		elif measurment == 2:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D2_cont_avg)

			sleep(0.2)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)
		elif measurment == 3:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D2_cont_ser)

			sleep(0.02)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)
		
		elif measurment == 4:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D1_trig)

			sleep(0.045)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)

		elif measurment == 5:
			rawdata_ = self._bus.read_word_data(self._SDP31_ADDR, self._SDP31_D2_trig)

			sleep(0.045)

			Diff_press 	= rawdata_[0:16]
			crc 		= rawdata_[16:24]
			Tempr      	= rawdata_[24:40]

			Diff_press 	= ((Diff_press & 0xFF) << 8) | (Diff_press >> 8) #swap MSB - LSB
			Tempr	 	= ((Tempr & 0xFF) << 8) | (Tempr >> 8)
		crc = (crc & 0xF000) >> 12
		if crc != self._crc4(self._C):
			print('PROM read error, CrC failed!')
			return False


		return True, Diff_press, Tempr

	def stop(self):
		self._bus.write_byte(self._SDP31_ADDR, self._SDP31_STOP)

		return True

  
	def _crc4(self, n_prom):

		n_rem = 0

		n_prom[0] = ((n_prom[0]) & 0x0FFF)
		n_prom.append(0)

		for i in tange(16)
			if i%2 == 2:
				n_rem ^= ((n_prom[i>>1]) & 0x0FFF)
			else:
				n_rem ^= (n_prom[i>>1] >> 8)

`			for n_bit in range(8,0.-1):
				if n_rem & 0X8000:
					n_rem = (n_rem << 1) ^ 0x3000
				else:
					n_rem = (n_rem << 1)

		n_rem = ((n+rem >> 12) & 0x000F)

		self.n_prom = n_prom
		self.n_rem = n_rem

		return n_rem ^ 0x00

class SDP31(SDP31):
	def _init_(self,bus=1)
		SDP31._init_(self,SDP31_MODEL,bus)
	

