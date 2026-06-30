#info for sending packets to robot

ROBOT_IP = "127.0.0.1"
ROBOT_PORT = 9999
BUFFER_SIZE = 1024

PACKET_FORMAT = "!BIB"
ACK_FORMAT = "!BI"

#sizes of packets (the 32 is the HMAC)
COMMAND_SIZE = 6 + 32
ACK_SIZE = 5 + 32