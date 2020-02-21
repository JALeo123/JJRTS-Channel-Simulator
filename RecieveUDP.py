import socket
import struct

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
            
localIP     = "0.0.0.0"
localPort   = 20001
bufferSize  = 1024

#Create a datagram socket
UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Bind to address and ip
UDPServerSocket.bind((localIP, localPort))

#Listen for incoming datagrams
ct = 0
while(ct < 3):
    select_list = []
    name_list = []
    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
    message = bytesAddressPair[0]
    address = bytesAddressPair[1]

    rawclientMsg = "Raw Message: {}".format(message)
    clientIP  = "Incoming IP Address: {}".format(address)
    print(rawclientMsg)
    print(clientIP)
    
    type1, = struct.unpack('i', message[0:4])
    print(type1)
    if(type1 == 1):
        select_list = hm_list.copy()
        name_list = hm_list_nm
    if(type1 == 2):
        select_list = bsc_list.copy()
        name_list = bsc_list_nm
    if(type1 == 3):
        select_list = ssr_list.copy()
        name_list = ssr_list_nm
       
    #Split Message Bytes
    r = 4
    for i in range(len(select_list)):
        tmp = select_list[i]
        if(select_list[i] == 4):
            select_list[i], = struct.unpack('i', message[r:select_list[i]+r])
        if(select_list[i] == 5):
            select_list[i], = struct.unpack('f', message[r:select_list[i]+r])
        if(select_list[i] == 8):
            select_list[i], = struct.unpack('d', message[r:select_list[i]+r])
        r += tmp
    
        
    #Print Interpreted Revieved Message
    for i in range(len(name_list)):
        print(name_list[i] , ": " , select_list[i])
        
    print("\n")
    del(select_list)
    ct += 1
UDPServerSocket.close()






