import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import time
import sys
import asyncio
import math
import matplotlib.pyplot as plt
from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CS16, SOAPY_SDR_TX
#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)

print("Initialization Process Begining")
#Set Sampling Rate
print()
smp_rate = 2e6
sdr.setSampleRate(SOAPY_SDR_RX, 0, smp_rate)
print("Receiver Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_RX, 0))
sdr.setSampleRate(SOAPY_SDR_TX, 0, smp_rate)
print("Transmitter Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_TX, 0))
print()

#Set Channel Frequencies
freq = 20e6
sdr.setFrequency(SOAPY_SDR_RX, 0, 20e6)
print("\nReceiver Channel Frequency:", sdr.getFrequency(SOAPY_SDR_RX, 0))
sdr.setFrequency(SOAPY_SDR_TX, 0, freq)
print("Transmitter Channel Frequency:", sdr.getFrequency(SOAPY_SDR_TX, 0), "\n")

#Set Gain
gain = 40
sdr.setGain(SOAPY_SDR_RX, 0, 40)
print("\nReceiver Channel Gain:", sdr.getGain(SOAPY_SDR_RX, 0))
sdr.setGain(SOAPY_SDR_TX, 0, gain )
print("Transmitter Channel Gain:", sdr.getGain(SOAPY_SDR_TX, 0), "\n")

#Set Bandwidth
bandwidthrx = 2e6
bandwidthtx = 2e6
sdr.setBandwidth(SOAPY_SDR_RX, 0, bandwidthrx)
sdr.setBandwidth(SOAPY_SDR_TX, 0, bandwidthtx)

#create a re-usable buffer for rx samples
buff_len = 2048
buff1 = numpy.array([0]*buff_len, numpy.complex64)
buff2 = numpy.array([0]*buff_len, numpy.complex64)
print("\nBuffer Length:", len(buff1), "\n")

#setup a stream (complex floats)
rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
time.sleep(1)

sdr.setDCOffsetMode(SOAPY_SDR_RX, 0, False)
sdr.setDCOffsetMode(SOAPY_SDR_TX, 0, False)

print("Activate TX and RX Stream")
sdr.activateStream(tx_stream)
sdr.activateStream(rx_stream)#, numElems = len(buff1))
print("Activation Complete")
time.sleep(1)

#Create class to initialize DSP object and such
class delay(object): 
	#initialize object
	def __init__(self, delay_samps = 0, buff_size = buff_len, phase_index = 0):
		# Time delay using circular buffer
		self.delay = delay_samps
		self.ptr = 0
		self.buffsize = buff_size
		self.cirbuff = numpy.array([0]*buff_size, numpy.complex64)

	#Set user defines delay
	def set_delay(self, new_delay):
		self.delay = new_delay

	def process_sample(self, buff):
		self.cirbuff[self.ptr] = buff
		buffd = self.cirbuff[(self.ptr - self.delay) % self.buffsize]
		self.ptr = (self.ptr + 1) % self.buffsize

		return buffd

	def process_frame(self, buff):
		Nframe = len(buff)
		buffd = numpy.array([0]*Nframe, numpy.complex64)
		for k in range(Nframe):
			buffd[k] = self.process_sample(buff[k])

		return buffd

#Create class to initialize DSP object and such
class phase_shift(object): 

	#initialize object
	def __init__(self, buff_size = buff_len, phase_index = 0):

		#Phase shift using complex multiplication/LUTs
		self.ptr = 0
		self.buffsize = buff_size
		self.phase = phase_index
		phase_incr = numpy.arange(0, 361, 1)
		self.coslut = numpy.cos(pi*phase_incr/180)
		self.sinlut = numpy.sin(pi*phase_incr/180)
		
	#Set user defines phase in degrees
	def set_phase(self, new_phase):
		self.phase = new_phase

	def process_frame(self, buff):
		shift = self.coslut[self.phase] +1j*self.sinlut[self.phase]
		buffp = shift*buff
		return buffp

#DSP Stuff
#Time delay is in terms of samples of 2MHz rate 
#Phase is any value form 0 to 360 (degrees)
pi = math.pi
pingpong = 0
rqs_delay = 0
rqs_phase = 0
cbuf1 = delay(0, buff_len)
phase1 = phase_shift(buff_len, 0)
keep_streaming = True
#infinite loop - break by changing keep_streaming = False
while(keep_streaming):

	#rqs_delay and rqs_phase variables are set by ethernet command
	cbuf1.set_delay(rqs_delay)
	phase1.set_phase(rqs_phase)
	
	if pingpong == 0:
		sr_read = sdr.readStream(rx_stream, [buff1], len(buff1))
		sr_write = sdr.writeStream(tx_stream, [buff2], len(buff2))

		#Process signal - processing delay = 9ms worst case
		#Processing time measured using time.time() and the result is printed, which may skew the results
		# start_time = time.time()
		buff1 = cbuf1.process_frame(buff1)
		buff1 = phase1.process_frame(buff1)
		#end_time = time.time()
		#print("Processing Time = ", end_time - start_time)
		pingpong = 1
		
	else: 
		sr_read = sdr.readStream(rx_stream, [buff2], len(buff2))
		sr_write = sdr.writeStream(tx_stream, [buff1], len(buff1))

		#Process signal - processing delay = 9ms worst case
		#Processing time measured using time.time() and the result is printed, which may skew the results
		# start_time = time.time()
		buff2 = cbuf1.process_frame(buff2)                                                                                         
		buff2 = phase1.process_frame(buff2)
		#end_time = time.time()
		#print("Processing Time = ", end_time - start_time)
		pingpong = 0

print("Closing Streams")
sdr.deactivateStream(rx_stream)
sdr.deactivateStream(tx_stream)
sdr.closeStream(rx_stream)
sdr.closeStream(tx_stream)
	