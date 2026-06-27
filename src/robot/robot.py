"""
due to having to run in terminal have had to add
file into import directory.

"""

import socket
from robot.motion import RobotState
from common.packets import Packet
from common.config import ROBOT_PORT, BUFFER_SIZE
from common.protocols import Command

#my robot bro
robro = RobotState()

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

while True:
    
    # recieve data from socet
    data, address = sock.recvfrom(BUFFER_SIZE)
    
    #decode it and initalise a packet class with it
    packet = Packet.decode(data)
    
    #deciding whether to stop or move the robot.
    if packet.command in actions:
        actions[packet.command]()
    elif packet.command == Command.STOP:
        print("Robot stopped.")