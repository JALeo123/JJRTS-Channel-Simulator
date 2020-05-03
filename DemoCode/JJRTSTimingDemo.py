import SoapySDR
from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import time
import sys
import asyncio
import socket
import struct
import threading
import math
import matplotlib.pyplot as plt
from SoapySDR import SOAPY_SDR_RX, SOAPY_SDR_CS16, SOAPY_SDR_TX

def main():
    #Memory Buffers, first element is active state, second is message type
    buffer1 = [0]
    buffer2 = [0]
    active = [1] #Can only be 1 or 2, in a list due to pointers
    t1 = threading.Thread(target=Ethernet_Recieve, args=(buffer1,buffer2,active,))
    t2 = threading.Thread(target=LimeSDR_Functions, args=(buffer1,buffer2,active,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
                    

def Ethernet_Recieve(buffer1, buffer2, active):
       
    print_info = 0
    
    #Create a datagram socket
    localIP     = "169.254.102.212"
    localPort   = 20001
    bufferSize  = 1024
    timeout_seconds = 0.005
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))
    UDPServerSocket.settimeout(timeout_seconds) #Timeout set in seconds
    
    #Listen for incoming datagrams
    active_buffer = active[0]
    while(1):
        try:
            #Messages to be Recieved based on L3Harris Data
            #Header Message (1)
            Message_ID = 4          #Byte Length = 4, Type INT
            PDP_ID = 4              #Byte Length = 4, Type INT
            Message_Length = 4      #Byte Length = 4, Type INT
            Message_Time = 8        #Byte Length = 8, Type BCD
            Num_Records = 4         #Byte Length = 4, Type INT
            Record_Length = 4       #Byte Length = 4, Type INT
            Recieve_ID = 4          #Byte Length = 4, Type INT
            hm_list = [Message_ID,PDP_ID,Message_Length,
                        Message_Time,Num_Records,Record_Length,
                        Recieve_ID] #4=int, 8=8byteFloat, 5=4byteFloat
            hm_list_nm = ["Message_ID","PDP_ID","Message_Length",
                            "Message_Time","Num_Records","Record_Length",
                            "Recieve_ID"]

            #Beam Steer Command (2)
            Action_ID = 4           #Byte Length = 4, Type INT
            Start_Action_Tm = 4     #Byte Length = 4, Type INT
            Stop_Action_Tm = 4      #Byte Length = 4, Type INT
            Pulse_Type = 4          #Byte Length = 4, Type ENUM
            Time_Delay = 4          #Byte Length = 4, Type INT
            Phase_Adj = 4           #Byte Length = 4, Type INT
            Ampl_Adj = 5            #Byte Length = 4, Type FLOAT
            bsc_list = [Action_ID,Start_Action_Tm,Stop_Action_Tm,
                        Pulse_Type,Time_Delay,Phase_Adj,
                        Ampl_Adj]
            bsc_list_nm = ["Action_ID","Start_Action_Tm","Stop_Action_Tm",
                            "Pulse_Type","Time_Delay","Phase_Adj",
                            "Ampl_Adj"]

            #Summary Status Report (3)
            Operability = 4         #Byte Length = 4, Type ENUM
            Status_1 = 4            #Byte Length = 4, Type INT
            Status_2 = 4            #Byte Length = 4, Type INT
            Status_3 = 4            #Byte Length = 4, Type INT
            Status_4 = 4            #Byte Length = 4, Type INT
            ssr_list = [Operability,Status_1,Status_2,
                        Status_3,Status_4]
            ssr_list_nm = ["Operability","Status_1","Status_2",
                            "Status_3","Status_4"]
           
            #Obtain buffer locations
            buffer_struct = [0, hm_list.copy(), hm_list_nm.copy(), bsc_list.copy(), bsc_list_nm.copy(), ssr_list.copy(), ssr_list_nm.copy()] #First var is message type
            #print(buffer_struct)
            
            """buffer_struct[1][0] = 100
            print(buffer_struct)
            buffer_struct = [0, hm_list.copy(), hm_list_nm.copy(), bsc_list.copy(), bsc_list_nm.copy(), ssr_list.copy(), ssr_list_nm.copy()] #First var is message type
            print(buffer_struct)"""
            hm_list = buffer_struct[1]
            hm_list_nm = buffer_struct[2]
            bsc_list = buffer_struct[3]
            bsc_list_nm = buffer_struct[4]
            ssr_list = buffer_struct[5]
            ssr_list_nm = buffer_struct[6]

            select_list = []
            name_list = []
            UDPServerSocket.settimeout(timeout_seconds) #Timeout set in seconds
            #print("A")
            bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
            #print("b")
            message = bytesAddressPair[0]
            #print(message)
            address = bytesAddressPair[1]

            rawclientMsg = "Raw Message: {}".format(message)
            clientIP  = "Incoming IP Address: {}".format(address)
            
            type1, = struct.unpack('i', message[0:4])

            buffer_struct[0] = type1

            if(type1 == 1 or type1 == -1):
                select_list = hm_list
                select_listInfo = hm_list.copy()
                name_list = hm_list_nm
            if(type1 == 2):
                select_list = buffer_struct[3]
                select_listInfo = buffer_struct[3].copy()
                name_list = buffer_struct[4]       
            if(type1 == 3):
                select_list = ssr_list
                select_listInfo = ssr_list.copy()
                name_list = ssr_list_nm

               
            #Split Message Bytes
            #PROBLEM HERE
            r = 4
            for i in range(len(select_listInfo)):
                tmp = select_listInfo[i]
                if(select_list[i] == 4):
                    select_list[i], = struct.unpack('i', message[r:select_listInfo[i]+r])
                if(select_list[i] == 5):
                    select_list[i], = struct.unpack('f', message[r:select_listInfo[i]+r])
                if(select_list[i] == 8):
                    select_list[i], = struct.unpack('d', message[r:select_listInfo[i]+r])
                r += tmp
            
            #Print Interpreted Revieved Message
            if (print_info == 1):
                print(rawclientMsg)
                print(clientIP)
                for i in range(len(name_list)):
                    print(name_list[i] , ": " , select_list[i])
                    
                #print("\n")
            #print(buffer_struct)    
            if (active_buffer == 1):
                buffer1.append(buffer_struct)
            else:
                buffer2.append(buffer_struct)
            #print("-")   
            #change active buffer
             #print("except")
             
            if (active_buffer == 1 and active[0] == 2):
               #print("SW")
                buffer1[0] = 1 #Set buffer to active
                #buffer2.clear()
                #buffer2.append(0)
                active_buffer = 2
            elif(active_buffer == 2 and active[0] == 1):
               #print("SW")
                #buffer1.clear()
                #buffer1.append(0)
                buffer2[0] = 1 #Set buffer to active
                active_buffer = 1
                
            del(select_listInfo)
            if(type1 == -1): #Exit Commands
                print("Exit Command: Ethernet Thread Exiting")
                if (active_buffer == 1):
                    buffer1[0] = 1 #Set buffer to active
                    #buffer2.clear()
                    #buffer2.append(0)
                elif(active_buffer == 2):
                    #buffer1.clear()
                    #buffer1.append(0)
                    buffer2[0] = 1 #Set buffer to active
                break
        except:
            #print("except")
            if (active_buffer == 1 and active[0] == 2):
                #rint("SW")
                buffer1[0] = 1 #Set buffer to active
                #buffer2.clear()
                #buffer2.append(0)
                active_buffer = 2
            elif(active_buffer == 2 and active[0] == 1):
                #rint("SW")
                #buffer1.clear()
                #buffer1.append(0)
                buffer2[0] = 1 #Set buffer to active
                active_buffer = 1
    UDPServerSocket.close()


