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

print("Initialization Process Begining")
#Set Reference Clock
#TBD

#Set Sampling Rate
smp_rate = 2e6
sdr.setSampleRate(SOAPY_SDR_RX, 0, smp_rate)
print("Receiver Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_RX, 0))
sdr.setSampleRate(SOAPY_SDR_TX, 0, smp_rate)
print("Transmitter Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_TX, 0), "\n")

#Set Channel Frequencies
freq = 70e6
sdr.setFrequency(SOAPY_SDR_RX, 0, freq)
print("\nReceiver Channel Frequency:", sdr.getFrequency(SOAPY_SDR_RX, 0))
sdr.setFrequency(SOAPY_SDR_TX, 0, freq)
print("Transmitter Channel Frequency:", sdr.getFrequency(SOAPY_SDR_TX, 0), "\n")

#Set Gain
gain = 40
sdr.setGain(SOAPY_SDR_RX, 0, gain)
print("\nReceiver Channel Gain:", sdr.getGain(SOAPY_SDR_RX, 0))
sdr.setGain(SOAPY_SDR_TX, 0, gain)
print("Transmitter Channel Gain:", sdr.getGain(SOAPY_SDR_TX, 0), "\n")

#Set Bandwidth
bandwidth = 20.5e6
sdr.setBandwidth(SOAPY_SDR_RX, 0, bandwidth)
sdr.setBandwidth(SOAPY_SDR_TX, 0, bandwidth)

#create a re-usable buffer for rx samples
buff = numpy.array([0]*4096, numpy.complex64)
print("\nBuffer Length:", len(buff), "\n")

#setup a stream (complex floats)
rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)

tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
time.sleep(1)

print("Activate TX and RX Stream")
sdr.activateStream(tx_stream)
sdr.activateStream(rx_stream)
print("Activation Complete")
time.sleep(1)

while(1):
	sr_read = sdr.readStream(rx_stream, [buff], len(buff))
	sr_write = sdr.writeStream(tx_stream, [buff], len(buff))
	
		
print("Closing Streams")
sdr.deactivateStream(rx_stream)
sdr.deactivateStream(tx_stream)
sdr.closeStream(rx_stream)
sdr.closeStream(tx_stream)
	
	
