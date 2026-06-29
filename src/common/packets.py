"""
due to having to run in terminal have had to add
file into import directory.

"""
from common.protocols import Command
from common.protocols import PacketType
from common.config import PACKET_FORMAT, ACK_FORMAT
import struct

#class to create packets
class Packet:
    
    def __init__(self, sequence, type, command=None):
        self.command = command
        self.sequence = sequence
        self.type = type
        
    #turning commands into bytes     
    def encode(self):
        return struct.pack(PACKET_FORMAT, self.type.value, self.sequence, self.command.value)
    
    def __str__(self):
        return f"[{self.sequence}] {self.command}"
    
    #turning bytes into commands
    @staticmethod
    def decode(data):
        pass
    
"""

Made command and ack a subclass to make it easier when 
adding heartbeat and HMAC later

"""
    
class CommandPacket(Packet):
    
    def __init__(self, sequence, type, command=None):
        super().__init__(sequence, type, command)
    
    @staticmethod
    def decode(data):
        type, sequence, value = struct.unpack(PACKET_FORMAT, data)
        return CommandPacket(sequence, PacketType(type), Command(value))
        
class AckPacket(Packet):
    
    def __init__(self, sequence, type, command=None):
        super().__init__(sequence, type, command)
        
    def encode(self):
        return struct.pack(ACK_FORMAT, self.type.value, self.sequence)
    
    @staticmethod
    def decode(data):
        type, sequence = struct.unpack(ACK_FORMAT, data)
        return AckPacket(sequence, PacketType(type)) 