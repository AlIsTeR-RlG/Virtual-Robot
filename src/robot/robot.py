"""
due to having to run in terminal have had to add
file into import directory.

"""

import socket
from robot.motion import RobotState
from common.packets import Packet, CommandPacket, AckPacket
from common.config import ROBOT_PORT, BUFFER_SIZE
from common.protocols import Command, PacketType

#my robot bro
robro = RobotState()

#sequence to check for duplicate protocols sent
last_sequence = -1

#command dispatch table to make it easier when calling functions 
actions = {
    Command.FORWARD: robro.move_forward,
    Command.BACKWARD: robro.move_backward,
    Command.LEFT: robro.turn_left,
    Command.RIGHT: robro.turn_right,
}

#defining the robot socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""
the 0.0.0.0 means that it is listening across all channels
and robot port means check for protocols sent to the port

"""
sock.bind(("0.0.0.0", ROBOT_PORT))

print("Robot listening...")

#sendAck = True

while True:
    
    # recieve data from socet
    data, address = sock.recvfrom(BUFFER_SIZE)
    
    #decode it and initalise a packet class with it
    packet = CommandPacket.decode(data)
#    print(packet)
    
    #checking that no duplicate packets have been sent
    if packet.sequence <= last_sequence:
        print("duplicate packet detected")
        
        #still sending Ack likely that ack wasn't recieved
        ack = AckPacket(packet.sequence, PacketType.ACK)
        sock.sendto(ack.encode(), address)
        sendAck = not sendAck
        
        #if duplicate data sent back to beginning of loop
        continue
    
    last_sequence = packet.sequence
    
    #deciding whether to stop or move the robot.
    if packet.command in actions:
        actions[packet.command]()
        print(packet)
        
        """
        if sendAck != True:
            continue
        sendAck = not sendAck
        
        """
        
        #sending Ack
        ack = AckPacket(packet.sequence, PacketType.ACK)
        sock.sendto(ack.encode(), address)
        
    elif packet.command == Command.STOP:
        print("Robot stopped.")