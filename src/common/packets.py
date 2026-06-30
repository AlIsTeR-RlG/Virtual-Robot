"""
due to having to run in terminal have had to add
file into import directory.

"""
from common.security import SECRET_KEY
from common.protocols import Command
from common.protocols import PacketType
from common.config import PACKET_FORMAT, ACK_FORMAT
import struct
import hmac
import hashlib

#class to create packets
class Packet:
    
    def __init__(self, sequence, type, command=None):
        self.command = command
        self.sequence = sequence
        self.type = type
    
    #caclulating the hmac of the packet being sent/recieved
    def calc_hmac(self):
        message = struct.pack(PACKET_FORMAT, self.type.value, self.sequence, self.command.value)
        return hmac.new(SECRET_KEY, message, hashlib.sha3_256).digest()
    
    def verify(self, tag):
        expected = self.calc_hmac()
        return hmac.compare_digest(expected, tag)
        
    #turning commands into bytes and adding a HMAC tag to it    
    def encode(self):
        tag = self.calc_hmac()
        message = struct.pack(PACKET_FORMAT, self.type.value, self.sequence, self.command.value)
        return message + tag 
    
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
    
    #caclulating the hmac of the packet being sent/recieved
    def calc_hmac(self):
        message = struct.pack(ACK_FORMAT, self.type.value, self.sequence)
        return hmac.new(SECRET_KEY, message, hashlib.sha3_256).digest()
        
    def encode(self):
        tag = self.calc_hmac()
        message = struct.pack(ACK_FORMAT, self.type.value, self.sequence)
        return message + tag 
    
    @staticmethod
    def decode(data):
        type, sequence = struct.unpack(ACK_FORMAT, data)
        return AckPacket(sequence, PacketType(type)) 