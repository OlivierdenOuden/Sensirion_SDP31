#*******************************************************#
#							#
#	SDP3x - Sensirion Diff. Pressure sensor		#
#							#
#	Simple Read-out script.				#
#							#
#	Olivier den Ouden				#
#	Royal Netherlands Meterological Institute	#
#	RD Seismology and Acoustics			#
#	https://www.seabirdsound.org 			#
#							#
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

# Stop all measuremnets
bus.write_i2c_block_data(SDP3x_ADDR,SDP3x_STOP,[0xF9])
time.sleep(0.8)

# MS to SL - data
bus.write_i2c_block_data(SDP3x_ADDR, SDP3x_CONT, [0x03])

# Read data
while True:
	time.sleep(1)
	data = bus.read_i2c_block_data(SDP3x_ADDR,SDP3x_READ,9)

	# Convert counts to Mass Flow[l/min]/Differentail Pressure[pa]
	press_value = data[0]+np.float(data[1])/255
	if press_value >= 0 and press_value<128:
		diff_press = press_value*60/256
	elif press_value>128 and press_value<=256:
		diff_press=-(256-press_value)*60/256

	# Convert counts to Temperature[C]
	temp_value = (data[3]+np.float(data[4]))/10.0

	# Print values
	print("Temp: %0.2f C  P: %0.2f Pa ") % (temp_value,diff_press)


