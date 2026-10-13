'''Defines message spec and implements basic data operations'''
from enum import IntEnum

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
    raise NotImplementedError

# Ensure correctness of handshake header and extract peer id
def validate_handshake(data: bytes) -> int:
    raise NotImplementedError

# Encode message by prepending message length and type fields
def encode_message(msg_type: MessageType, msg_payload: bytes = b"") -> bytes:
    raise NotImplementedError

# Helper functions to convert from int and bytes (used by pieces, peer id, etc)
def int_from_4_bytes(b:bytes) -> int:
    raise NotImplementedError

def int_to_4_bytes(num: int) -> bytes:
    raise NotImplementedError