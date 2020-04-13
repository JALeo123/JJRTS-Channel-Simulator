#import SoapySDR
#from SoapySDR import * #SOAPY_SDR_ constants
import numpy #use numpy for buffers
import time
import sys
import asyncio
import socket
import struct
import threading

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
       
       
    print_info = 0
    
    buffer_struct_master = [0, hm_list, hm_list_nm, bsc_list, bsc_list_nm, ssr_list, ssr_list_nm] #First var is message type
    
    #Create a datagram socket
    localIP     = "0.0.0.0"
    localPort   = 20001
    bufferSize  = 1024
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    #Listen for incoming datagrams
    active_buffer = active[0]
    while(1):
        #Obtain buffer locations
        buffer_struct = buffer_struct_master.copy()
        hm_list = buffer_struct[1]
        hm_list_nm = buffer_struct[2]
        bsc_list = buffer_struct[3]
        bsc_list_nm = buffer_struct[4]
        ssr_list = buffer_struct[5]
        ssr_list_nm = buffer_struct[6]

        select_list = []
        name_list = []
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
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
            select_list = bsc_list
            select_listInfo = bsc_list.copy()
            name_list = bsc_list_nm
        if(type1 == 3):
            select_list = ssr_list
            select_listInfo = ssr_list.copy()
            name_list = ssr_list_nm
           
        #Split Message Bytes
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
                
            print("\n")
            
        if (active_buffer == 1):
            buffer1.append(buffer_struct)
        else:
            buffer2.append(buffer_struct)
            
        #change active buffer
        if (active_buffer == 1 and active[0] == 2):
            buffer1[0] = 1 #Set buffer to active
            active_buffer = active[0]
        elif(active_buffer == 2 and active[0] == 1):
            buffer2[0] = 1 #Set buffer to active
            active_buffer = active[0]
            
        del(select_listInfo)
        if(type1 == -1): #Exit Commands
            print("Exit Command: Ethernet Thread Exiting")
            if (active_buffer == 1):
                buffer1[0] = 1 #Set buffer to active
            elif(active_buffer == 2):
                buffer2[0] = 1 #Set buffer to active
            break
    UDPServerSocket.close()


def LimeSDR_Functions(buffer1, buffer2, active):
    print_info = 1

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
    #buff = numpy.array([0]*1024, numpy.complex64)
    #print("\nBuffer Length:", len(buff), "\n")

    #setup a stream (complex floats)
    rx_stream = sdr.setupStream(SOAPY_SDR_RX, SOAPY_SDR_CF32)
    tx_stream = sdr.setupStream(SOAPY_SDR_TX, SOAPY_SDR_CF32)
    time.sleep(1)

    print("Activate TX and RX Stream")
    sdr.activateStream(tx_stream)
    sdr.activateStream(rx_stream)
    print("Activation Complete")
    time.sleep(1)

    exit = 0
    while(1):
    
        ####ADD CODE HERE TO CHANGE CYCLE
        active[0] = 1
        active[0] = 2
        #####SWAP BETWEEN BUFFERS
        
        if(buffer1[0] == 1 or buffer2[0] == 1):
            if(buffer1[0] == 1):
                b = 1
                buffer1[0] = 0
                buffer_struct = buffer1.copy()
                buffer1.clear()
                buffer1.append(0)
            elif(buffer2[0] == 1):
                b = 2
                buffer2[0] = 0
                buffer_struct = buffer2.copy()
                buffer2.clear()
                buffer2.append(0)
            print("Buffer", str(b)," active!")

            for i in range(1,len(buffer_struct)):
                buffer = buffer_struct[i]
                type1 = buffer[0]
                hm_list = buffer[1]
                hm_list_nm = buffer[2]
                bsc_list = buffer[3]
                bsc_list_nm = buffer[4]
                ssr_list = buffer[5]
                ssr_list_nm = buffer[6]
                if(type1 == 1):
                    select_list = hm_list.copy()
                    name_list = hm_list_nm
                if(type1 == 2):
                    select_list = bsc_list.copy()
                    name_list = bsc_list_nm
                if(type1 == 3):
                    select_list = ssr_list.copy()
                    name_list = ssr_list_nm
                if(type1 == -1):
                    print("Exit Command: LimeSDR Thread Exiting")
                    exit = 1
                    break
                    
                #Enum Integration
                #Type2 Signal, Beam Steet Command
                pulse_type = ["n/a","1 usec/CW","10 usec/CW","16 usec/1MHz LFM","25 usec/CW",
                                "32 usec/1MHz LFM","64 usec/1MHz LFM","125 usec/CW","128 usec/100kHz LFM",
                                "128 usec/1MH LFM","250 usec/100kHz LFM","250 usec/1MHz LFM"]
                operability = ["Green","White","Yellow","Red"]
                if(type1 == 2):
                    select_list[3] = pulse_type[select_list[3]]
                if(type1 == 3):
                    select_list[0] = operability[select_list[0]]
                    
                if (print_info == 1): #Print Incoming Buffer
                    for i in range(len(name_list)):
                        print(name_list[i] , ": " , select_list[i])
                print("\n") 
                
                buff = numpy.array([0]*1024, numpy.complex64)
                sr_read = sdr.readStream(rx_stream, [buff], len(buff))
                
                if(type1 == 2): #LimeSDR Functions, Signal Manipulations
                    tm_delay = int(select_list[4])
                    phs_shift = int(select_list[5])
                    if(tm_delay > 0): #Time Delay
                        #Create Buffer Extender with 0 values
                        tm_delay_arry = numpy.array([0]*tm_delay, numpy.complex64)
                        buff = np.append(tm_delay_arry, buff)
                    if(phs_shift > 0): #Phase Shift
                        pass #ADD PHASE SHIFT CODE HERE!!!
                        
                sr_write = sdr.writeStream(tx_stream, [buff], len(buff))
                
        if(exit == 1):
            break

    print("Closing Streams")
    sdr.deactivateStream(rx_stream)
    sdr.deactivateStream(tx_stream)
    sdr.closeStream(rx_stream)
    sdr.closeStream(tx_stream)


if __name__ == "__main__":
    main()
	
	