def LimeSDR_Functions(buffer1, buffer2, active):
    print_info = 0

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
    smp_rate = 2.5e6
    sdr.setSampleRate(SOAPY_SDR_RX, 0, smp_rate)
    print("Receiver Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_RX, 0))
    sdr.setSampleRate(SOAPY_SDR_TX, 0, smp_rate)
    print("Transmitter Sampling Rate:", sdr.getSampleRate(SOAPY_SDR_TX, 0), "\n")

    #Set Channel Frequencies
    freq = 20e6
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
    bandwidth = 2e6
    sdr.setBandwidth(SOAPY_SDR_RX, 0, bandwidth)
    sdr.setBandwidth(SOAPY_SDR_TX, 0, bandwidth)

    #Clock Sources - Try to use External reference clock for something useful
    print("************* Clock Stuff ****************")
    #sdr.setClockSource(REF_CLK_IN)
    print(sdr.getMasterClockRate())
    print(sdr.listClockSources())
    print(sdr.getClockSource())
    print(sdr.getTimeSource())
    
    #print(sdr.getMasterClockRate())
    #--------------------------------------------------------

    #create a re-usable buffer for rx samples
    buff_len = 1024
    #buff = numpy.array([0]*1024, numpy.complex64)
    #print("\nBuffer Length:", len(buff), "\n")
    prevhwTime = 0
    #Set buffer 1 to active to get the program started
    #setup a stream (complex floats)
    rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
    time.sleep(1)
    #sdr.setDCOffsetMode(SOAPY_SDR_RX, 0, False)
    #sdr.setDCOffsetMode(SOAPY_SDR_TX, 0, False)

    print("Activate TX and RX Stream")
    sdr.activateStream(tx_stream)
    sdr.activateStream(rx_stream)
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
            
    type1=0
    hm_list=[]
    hm_list_nm=[]
    bsc_list=[]
    bsc_list_nm=[]
    ssr_list=[]
    ssr_list_nm=[]
    select_list=[]
    name_list=[]
    
    pi = math.pi
    pingpong = 0
    rqs_delay = []
    rqs_phase = []
    rqs_start = []
    rqs_end = []
    cbuf1 = []
    phase1 = []
    
    exit = 0
    while(1):
        
        if(buffer1[0] == 1 or buffer2[0] == 1):
           #print("HI")
            #print("hi ******************************************************")
            if(buffer1[0] == 1):
                b = 1
                #buffer1[0] = 0
                buffer_struct = buffer1.copy()
                buffer1.clear()
                buffer1.append(0)
            elif(buffer2[0] == 1):
                b = 2
                #buffer2[0] = 0
                buffer_struct = buffer2.copy()
                buffer2.clear()
                buffer2.append(0)
           # print("Buffer",str(b),"active!")
            #print(buffer_struct)
            #rint(len(buffer_struct))
            #fill the lists with all ethernet commands recieved
            #int("\n")
            for i in range(0,len(buffer_struct)-1):
                cbuf1.append(delay(0, buff_len))
                phase1.append(phase_shift(buff_len, 0))
                
                buffer = buffer_struct[i+1]
                #print(buffer)
                type1= buffer[0]
                #print(buffer[0])
                hm_list.append(buffer[1])
                #print(buffer[1])
                hm_list_nm.append(buffer[2])
                #print(buffer[2])
                bsc_list.append(buffer[3])
                #print(bsc_list)
                bsc_list_nm.append(buffer[4])
                ssr_list.append(buffer[5])
                ssr_list_nm.append(buffer[6])
                if(type1== 1):
                    select_list.append(hm_list[i].copy())
                    name_list.append(hm_list_nm[i])
                if(type1 == 2):
                    select_list.append(bsc_list[i])
                    
                    name_list.append(bsc_list_nm[i])
                    #print(select_list, '*********************')
                if(type1 == 3):
                    select_list.append(ssr_list[i].copy())
                    name_list.append(ssr_list_nm[i])
                if(type1 == -1):
                    print("Exit Command: LimeSDR Thread Exiting")
                    exit = 1
                    break
                sel = select_list[i]    
                #Enum Integration
                #Type2 Signal, Beam Steet Command
                pulse_type = ["n/a","1 usec/CW","10 usec/CW","16 usec/1MHz LFM","25 usec/CW",
                                "32 usec/1MHz LFM","64 usec/1MHz LFM","125 usec/CW","128 usec/100kHz LFM",
                                "128 usec/1MH LFM","250 usec/100kHz LFM","250 usec/1MHz LFM"]
                operability = ["Green","White","Yellow","Red"]
                
                #if(type1 == 2):
                    #sel[3] = pulse_type[pt]
                    #print(sel[3])
                #if(type1 == 3):
                    #sel[0] = operability[]
                    
                if (print_info == 1): #Print Incoming Buffer
                    for j in range(len(name_list)):
                        print(name_list[i][j] , ": " , select_list[i][j])
                #print("\n") 
                #print("type1: ",type1)
                
                if(type1 != 2): #LimeSDR Functions, Signal Manipulations
                    rqs_delay.append(0)
                    rqs_phase.append(0)
                    rqs_start.append(0)
                    rqs_end.append(0)
                else:
                    rqs_delay.append(int(select_list[i][4]))
                    rqs_phase.append(int(select_list[i][5]))
                    rqs_start.append(int(select_list[i][1])//816000)
                    rqs_end.append(int(select_list[i][2])//816000)
                
                #print(rqs_delay,rqs_phase,rqs_start,rqs_end)
                #print(rqs_delay,rqs_phase,rqs_start,rqs_end)
                    
                #print(rqs_delay,rqs_phase,rqs_start,rqs_end)
                cbuf1[i].set_delay(rqs_delay[i])
                phase1[i].set_phase(rqs_phase[i])
            
                #Signal DSP Function Processing
                if(pingpong == 0):
                    sr_read = sdr.readStream(rx_stream, [buff1], len(buff1))
                    msTime = sr_read.timeNs//816000
                    print(msTime)
                    sr_write = sdr.writeStream(tx_stream, [buff2], len(buff2))
                    pingpong = 1
                elif(pingpong == 1):
                    sr_read = sdr.readStream(rx_stream, [buff2], len(buff2))
                    msTime = sr_read.timeNs//816000
                    print(msTime)
                    sr_write = sdr.writeStream(tx_stream, [buff1], len(buff1))
                    
                    pingpong = 0
                #End DSP Function Processing
                
                
                # Buffer Switch Logic - using timeNs -------------
                
                hwTime = sr_read.timeNs
                if(hwTime==0 < prevhwTime):
                    print("BufferSwitch")
                    if active[0] == 1: 
                        active[0]=2
                    elif active[0] == 2:
                        active[0]=1
                prevhwTime = hwTime
                
                #--------------------------------------------------
            #rint(rqs_start,rqs_end,rqs_phase,rqs_delay)

        else: #Deafult ADC/DAC pass through
            #Signal DSP Function Processing
            #buff_len = 2048
            buff1 = numpy.array([0]*buff_len, numpy.complex64)
            buff2 = numpy.array([0]*buff_len, numpy.complex64)
            if(pingpong == 0):
                sr_read = sdr.readStream(rx_stream, [buff1], len(buff1))
                msTime = sr_read.timeNs//816000
                print(msTime)
                if(rqs_start != []):
                    if(msTime >= rqs_start[0] and msTime <= rqs_end[0]):
                        if(len(rqs_start) > 1):
                            if(msTime >= rqs_start[1]):
                                #rint("New Command Running")
                                cbuf1.pop(0)
                                phase1.pop(0)
                                rqs_start.pop(0)
                                rqs_end.pop(0)
                                rqs_phase.pop(0)
                                rqs_delay.pop(0)
                        print("Phase:",rqs_phase[0],"deg. Delay:",rqs_delay[0],"samples")
                        #buff1 = cbuf1[0].process_frame(buff1)
                        #buff1 = phase1[0].process_frame(buff1)
                            #are there more commands to process
                        #print(len(rqs_start))
                        
                    elif(msTime >= rqs_end[0]):
                        if(len(rqs_start) > 1):
                            cbuf1.pop(0)
                            phase1.pop(0)
                            rqs_start.pop(0)
                            rqs_end.pop(0)
                            rqs_delay.pop(0)
                            rqs_phase.pop(0)
                sr_write = sdr.writeStream(tx_stream, [buff2], len(buff2))
                pingpong = 1
            elif(pingpong == 1):
                sr_read = sdr.readStream(rx_stream, [buff2], len(buff2))
                msTime = sr_read.timeNs//816000
                print(msTime)
                if(rqs_start != [] and rqs_start[0] != 0):
                    if(msTime >= rqs_start[0] and msTime <= rqs_end[0]):
                        if(len(rqs_start) > 1):
                            if(msTime >= rqs_start[1]):
                               #print("New Command Running")
                                cbuf1.pop(0)
                                phase1.pop(0)
                               #print(rqs_start)
                                rqs_start.pop(0)
                               #print(rqs_start)
                                rqs_end.pop(0)
                                rqs_delay.pop(0)
                                rqs_phase.pop(0)
                        print("Phase:",rqs_phase[0]," deg. Delay:",rqs_delay[0],"samples")
                        #buff1 = cbuf1[0].process_frame(buff2)
                        #buff1 = phase1[0].process_frame(buff2)
                        #are there more commands to process
                        #print(len(rqs_start))
                       
                    elif(msTime >= rqs_end[0]):
                        if(len(rqs_start) > 1):
                            if(msTime >= rqs_start[1]):
                                cbuf1.pop(0)
                                phase1.pop(0)
                                rqs_start.pop(0)
                                rqs_end.pop(0)
                                rqs_delay.pop(0)
                                rqs_phase.pop(0)
                    sr_write = sdr.writeStream(tx_stream, [buff1], len(buff1))
                pingpong = 0
            #End DSP Function Processing
                
            # Buffer Switch Logic - using timeNs -------------
            hwTime = sr_read.timeNs
            #print(hwTime//816000)
            if(hwTime < prevhwTime):
                print("BufferSwitch")
                rqs_delay.clear()
                rqs_phase.clear()
                rqs_start.clear()
                rqs_end.clear()
                cbuf1.clear()
                phase1.clear()
                if active[0] == 1: 
                    active[0]=2
                elif active[0] == 2:
                    active[0]=1
            prevhwTime = hwTime

            #--------------------------------------------------
            
        if(exit == 1):
            break

    print("Closing Streams")
    sdr.deactivateStream(rx_stream)
    sdr.deactivateStream(tx_stream)
    sdr.closeStream(rx_stream)
    sdr.closeStream(tx_stream)


if __name__ == "__main__":
    main()
	
	
