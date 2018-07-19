# Sensirion_SDP31

How to read-out the Sensirion SDP31 digital differetial pressure sensor by use of the I2C port on a Raspberry PI model 3B+. More info on the [SDP31 sensor](https://nl.mouser.com/datasheet/2/682/Sensirion_Differential_Pressure_Sensors_SDP3x_Digi-1093440.pdf) and the [I2C port](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial).

## Raspberry PI - I2C port 

First the hardware needs to be enabled before the software, attached python scripts, can be used. This is done by following the steps of the link above.
The I2C port is not enabled by default, this needs to be done;
1. Run, in terminal, ```sudo raspi-config```.
2. Select point 9, ```Advanced options```.
3. Select A7, ```I2C```, and select ```yes```.
4. Exit this window and reboot the PI.

After reboot, check if the I2C port is enabled by using;

```
ls /dev/*i2c*
```

if I2C port is open the PI will respond with;

```
/dev/i2c-1
```

where ```1``` indicates which I2C bus is used.

Now the I2C port is enabled but to have interaction between the PI and the sensor some utilities are needed. Use the following command line in a terminal;

```
sudo apt-get install -y i2c-tools
```

The ```i2cdetect``` command probes all the addresses on a I2C port bus, and report whether any devices are present. Outcome of this command will look like;

```
pi@raspberrypi:~/$ i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
60: 60 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
70: -- -- -- -- -- -- -- --
```

Here the I2C adress of the sensor is 0x60. More information, or source, can be found [here](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial).

## I2C - Python 

To read out the sensors with python, some python modules are needed. Run the command lines below;

```
sudo apt-get update
sudo apt-get install python-smbus
sudo apt-get install python-obspy
```

## Python scripts

The ```read_sdp31.py``` script is the main script. This script uses the defenitions of ```sdp31.py```, which defines all different methods of reading the data. To use the main script some parameters are needed;

```
OSR - Sampling rate, only needed when using methods 0 or 2. Methods 1 and 3 have a sampling rate of 1000hz, while 4 and 5 sample at 22hz
Measurement - The sensor got 6 different measurement methods. 0 and 2 are continuous measurements where the average value over the sampling time is taken as datapoint. 1 and 2 are continuous measurements with automatic updata, no averaging. 4 and 5 are triggered measurements.
Recording time - Determining the length of recording.
```

The main script gives back 2 MSEED files, one with temperature counts and one with pressure counts. To convert those count in real values the ```conv_sdp31.py``` script is used.

## Author

**Olivier den Ouden** - *KNMI* - [HFSP SeabirdSound](https://seabirdsound.org)
