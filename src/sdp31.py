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
from obspy import Stream,Trace
import shutil

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
    '-t', action='store', default=6100000, type=float,
    help='Time of recording, [sec].\n', metavar='-t')

parser.add_argument(
    '-fs', action='store', default=1, type=float,
    help='Sample rate, [Hz].\n', metavar='-fs')

parser.add_argument(
    '-miniSeed', action='store', default=64, type=float,
    help='Saving the data after x [sec], always power of 2!.\n', metavar='-miniSeedFreq')

args = parser.parse_args()

# Check if MS can comunicate with SL
if sdp31_main.init() == True:
	print "Sensor SDP3x initialized"
else:
	print "Sensor SDP3x could not be initialized"
	exit(1)

# Time knowledge
fs = args.fs
record_t = args.t
n_samples = record_t*fs

delta_time = args.miniSeed
delta_sampl= np.int(delta_time*fs)

# Save data
Time_array = np.linspace(0,record_t,n_samples)
Temp = np.zeros((delta_sampl,))
Pres = np.zeros((delta_sampl,))

# Header Channel type
if fs < 20:
	ch = 'LDF'
elif fs > 20 and fs < 80:
	ch = 'BDF'
elif fs > 80 and fs < 250:
	ch = 'HDF'
elif fs > 250:
	ch = 'EDF'

stats = {'network': 'MBA_PI', 'station': '01_SDP3x',
         'channel': ch, 'npts': delta_sampl, 'sampling_rate': fs,
         'mseed': {'dataquality': 'D'}}

# Comunicate with sensor what kind of measurement
sdp31_main.devine()

# Loop 
i = 0
j = 0
while i < n_samples:
	if j == delta_sampl:
		stats['starttime'] = st
#		sTemp = Stream([Trace(data=Temp[:,], header=stats)])
		sPres = Stream([Trace(data=Pres[:,], header=stats)])
#		sTemp.write("SDP3x_Temp_"+str(st_str)+".mseed", format='MSEED',reclen=512)
		sPres.write("SDP3x_Pres_"+str(st_str)+".mseed", format='MSEED',reclen=512)
#		shutil.move("/SDP3x_Pres_"+str(st_str)+".mseed","/home/pi/PIM_data/mseed/SDP3x_Pres_"+str(st_str)+".mseed")

		Temp = np.zeros((delta_sampl,))
		Pres = np.zeros((delta_sampl,))

		j = 0

	if j==0:
		st = datetime.utcnow()
		st_str = st.strftime('%Y_%m_%d_T%H_%M_%S.%f')
	

	press_data,temp_data = sdp31_main.read()

	read_Temp = sdp31_main.temperature(temp_data)
	read_Pres = sdp31_main.pressure(press_data)

	Temp[j,] = read_Temp
	Pres[j,] = read_Pres
	
	j = j+1
	i = i+1

	# Print converted data
	print "Temp:",read_Temp,"C","P:",read_Pres,"Pa"
#	print(press_data)
	# Sampling rate
	time.sleep(1/fs)
