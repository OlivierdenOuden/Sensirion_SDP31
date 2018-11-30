#*******************************************************#
#														#
#		SDP3x - Sensirion Diff. Pressure sensor			#
#														#
#		Read-out script.								#
#														#
#		Olivier den Ouden								#
#		Royal Netherlands Meterological Institute		#
#		RD Seismology and Acoustics						#
#		https://www.seabirdsound.org 					#
#														#
#*******************************************************#

# Modules
import sdp31_main
import smbus
import time
import numpy as np
from datetime import datetime
import argparse
from argparse import RawTextHelpFormatter

print('')
print('SDP3x Sensirion differential Pressure sensor Read-out')
print('')
print('Olivier den Ouden')
print('Royal Netherlands Meteorological Institute, KNMI')
print('Dec. 2018')
print('')

# Parser arguments
parser = argparse.ArgumentParser(prog='SDP3x Sensirion differential Pressure sensor Read-out',
    description=('Read-out of the SDP3x Sensirion differential Pressure sensor\n'
    ), formatter_class=RawTextHelpFormatter
)

parser.add_argument(
    '-t', action='store', default=100, type=float,
    help='Time of recording, [sec].\n', metavar='-t')

parser.add_argument(
    '-fs', action='store', default=1, type=float,
    help='Sample rate, [Hz].\n', metavar='-fs')

args = parser.parse_args()

# Check if MS can comunicate with SL
if sdp31_main.init() == True:
	print "Sensor SDP3x initialized"
else:
	print "Sensor SDP3x could not be initialized"
	exit(1)

# Time knowledge
st = datetime.utcnow()
fs = args.fs
record_t = args.t
n_samples = record_t*fs

# Save data
Time_array = np.linspace(0,record_t,n_samples)
Temp = np.zeros((n_samples,2))
Pres = np.zeros((n_samples,2))
Temp[:,0] = Time_array[:]
Pres[:,0] = Time_array[:]

# Loop 
i = 0
sdp31_main.devine()
while i < n_samples:
	press_data,temp_data = sdp31_main.read()
	Temp[i,1] = temp_data
	Pres[i,1] = press_data
	i = i+1

	# Print converted data
	read_Temp = sdp31_main.temperature(temp_data)
	read_Pres = sdp31_main.pressure(press_data)
	print("Temp: %0.2f C  P: %0.2f Pa ") % (read_Temp,read_Pres)

	# Sampling rate
	time.sleep(1/fs)
