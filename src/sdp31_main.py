#*******************************************************#
#														#
#		SDP3x - Sensirion Diff. Pressure sensor			#
#														#
#		Main script with defenitions, can be called		#
#		by a read-out script.							#
#														#
#		Olivier den Ouden								#
#		Royal Netherlands Meterological Institute		#
#		RD Seismology and Acoustics						#
#		https://www.seabirdsound.org 					#
#														#
#*******************************************************#

# Modules
import smbus
import time
import numpy as np

bus = smbus.SMBus(1)

# SDP3x hex adres
SDP3x_ADDR      	= 0x21
SDP3x_STOP		= 0x3F
SDP3x_READ		= 0x00
SDP3x_CONT		= 0x36
SDP3x_AVG_FLOW		= 0x03
SDP3x_MOM_FLOW		= 0x08
SDP3x_AVG_PRES		= 0x15
SDP3x_MOM_PRES		= 0x1E

# Init, stop measurements        
def init():
	bus.write_i2c_block_data(SDP3x_ADDR,SDP3x_STOP,[0xF9])
	time.sleep(0.8)
	return True
        
def devine():
	# MS to SL
        bus.write_i2c_block_data(SDP3x_ADDR, SDP3x_CONT, [0x15])
        time.sleep(0.5)



def read():
	# Read data, 9 bytes
	data = bus.read_i2c_block_data(SDP3x_ADDR,SDP3x_READ,9)
    
    # Devide bytes into values
    # Pressure
    	press_data = data[0] << 8 | data[1] #+np.float(data[1])

    # Temperature
	temp_data = data[3] << 8 | data[4] #+np.float(data[4]))

    # Calibration check
	cali_data = data[6] << 8 | data[7] # +np.float(data[7]))

	if cali_data != 60.0:
		#return True
		print "ERROR SDP3x, CRC fail!"
		exit(1)
	return press_data,temp_data
    
# Conversion counts to Pa	
def pressure(press_data):
	if press_data >60000:
		diff_press = -(65535-press_data)/60.0
	else:
		diff_press = press_data/60.0

	return diff_press
        
# Conversion counts to degree Celcius	
def temperature(temp_data):
	return np.float(temp_data)/200.0
        
