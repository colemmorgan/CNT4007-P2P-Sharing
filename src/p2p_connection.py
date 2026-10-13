'''Networking implementation that transfers data formatted by message.py'''
import socket
from message import MessageType, make_handshake, validate_handshake, encode_message, int_from_4_bytes, HANDSHAKE_LENGTH

# Custom exception to handle when peer closes connection
class ConnectionClosedException(Exception):
    pass

# Each peer talks to another peer through TCP.
# Defines the handshake and then the data transfer
class P2PConnection:

    def __init__(self, socket: socket.socket):
        self.socket = socket

    # Make/recieve handshake
    def send_handshake(self, own_id:int) -> None:
        raise NotImplementedError

    def recieve_handshake(self) -> int:
        raise NotImplementedError

    # Send/recieve data after handshake is completed
    def send_data(self, msg_type: MessageType, payload: bytes = b"") -> None:
        raise NotImplementedError

    def recieve_data(self) -> tuple[int, bytes]:
        raise NotImplementedError

    #Ensure connection is cleaned up properly
    def close(self) -> None:
        raise NotImplementedError

# Create a p2p connection from PeerInfo.cfg schema
def create_connection(host: str, port: int, retries: int = 5) -> P2PConnection:
    raise NotImplementedError

# Open create a p2p connection on a specified port
class Listener:
    def __init__(self,port: int):
        self.port = port
    def accept(self) -> P2PConnection:
        raise NotImplementedError
