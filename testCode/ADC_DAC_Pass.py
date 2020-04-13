import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import time
import sys
import asyncio

#enumerate devices
results = SoapySDR.Device.enumerate()
for result in results: print(result)

#create device instance
#args can be user defined or from the enumeration result
args = dict(driver="lime")
sdr = SoapySDR.Device(args)

#apply settings
smp_rate = 2e6
sdr.setSampleRate(SOAPY_SDR_RX, 0, smp_rate)
sdr.setSampleRate(SOAPY_SDR_TX, 0, smp_rate)
freq = 20.5e6
sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
sdr.setFrequency(SOAPY_SDR_TX, 0, 800e6)
gain = 60
sdr.setGain(SOAPY_SDR_RX, 0, gain)
sdr.setGain(SOAPY_SDR_TX, 0, gain)

print(sdr.listClockSources())
print(sdr.getClockSource())
#sdr.setMasterClockRate(60e6)
print(sdr.getMasterClockRate())

#create a re-usable buffer for rx samples
buff = numpy.array([0]*1024, numpy.complex64)

#setup a stream (complex floats)
rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
time.sleep(1)

print("Activate TX and RX Stream")
sdr.activateStream(tx_stream)

'''
rx_flags = SOAPY_SDR_HAS_TIME
tx_time_0 = int(sdr.getHardwareTime() + 0.1e9) #100ms
num_rx_samps = 10000
rate = 1e6
receive_time = int(tx_time_0 - (num_rx_samps/rate) * 1e9 / 2)
sdr.activateStream(rx_stream, rx_flags, receive_time, num_rx_samps)
'''
sdr.activateStream(rx_stream)

print("Activation Complete")
time.sleep(1)

timeout = int(5e5)
while(1):
	sr_read = sdr.readStream(rx_stream, [buff], len(buff))#, timeoutUs=timeout)
	#time.sleep(0.5)
	sr_write = sdr.writeStream(tx_stream, [buff], len(buff))
	#time.sleep(0.5)
	#buff = numpy.array([0]*4024, numpy.complex64)
	#print(buff)
	#sys.exit()
	
	
print("Closing Streams")
sdr.deactivateStream(rx_stream)
sdr.deactivateStream(tx_stream)
sdr.closeStream(rx_stream)
sdr.closeStream(tx_stream)
	
	
