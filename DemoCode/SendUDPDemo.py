import socket
import struct
import time
"""
serverAddressPort = ("169.254.102.212", 20001)
#Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
"""
def sendEthernet(msgType, msgList, list_bytes):
    serverAddressPort = ("169.254.102.212", 20001)
    print(msgList)
    #Create a UDP socket at client side
    UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    message = struct.pack('i', msgType)
    select_list = []
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
    UDPClientSocket.close()
    


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
Action_ID = [11,22,333,44,55,66,77,88,999,1010]       #Byte Length = 4, Type INT

Start_Action_Tm = [7344000,9792000,11424000,14688000,21216000,25296000,30192000,36720000,44064000,48960000]   #Byte Length = 4, Type INT
Stop_Action_Tm = [20400000,20400000,21216000,21216000,27744000,35088000,39268000,41616000,49776000,49776000]   #Byte Length = 4, Type INT
Pulse_Type = [1,2,3,3,5,6,7,7,9,10]          #Byte Length = 4, Type ENUM
Time_Delay = [1,10,30,80,129,300,500,850,910,1000]   #Byte Length = 4, Type INT
Phase_Adj = [0,35,67,90,129,180,225,280,300,345]      #Byte Length = 4, Type INT
Ampl_Adj = [0,0,0,0,0,0,0,0,0,0]         #Byte Length = 4, Type FLO]AT
bsc_list = []
bsc_list_bytes = [4,4,4,4,4,4,5]
for i in range(10):
    #print(i)
    bsc_list.append([int(Action_ID[i]),int(Start_Action_Tm[i]),int(Stop_Action_Tm[i]),int(Pulse_Type[i]),int(Time_Delay[i]),int(Phase_Adj[i]),float(Ampl_Adj[i])])
#print(bsc_list)    

#sendEthernet(2,bsc_list[2],bsc_list_bytes)
#time.sleep(0.015)
#sendEthernet(2,bsc_list[4],bsc_list_bytes)


# Timing Test Routine
# Run Five Commands and Verify Command Timing
"""
    1. Phase Shift 35 deg, Time Delay 10 samples, Start Time 12, End Time 25
    2. Phase Shift 67 deg, Time Delay 30 samples, Start Time 14, End Time 26
    3. Phase Shift 90 deg, Time Delay 80 Samples, Start Time 18, End Time 26
    4. Phase Shift 180 deg, Time Delay 300 Samples, Start Time 31, End Time 43
    5. Phase Shift 280 deg, Time Delay 850 Samples, Start Time 45, End Time 51
"""
while(1):
    time.sleep(0.05)
    
    sendEthernet(2,bsc_list[1],bsc_list_bytes)
    sendEthernet(2,bsc_list[2],bsc_list_bytes)
    sendEthernet(2,bsc_list[3],bsc_list_bytes)
    sendEthernet(2,bsc_list[5],bsc_list_bytes)
    sendEthernet(2,bsc_list[7],bsc_list_bytes)
    

# Ethernet recieve test routine
# Show that all command types can be recieved.
"""

"""    


#Summary Status Report (3)
Operability = 1         #Byte Length = 4, Type ENUM
Status_1 = 2345         #Byte Length = 4, Type INT
Status_2 = 3456         #Byte Length = 4, Type INT
Status_3 = 4567         #Byte Length = 4, Type INT
Status_4 = 5678         #Byte Length = 4, Type INT


ssr_list = [int(Operability),int(Status_1),int(Status_2),
            int(Status_3),int(Status_4)]
ssr_list_bytes = [4,4,4,4,4]



