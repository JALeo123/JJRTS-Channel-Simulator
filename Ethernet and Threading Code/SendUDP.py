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
Action_ID = 1234       #Byte Length = 4, Type INT
Start_Action_Tm = 2345  #Byte Length = 4, Type INT
Stop_Action_Tm = 3456   #Byte Length = 4, Type INT
Pulse_Type = 2          #Byte Length = 4, Type ENUM
Time_Delay = 5678       #Byte Length = 4, Type INT
Phase_Adj = 6789        #Byte Length = 4, Type INT
Ampl_Adj = 7890         #Byte Length = 4, Type FLOAT
bsc_list = [int(Action_ID),int(Start_Action_Tm),int(Stop_Action_Tm),
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

msgType = -1
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

serverAddressPort = ("10.0.0.182", 20001)

#Create a UDP socket at client side
UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Send to server using created UDP socket
UDPClientSocket.sendto(message, serverAddressPort)

print("Address Port: ", str(serverAddressPort))
print("Raw Message: ", message)
UDPClientSocket.close()

