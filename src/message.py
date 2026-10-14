'''Defines message spec and implements basic data operations'''
from enum import IntEnum
import struct

HANDSHAKE_HEADER = b'P2PFILESHARINGPROJ'
HANDSHAKE_ZEROS = bytes(10)
HANDSHAKE_LENGTH = 32

class MessageType(IntEnum):
    CHOKE = 0
    UNCHOKE = 1
    INTERESTED = 2
    NOT_INTERESTED = 3
    HAVE = 4
    BITFIELD = 5
    REQUEST = 6
    PIECE = 7

# Build 32 byte handshake: header + zero bits + peer id
def make_handshake(peer_id: int) -> bytes: 
    return HANDSHAKE_HEADER + HANDSHAKE_ZEROS + int_to_4_bytes(peer_id)

# Ensure correctness of handshake header and extract peer id
def validate_handshake(data: bytes) -> int:
    if(len(data) != HANDSHAKE_LENGTH):
        raise ValueError(f"Invalid Handshake length. Received {len(data)}")
    
    handshake = data[:18]
    if(handshake != HANDSHAKE_HEADER):
        raise ValueError(f"Invalid handshake header. Received {handshake!r}")
    
    zeros = data[18:28]
    if(zeros != HANDSHAKE_ZEROS):
        raise ValueError(f"Invalid handshake zeros. Received {zeros!r}")
    
    pid = data [28:]
    return int_from_4_bytes(pid)

# Encode message by prepending message length and type fields
def encode_message(msg_type: MessageType, msg_payload: bytes = b"") -> bytes:
    msg_len: int = len(msg_payload) + 1 # add type byte to length
    return int_to_4_bytes(msg_len) + bytes([msg_type]) + msg_payload

# Helper functions to convert from int and bytes (used by pieces, peer id, etc)
def int_from_4_bytes(b:bytes) -> int:
    return struct.unpack(">I",b)[0]

def int_to_4_bytes(num: int) -> bytes:
    return struct.pack(">I", num)