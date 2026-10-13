'''Peer logging implementation to record p2p activity'''

class Logger:
    def __init__(self, own_id: int) -> None:
        self.own_id = own_id

 
    def log_made_connection(self, neighbor_id: int) -> None:
        ''' TCP connection

        Whenever a peer makes a TCP connection to other peer, it generates the following log:
        [Time]: Peer [peer_ID 1] makes a connection to Peer [peer_ID 2].
        [peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer connected
        from [peer_ID 1]. The [Time] field represents the current time, which contains the date,
        hour, minute, and second. The format of [Time] is up to you.'''
        raise NotImplementedError

   
    def log_received_connection(self, neighbor_id: int) -> None:
        ''' Whenever a peer is connected from another peer, it generates the following log:

        [Time]: Peer [peer_ID 1] is connected from Peer [peer_ID 2].
        [peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer who has
        made TCP connection to [peer_ID 1].'''
        raise NotImplementedError

    
    def log_received_have(self, neighbor_id:int, piece_index: int) -> None:
        ''' Receiving 'have' message

        Whenever a peer receives a 'have' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'have' message from [peer_ID 2] for the piece
        [piece index].
        [peer_ID 1] represents the peer who received the 'have' message and [peer_ID 2]
        represents the peer who sent the message. [piece index] is the piece index contained in
        the message. '''
        raise NotImplementedError

    def log_received_interest(self, neighbor_id: int) -> None:  
        '''receiving 'interested' message

        Whenever a peer receives an 'interested' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'interested' message from [peer_ID 2].
        [peer_ID 1] represents the peer who received the 'interested' message and [peer_ID 2]
        represents the peer who sent the message.'''
        raise NotImplementedError

    def log_received_not_interested(self, neighbor_id:int) -> None:
        '''receiving 'not interested' message

        Whenever a peer receives a 'not interested' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'not interested' message from [peer_ID 2]. '''
        raise NotImplementedError