"""
due to having to run in terminal have had to add
file into import directory.

"""
from common.protocols import Command
import struct

#class to create packets
class Packet:
    
    def __init__(self, command):
        self.command = command
        
    #turning commands into bytes     
    def encode(self):
        return struct.pack("B", self.command.value)
    
    def __str__(self):
        return self.command
    
    #turning bytes into commands
    @staticmethod
    def decode(data):
        value = struct.unpack("B", data)[0]
        return Packet(Command(value))