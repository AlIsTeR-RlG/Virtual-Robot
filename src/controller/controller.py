"""
due to having to run in terminal have had to add
file into import directory.

"""
import socket
from common.protocols import Command
from common.packets import Packet
from common.config import ROBOT_PORT, ROBOT_IP

#defining the controller socket
sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

while True:
        key = input("Command (w,a,s,d,x): ")
        
        if key == "w":
            packet = Packet(Command.FORWARD)
        if key == "a":
            packet = Packet(Command.LEFT)
        if key == "s":
            packet = Packet(Command.BACKWARD)
        if key == "d":
            packet = Packet(Command.RIGHT)
        if key == "x":
            packet = Packet(Command.STOP)
        
        #sending the packet over UDP across the robot ip to the robot port
        sock.sendto( packet.encode(), (ROBOT_IP, ROBOT_PORT))
        
        print(Packet," command sent.")