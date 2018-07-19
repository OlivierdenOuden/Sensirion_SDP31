#*****************************************************************#
#
#	SDP31 Pressure sensor convert
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
print('Convertion of raw data, SDP31 differential pressure sensor')
print('')
print('')

Temp_conv = 200
Pres_conv = 60

Tmp = read('SDP31_Tempr.mseed')
Prs = read('SDP31_pressure.mseed')
stats = Prs[0].stats

n_samples = len(Tmp)

for i in range(0,n_samples):
	#Calc Temperature
	Tmp[i] = Tmp[i]/Temp_conv 

	#Calc temp compensated Pressure
	Prs[i] = Prs[i]/Pres_conv

st = Stream([Trace(data=Prs, header=stats)])
st.write("Conv_SDP31_pressure.mseed", format='MSEED', encoding=11, reclen=512)

ts = Stream([Trace(data=Tmp, header=stats)])
ts.write("Conv_SDP31_tmp.mseed", format='MSEED', encoding=11, reclen=512)