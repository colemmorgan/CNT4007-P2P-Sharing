'''Networking implementation that transfers data formatted by message.py'''
import socket
import threading
from message import MessageType, make_handshake, validate_handshake, encode_message, int_from_4_bytes, HANDSHAKE_LENGTH

# Custom exception to handle when peer closes connection
class ConnectionClosedException(Exception):
    pass

# Each peer talks to another peer through TCP.
# Defines the handshake and then the data transfer
class P2PConnection:

    def __init__(self, _socket: socket.socket):
        self._socket = _socket
        # write lock so threads don't write at same time on same con
        self._send_lock = threading.Lock()

    # read bytes from tcp stream until we get desired amount. Implementation from
    # https://docs.python.org/3/howto/sockets.html
    def _receive_bytes(self, num_bytes: int) -> bytes:
        chunks = []
        bytes_recd = 0

        while bytes_recd < num_bytes:
            try:
                chunk = self._socket.recv(min(num_bytes - bytes_recd, 2048))
            except OSError as e:
                raise ConnectionClosedException() from e
            if chunk == b'':
                raise ConnectionClosedException("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return b''.join(chunks)

    # Send handshake to peer
    def send_handshake(self, own_id:int) -> None:
        self._socket.sendall(make_handshake(own_id))

    # Handshake is 32bytes, read until we get all, then validate
    def receive_handshake(self) -> int:
        data = self._receive_bytes(HANDSHAKE_LENGTH)
        return validate_handshake(data)

    # Send/recieve data after handshake is completed
    def send_data(self, msg_type: MessageType, payload: bytes = b"") -> None:
        # encode data in format we can send
        data = encode_message(msg_type, payload)
        
        # Enter critical area and ensure we release after
        with self._send_lock:
            try:
                self._socket.sendall(data)
            except OSError as e:
                raise ConnectionClosedException() from e

    def receive_data(self) -> tuple[int, bytes]:
        # read first 4 bytes to get length of message, then read message
        msg_len = int_from_4_bytes(self._receive_bytes(4))
        if(msg_len < 1):
            raise ValueError("Invalid msg length")
        type_payload = self._receive_bytes(msg_len)
        msg_type = type_payload[0]
        payload = type_payload[1:]

        return (msg_type, payload)

    #Ensure connection is cleaned up properly
    def close(self) -> None:
        try:
            # Close connection with peers
            self._socket.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass # case when peer already shutdown
        # Close socket entirely
        self._socket.close()


# Create a p2p connection from PeerInfo.cfg schema
def create_p2p_connection(host: str, port: int) -> P2PConnection:
    try:
        _socket = socket.create_connection((host,port))
        return P2PConnection(_socket)
    except:
        raise

# listen on specified port and create connections for peers
class Listener:
    def __init__(self,port: int):
        self.port = port

        # https://docs.python.org/3/library/socket.html#example

        #1. create socket
        self._server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM) 
        #2. configure socket to be reusable
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind(("", port))
        # start listening for connections once everything is setup
        self._server.listen()

    def accept(self) -> P2PConnection:
        _socket, addr = self._server.accept()
        return P2PConnection(_socket)
    
    def close(self) -> None:
        self._server.close()
