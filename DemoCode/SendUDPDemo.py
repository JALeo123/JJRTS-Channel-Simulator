import socket
import struct

#Messages to be sent based on L3Harris Data
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

#Test 1 - Single Beam Steer Command
Action_ID = [1,2,3,4,5,6,7,8,9,10]       #Byte Length = 4, Type INT
Start_Action_Tm1 = [7140000,11220000,18360000,23460000,27540000,30600000,33660000,35700000,43860000,48960000]   #Byte Length = 4, Type INT
Stop_Action_Tm1 = [39780000,40800000,41820000,42840000,43860000,44880000,45900000,46920000,47940000,48960000]   #Byte Length = 4, Type INT
Pulse_Type1 = [1,2,3,4,5,6,7,8,9,10]          #Byte Length = 4, Type ENUM
Time_Delay1 = [1,   #Byte Length = 4, Type INT
Phase_Adj1 = [0,35,67,90,129,180,225,280,300,345]      #Byte Length = 4, Type INT
Ampl_Adj1 = 7890         #Byte Length = 4, Type FLO]AT
bsc_list1 = [int(Action_ID),int(Start_Action_Tm),int(Stop_Action_Tm),
            int(Pulse_Type),int(Time_Delay),int(Phase_Adj),
            float(Ampl_Adj)]
bsc_list_bytes = [4,4,4,4,4,4,5]

#Test 2 - Two Beam Steer Commands in one time interval
Action_ID = 1234       #Byte Length = 4, Type INT
Start_Action_Tm2 = 29580000  #Byte Length = 4, Type INT
Stop_Action_Tm2 = 3456   #Byte Length = 4, Type INT
Pulse_Type2 = 2          #Byte Length = 4, Type ENUM
Time_Delay2 = 5678       #Byte Length = 4, Type INT
Phase_Adj2 = 90        #Byte Length = 4, Type INT
Ampl_Adj2 = 7890         #Byte Length = 4, Type FLOAT
bsc_list2 = [int(Action_ID),int(Start_Action_Tm),int(Stop_Action_Tm),
            int(Pulse_Type),int(Time_Delay),int(Phase_Adj),
            float(Ampl_Adj)]
bsc_list_bytes = [4,4,4,4,4,4,5]

Action_ID3 = 1234       #Byte Length = 4, Type INT
Start_Action_Tm3 = 29580000  #Byte Length = 4, Type INT
Stop_Action_Tm3 = 3456   #Byte Length = 4, Type INT
Pulse_Type3 = 2          #Byte Length = 4, Type ENUM
Time_Delay3 = 5678       #Byte Length = 4, Type INT
Phase_Adj3 = 90        #Byte Length = 4, Type INT
Ampl_Adj3 = 7890         #Byte Length = 4, Type FLOAT
bsc_list3 = [int(Action_ID),int(Start_Action_Tm),int(Stop_Action_Tm),
            int(Pulse_Type),int(Time_Delay),int(Phase_Adj),
            float(Ampl_Adj)]
bsc_list_bytes = [4,4,4,4,4,4,5]

#Summary Status Report (3)
Operability = 1         #Byte Length = 4, Type ENUM
Status_1 = 2345         #Byte Length = 4, Type INT
Status_2 = 3456         #Byte Length = 4, Type INT
Status_3 = 4567         #Byte Length = 4, Type INT
Status_4 = 5678         #Byte Length = 4, Type INT
ssr_list = [int(Operability),int(Status_1),int(Status_2),
            int(Status_3),int(Status_4)]
ssr_list_bytes = [4,4,4,4,4]

msgType = 2
message = struct.pack('i', msgType)
select_list = []
select_list_bytes = []
if(msgType == 1 or msgType == -1):
    select_list = hm_list
    select_list_bytes = hm_list_bytes
if(msgType == 2):
    select_list = bsc_list
    select_list_bytes = bsc_list_bytes
if(msgType == 3):
    select_list = ssr_list
    select_list_bytes = ssr_list_bytes
for i in range(len(select_list_bytes)):
    if(select_list_bytes[i] == 4):
        message = message + struct.pack('i', select_list[i])
    elif(select_list_bytes[i] == 5):
        message = message + struct.pack('f', select_list[i])
    elif(select_list_bytes[i] == 8):
        message = message + struct.pack('d', select_list[i])

serverAddressPort = ("169.254.102.212", 20001)

#Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
UDPClientSocket.sendto(message, serverAddressPort)

print("Address Port: ", str(serverAddressPort))
print("Raw Message: ", message)
UDPClientSocket.close()

