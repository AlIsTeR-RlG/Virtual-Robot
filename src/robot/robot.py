"""
due to having to run in terminal have had to add
file into import directory.

"""

import socket
import time
from robot.motion import RobotState
from common.packets import Packet, CommandPacket, AckPacket
from common.config import ROBOT_PORT, BUFFER_SIZE, COMMAND_SIZE, ACK_SIZE
from common.protocols import Command, PacketType

#checking whether a packet is a heartbeat or a command
def decode_packet(data):
    type = PacketType(data[0])
    if type == PacketType.COMMAND:
        return CommandPacket.decode(data)
    else:
        #using AckPacket as cba to make another class
        return AckPacket.decode(data)

#my robot bro
robro = RobotState()

#sequence to check for duplicate protocols sent
last_sequence = -1

#last time a packet was recieved
last_time = time.time()

#command dispatch table to make it easier when calling functions 
actions = {
    Command.FORWARD: robro.move_forward,
    Command.BACKWARD: robro.move_backward,
    Command.LEFT: robro.turn_left,
    Command.RIGHT: robro.turn_right,
}

#defining the robot socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#timeout for heartbeat
sock.settimeout(0.5)

"""
the 0.0.0.0 means that it is listening across all channels
and robot port means check for protocols sent to the port

"""
sock.bind(("0.0.0.0", ROBOT_PORT))

print("Robot listening...")

controller_alive = True

while controller_alive:
    
    try:
        
    # recieve data from socet
        data, address = sock.recvfrom(BUFFER_SIZE)
        
        if len(data) != COMMAND_SIZE and len(data) != ACK_SIZE:
            print("Packet too small")
            continue
        
        #seperating data with message and tag
        message = data[:-32]
        tag = data[-32:]
    
    #decode it and initalise a packet class with it
        packet = decode_packet(message)
        
        #checking that the tag on the message is correct
        if not packet.verify(tag):
            print("Not authorised tag")
            continue
        
        last_time = time.time()
        
        if packet.type == PacketType.HEARTBEAT:
            #print("heartbeat")
            continue
    
    #checking that no duplicate packets have been sent
        if packet.sequence <= last_sequence:
            print("duplicate packet detected")
        
        #still sending Ack likely that ack wasn't recieved
            ack = AckPacket(packet.sequence, PacketType.ACK)
            sock.sendto(ack.encode(), address)
            #sendAck = not sendAck
        
        #if duplicate data sent back to beginning of loop
            continue
    
        last_sequence = packet.sequence
    
    #deciding whether to stop or move the robot.
        if packet.command in actions:
            actions[packet.command]()
            print(packet)
            print(robro)
            
        #sending Ack
            ack = AckPacket(packet.sequence, PacketType.ACK)
            sock.sendto(ack.encode(), address)
        
        elif packet.command == Command.STOP:
            print("Robot stopped.")
            
    except socket.timeout:
        
        #stopping the robot if controller disconnects
        if time.time() - last_time > 0.5:
            print("Controller has disconnected")
            print("Stopping Robot")
            controller_alive = False