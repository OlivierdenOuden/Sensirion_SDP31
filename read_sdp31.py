#*****************************************************************#
#
#	SDP31 Pressure sensor read I2C port
#
#	Olivier den Ouden
#	Royal Netherlands Meteorological Institute
#	RDSA
#	Jul. 2018
#
#****************************************************************#

#modules
import sdp31
import time
import argparse
from argparse import RawTextHelpFormatter
from datetime import datetime, timedelta
from obspy import UTCDateTime, read, Trace, Stream
import numpy as np


print('')
print('Read SDP31 differential pressure sensor - I2C port')
print('')
print('')


parser = argparse.ArgumentParser(prog='Import pressure data of the SDP31.',
    description=('Main script to import differential pressure data of the SDP31\n'
        'to a Raspberry Pi. Data formt is MSEED. \n'
    ), formatter_class=RawTextHelpFormatter
)


parser.add_argument(
    '--OSR',action='store', default=1000, type=float,
    help=('Oversampling rate (only in case of avg measurments) 1000Hz is maximum, in case of 1000Hz use serie measurments (default: %(default)s Hz)\n'),
    metavar='1000')

parser.add_argument(
    '--Measurment',action='store', default=0, type=float,
    help=('Measurment type (default: %(default)s)\n'),
    metavar='1')

parser.add_argument(
    '--Record_time',action='store', default=3600, type=float,
    help=('Time of recording (default: %(default)s sec)\n'),
    metavar='3600')

#Sensor definition

sensor = sdp31.SDP31() 
check_in = sensor.init()
if not check_in:
	print("Sensor could not be initialized")
	exit(1)

check_re,c,d = sensor.read()
if not check_re:
	print("Sensor read failed!")
	exit(1)

# Read data 
StTime = (datetime.utcnow())
dT = timedelta(seconds=args.Record_time)
EdTime = StTime + dT

#Sampling data
if (args.Measurment == 1) or (args.Measurment == 3):
	Updatetime = 0.001
elif (args.Measurment == 0) or (args.Measurment == 2):
	Updatetime = 1/args.OSR
elif (args.Measurment == 4) or (args.Measurment == 5):
	Updatetime = 0.045


#Data save array
sampl_time = Updatetime
n_samples = dT/sampl_time
D1_save = np.zeros((n_samples,),dtype=int32)
D2_save = np.zeros((n_samples,),dtype=int32)

#Different schemes for different measurment methods
i = 0
if (args.Measurment == 0) or (args.Measurment == 2):
	check,D1,D2 = sensor.read(Measurment=args.Measurment)
	while datetime.utcnow() < EdTime:
		D1_save[i] = D1
		D2_save[i] = D2
		i = i+1
		time.sleep(sampl_time)

if (args.Measurment == 1) or (args.Measurment == 3):
	check,D1,D2 = sensor.read(Measurment=args.Measurment)
	while datetime.utcnow() < EdTime:
		D1_save[i] = D1
		D2_save[i] = D2
		i = i+1

if (args.Measurment == 4) or (args.Measurment == 5):

	while datetime.utcnow() < EdTime:
		check,D1,D2 = sensor.read(Measurment=args.Measurment)
		D1_save[i] = D1
		D2_save[i] = D2
		i = i+1

sensor.stop()


#MSEED write

#Channel type
if args.OSR < 20:
	ch = 'LDF'
elif args.OSR > 20 and args.OSR < 80:
	ch = 'BDF'
elif args.OSR > 80 and args.OSR < 250:
	ch = 'HDF'
elif args.OSR > 250:
	ch = 'EDF'


# Fill header attributes
stats = {'network': 'PI', 'station': 'SD',
         'channel': ch, 'npts': n_samples, 'sampling_rate': args.OSR,
         'mseed': {'dataquality': 'D'}}

stats['starttime'] = StTime
st = Stream([Trace(data=D1_save, header=stats)])
sr = Stream([Trace(data=D2_save, header=stats)])
st.write("SDP31_pressure.mseed", format='MSEED', encoding=11, reclen=512)
sr.write("SDP31_Tempr.mseed", format='MSEED', encoding=11, reclen=512)





