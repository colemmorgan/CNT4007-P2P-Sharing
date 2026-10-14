# Peer state, threading, messaging.

import threading
from message import MessageType
from bitfield import Bitfield

class PeerHandler(threading.Thread):
    def __init__(self, target_peer_id, connection, own_bitfield, logger, own_id):
        super().__init__()
        self.target_peer_id = target_peer_id
        self.connection = connection
        self.own_bitfield = own_bitfield
        self.logger = logger
        self.own_id = own_id

        # initialize neighbor bitfield to none until its received from peer
        self.neighbor_bitfield = None
        self.running = True

    def run(self):
        try:
            #send handshake and wait for handshake response
            self.connection.send_handshake(self.own_id)

            received_id = self.connection.receive_handshake()

            # if got incoming connection, we dont know their id, and if outgoing, then check that its the right one
            if self.target_peer_id == -1:
                self.target_peer_id = received_id
            elif self.target_peer_id != received_id:
                print(f"Failed handshake, IDs do not match: expected")
                self.running = False
                return


            #send bitfield if there are pieces
            if not self.own_bitfield.is_empty():
                bitfield_payload = self.own_bitfield.piece_mask_as_bytes()
                self.connection.send_data(MessageType.BITFIELD, bitfield_payload)
            #main loop for listening
            while self.running:
                message_type, payload = self.connection.receive_data()
                self.handle_message(message_type, payload)

        #any errors or closes stops the running
        except Exception as e:
            print(f"Error: {e}")
            self.running = False
        finally:
            self.connection.close()


    def handle_message(self, message_type, payload):
        
        #initial messages parsing
        if message_type == MessageType.BITFIELD:
            #parse and check interest
            self.neighbor_bitfield = Bitfield.bitfield_from_bytes(payload, self.own_bitfield.num_pieces)
            self.check_interest()


        elif message_type == MessageType.HAVE:
            # parse piece index and update neighbor bitfield then check interest
            piece_index = int.from_bytes(payload, byteorder='big')
            if self.neighbor_bitfield is not None:
                self.neighbor_bitfield.set_has_piece(piece_index)


            self.logger.log_received_have(self.target_peer_id, piece_index)
            self.check_interest()



    

        elif message_type == MessageType.INTERESTED:
            self.logger.log_received_interested(self.target_peer_id)

        elif message_type == MessageType.NOT_INTERESTED:
            self.logger.log_received_not_interested(self.target_peer_id)


    def check_interest(self):

        # cant check interest if we dont have neighbors bitfield
        if self.neighbor_bitfield is None:
            return

        missing_pieces = self.own_bitfield.missing_pieces(self.neighbor_bitfield)

        # if theres pieces needed, then interested, otherwise not interested
        if len(missing_pieces) > 0:
            self.connection.send_data(MessageType.INTERESTED)
        else:
            self.connection.send_data(MessageType.NOT_INTERESTED)
