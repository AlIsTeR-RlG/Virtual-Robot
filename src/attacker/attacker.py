import socket
import struct
import hmac
import hashlib

#to make my life easier imagine these aren't imported
from common.config import ROBOT_PORT, ROBOT_IP, PACKET_FORMAT

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
fake = struct.pack(PACKET_FORMAT, 0, 666, 1)
tag = hmac.new(b"SECRET_KEY", fake, hashlib.sha3_256).digest()
sock.sendto( fake+tag, (ROBOT_IP, ROBOT_PORT))