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
       
    #Memory Buffers, first element is active state, second is message type
    buffer1 = [0, 0, hm_list, hm_list_nm, bsc_list, bsc_list_nm, ssr_list, ssr_list_nm]
    buffer2 = [0, 0, hm_list, hm_list_nm, bsc_list, bsc_list_nm, ssr_list, ssr_list_nm]
    t1 = threading.Thread(target=Ethernet_Recieve, args=(buffer1,buffer2,))
    t2 = threading.Thread(target=LimeSDR_Functions, args=(buffer1,buffer2,))
    
    t1.start()
    t2.start()
    
    t1.join()
    t2.join()
                    

def Ethernet_Recieve(buffer1, buffer2):
    print_info = 0
    
    #Create a datagram socket
    localIP     = "0.0.0.0"
    localPort   = 20001
    bufferSize  = 1024
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    #Bind to address and ip
    UDPServerSocket.bind((localIP, localPort))

    #Listen for incoming datagrams
    active_buffer = 1
    while(1):
        #Obtain buffer locations
        if(active_buffer == 1):
            hm_list = buffer1[2]
            hm_list_nm = buffer1[3]
            bsc_list = buffer1[4]
            bsc_list_nm = buffer1[5]
            ssr_list = buffer1[6]
            ssr_list_nm = buffer1[7]
        elif(active_buffer == 2):
            hm_list = buffer2[2]
            hm_list_nm = buffer2[3]
            bsc_list = buffer2[4]
            bsc_list_nm = buffer2[5]
            ssr_list = buffer2[6]
            ssr_list_nm = buffer2[7]
    
        select_list = []
        name_list = []
        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]

        rawclientMsg = "Raw Message: {}".format(message)
        clientIP  = "Incoming IP Address: {}".format(address)
        
        type1, = struct.unpack('i', message[0:4])

        if(active_buffer == 1):
            buffer1[1] = type1
        elif(active_buffer == 2):
            buffer2[1] = type1

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
            
        #change active buffer
        if (active_buffer == 1):
            buffer1[0] = 1 #Set buffer to active
            active_buffer = 2
        else:
            buffer2[0] = 1 #Set buffer to active
            active_buffer = 1
            
        del(select_listInfo)
        if(type1 == -1):
            print("Exit Command: Ethernet Thread Exiting")
            break
    UDPServerSocket.close()


def LimeSDR_Functions(buffer1, buffer2):
    print_info = 1
    '''
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
    '''
    while(1):
        if(buffer1[0] == 1 or buffer2[0] == 1):
            if(buffer1[0] == 1):
                b = 1
                buffer1[0] = 0
                buffer = buffer1.copy()
            elif(buffer2[0] == 1):
                b = 2
                buffer2[0] = 0
                buffer = buffer2.copy()
            print("Buffer", str(b)," active!")

            type1 = buffer[1]
            hm_list = buffer[2]
            hm_list_nm = buffer[3]
            bsc_list = buffer[4]
            bsc_list_nm = buffer[5]
            ssr_list = buffer[6]
            ssr_list_nm = buffer[7]
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
                break
                
            if (print_info == 1):
                for i in range(len(name_list)):
                    print(name_list[i] , ": " , select_list[i])
            print("\n") 
            #sr_read = sdr.readStream(rx_stream, [buff], len(buff))
            #sr_write = sdr.writeStream(tx_stream, [buff], len(buff))
    '''
    print("Closing Streams")
    sdr.deactivateStream(rx_stream)
    sdr.deactivateStream(tx_stream)
    sdr.closeStream(rx_stream)
    sdr.closeStream(tx_stream)
    '''

if __name__ == "__main__":
    main()
	
	
