from enum import Enum

#giving commands values
class Command(Enum):
    STOP = 0
    FORWARD = 1
    BACKWARD = 2
    LEFT = 3
    RIGHT = 4
    
class PacketType(Enum):
    COMMAND = 0
    ACK = 1
    HEARTBEAT = 2