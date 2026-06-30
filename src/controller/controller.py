"""
due to having to run in terminal have had to add
file into import directory.

"""
import time
import threading
import socket
from common.protocols import Command
from common.protocols import PacketType
from common.packets import Packet, CommandPacket, AckPacket
from common.config import ROBOT_PORT, ROBOT_IP, BUFFER_SIZE

#function to send heartbeat 
def heartbeat():
    
    """
    making a new socket as was running into 
    errors with only 1 as they were trying to send 
    and recive at the same time
    
    """
    socks = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    sequence = 0 
    while True:
        
        #cba to make heartbeat subclass so using ack
        packet = AckPacket(sequence, PacketType.HEARTBEAT)
        
        socks.sendto(packet.encode(), (ROBOT_IP, ROBOT_PORT))
        sequence += 1
        time.sleep(0.1)



#defining the controller socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
sock.settimeout(0.1)

#opening a thread to constantly send heartbeat to robot
heartbeat_thread = threading.Thread(target=heartbeat, daemon=True)
heartbeat_thread.start()


#to track what packet we are sending
sequence = 0

while True:
        key = input("Command (w,a,s,d,x): ")
        
        if key == "w":
            packet = CommandPacket(sequence, PacketType.COMMAND,Command.FORWARD)
            sequence+=1
        elif key == "a":
            packet = CommandPacket(sequence, PacketType.COMMAND,Command.LEFT)
            sequence+=1
        elif key == "s":
            packet = CommandPacket(sequence, PacketType.COMMAND, Command.BACKWARD)
            sequence+=1
        elif key == "d":
            packet = CommandPacket(sequence, PacketType.COMMAND, Command.RIGHT)
            sequence+=1
        elif key == "x":
            packet = CommandPacket(sequence, PacketType.COMMAND, Command.STOP)
            sequence+=1
        else:
            print("Don't be an idiot")
            continue
        
        #sending the packet over UDP across the robot ip to the robot port
        Ack_recieved = False
        while not Ack_recieved:
            sock.sendto( packet.encode(), (ROBOT_IP, ROBOT_PORT))
            print(packet)
            
            #checks if ack has been received
            try:
                data, _ = sock.recvfrom(BUFFER_SIZE)
                ack = AckPacket.decode(data)
                Ack_recieved = True
                print("Executed successfully")
                
            except socket.timeout:
                print("Timeout...")
                print("Retransmitting")
                
            #here for debugging reasons
            except ConnectionResetError as e:
                print(e)
                print("Robot disconnected.")