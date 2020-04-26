import socket
import struct

serverAddressPort = ("169.254.102.212", 20001)
#Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

def sendEthernet(msgType, msgList, list_bytes):
    message = struct.pack('i', msgType)
    select_list = msgList
    select_list_bytes = list_bytes
    for i in range(len(select_list_bytes)):
        if(select_list_bytes[i] == 4):
            message = message + struct.pack('i', select_list[i])
        elif(select_list_bytes[i] == 5):
            message = message + struct.pack('f', select_list[i])
        elif(select_list_bytes[i] == 8):
            message = message + struct.pack('d', select_list[i])

    #Send to server using created UDP socket
    UDPClientSocket.sendto(message, serverAddressPort)

    print("Address Port: ", str(serverAddressPort))
    print("Raw Message: ", message)


#Test Messages
#Header Message (1)
Message_ID = 1234       #Byte Length = 4, Type INT
PDP_ID = 2345           #Byte Length = 4, Type INT
Message_Length = 3456   #Byte Length = 4, Type INT
Message_Time = 12.345678 #Byte Length = 8, Type BCD
Num_Records = 4567      #Byte Length = 4, Type INT
Record_Length = 5678    #Byte Length = 4, Type INT
Recieve_ID = 6789       #Byte Length = 4, Type INT
hm_list = [int(Message_ID),int(PDP_ID),int(Message_Length),
            float(Message_Time),int(Num_Records),int(Record_Length),
            int(Recieve_ID)]
hm_list_bytes = [4,4,4,8,4,4,4] #4=int, 8=8byteFloat, 5=4byteFloat

#Beam Steer Command (2)

#Test Beam Steer Commands
Action_ID = [1,2,3,4,5,6,7,8,9,10]       #Byte Length = 4, Type INT
Start_Action_Tm = [7344000,9792000,14688000,17136000,20400000,22848000,26112000,34272000,40800000,44064000]   #Byte Length = 4, Type INT
Stop_Action_Tm = [42432000,43248000,44064000,44880000,45696000,46512000,47328000,48144000,48960000,49776000]   #Byte Length = 4, Type INT
Pulse_Type = [1,2,3,4,5,6,7,8,9,10]          #Byte Length = 4, Type ENUM
Time_Delay = [1,10,30,80,129,300,500,850,910,1000]   #Byte Length = 4, Type INT
Phase_Adj = [0,35,67,90,129,180,225,280,300,345]      #Byte Length = 4, Type INT
Ampl_Adj = [0,0,0,0,0,0,0,0,0,0]         #Byte Length = 4, Type FLO]AT
bsc_list = []

for i in range(10):
    print(i)
    bsc_list.append([int(Action_ID[i]),int(Start_Action_Tm[i]),int(Stop_Action_Tm[i]),int(Pulse_Type[i]),int(Time_Delay[i]),int(Phase_Adj[i]),float(Ampl_Adj[i])])
    print(bsc_list[i])
bsc_list_bytes = [4,4,4,4,4,4,5]

sendEthernet(2,bsc_list[1],bsc_list_bytes)


#Summary Status Report (3)
Operability = 1         #Byte Length = 4, Type ENUM
Status_1 = 2345         #Byte Length = 4, Type INT
Status_2 = 3456         #Byte Length = 4, Type INT
Status_3 = 4567         #Byte Length = 4, Type INT
Status_4 = 5678         #Byte Length = 4, Type INT


ssr_list = [int(Operability),int(Status_1),int(Status_2),
            int(Status_3),int(Status_4)]
ssr_list_bytes = [4,4,4,4,4]

UDPClientSocket.close()

