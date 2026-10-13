'''Peer logging implementation to record p2p activity'''
import logging
import datetime

class Logger:
    def __init__(self, own_id: int) -> None:
        self.own_id = own_id

        self.logger = logging.getLogger(f"Peer_{own_id}")
        #base logging level is INFO so its clean and ignores like DEBUG messages
        self.logger.setLevel(logging.INFO)

        #check for log dupes
        if not self.logger.handlers:
            log_filename = f"log_peer_{self.own_id}.log"
            file_handler = logging.FileHandler(log_filename)
            #for output to console for debugging
            console_handler = logging.StreamHandler()

            # %(asctime) is timestamp so this is the prefix for all the log messages since they all start with time then peer peer_id
            log_format = f"[%(asctime)s]: Peer {self.own_id} %(message)s"
            
            #specific formatting for year-month-day then hour:min:sec
            formatter = logging.Formatter(fmt=log_format, datefmt="%Y-%m-%d %H:%M:%S")

            file_handler.setFormatter(formatter)
            console_handler.setFormatter(formatter)
            #add the file and console handlers to the actual logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

 #self logger info adds the prefix format of [time]: Peer [peer_id] so these dont have to duplicate the time and id

    def log_made_connection(self, neighbor_id: int) -> None:
        ''' TCP connection

        Whenever a peer makes a TCP connection to other peer, it generates the following log:
        [Time]: Peer [peer_ID 1] makes a connection to Peer [peer_ID 2].
        [peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer connected
        from [peer_ID 1]. The [Time] field represents the current time, which contains the date,
        hour, minute, and second. The format of [Time] is up to you.'''
        self.logger.info(f"makes a connection to Peer {neighbor_id}.")

   
    def log_received_connection(self, neighbor_id: int) -> None:
        ''' Whenever a peer is connected from another peer, it generates the following log:

        [Time]: Peer [peer_ID 1] is connected from Peer [peer_ID 2].
        [peer_ID 1] is the ID of peer who generates the log, [peer_ID 2] is the peer who has
        made TCP connection to [peer_ID 1].'''
        self.logger.info(f"is connected from Peer {neighbor_id}.")

    def log_changed_preferred_neighbors(self, neighbors: list[int]) -> None:
        '''
        Whenever a peer changes its preferred neighbors, it generates the following log:
        [Time]: Peer [peer_ID] has the preferred neighbors [preferred neighbor ID list].
        [preferred neighbor list] is the list of peer IDs separated by commas.
        '''
        
        
        neighbors_string = ",".join(map(str, neighbors))
        self.logger.info(f"has the preferred neighbors {neighbors_string}.")
        
    
    def log_changed_optimistically_unchoked_neighbor(self, neighbor_id:int) -> None:
        '''
        Whenever a peer changes its optimistically unchoked neighbor, it generates the following log:
        [Time]: Peer [peer_ID] has the optimistically unchoked neighbor [optimistically unchoked neighbor ID].
        [optimistically unchoked neighbor ID] is the peer ID of the optimistically unchoked neighbor.
        '''
        self.logger.info(f"has the optimistically unchoked neighbor {neighbor_id}.")


    def log_unchoked(self, neighbor_id:int) -> None:
        
        '''
        Whenever a peer is unchoked by a neighbor (which means when a peer receives an
        unchoking message from a neighbor), it generates the following log:
        [Time]: Peer [peer_ID 1] is unchoked by [peer_ID 2].
        [peer_ID 1] represents the peer who is unchoked and [peer_ID 2] represents the peer
        who unchokes [peer_ID 1].
        '''
        self.logger.info(f"is unchoked by {neighbor_id}.")
    


    def log_choked(self, neighbor_id: int) -> None:
        '''
        Whenever a peer is choked by a neighbor (which means when a peer receives a choking
        message from a neighbor), it generates the following log:
        [Time]: Peer [peer_ID 1] is choked by [peer_ID 2].
        [peer_ID 1] represents the peer who is choked and [peer_ID 2] represents the peer who
        chokes [peer_ID 1].
        '''
        
        
        self.logger.info(f"is choked by {neighbor_id}.")


    def log_received_have(self, neighbor_id:int, piece_index: int) -> None:
        ''' Receiving 'have' message

        Whenever a peer receives a 'have' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'have' message from [peer_ID 2] for the piece
        [piece index].
        [peer_ID 1] represents the peer who received the 'have' message and [peer_ID 2]
        represents the peer who sent the message. [piece index] is the piece index contained in
        the message. '''
        self.logger.info(f"received the 'have' message from {neighbor_id} for the piece {piece_index}.")


    def log_received_interested(self, neighbor_id: int) -> None:  
        '''receiving 'interested' message

        Whenever a peer receives an 'interested' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'interested' message from [peer_ID 2].
        [peer_ID 1] represents the peer who received the 'interested' message and [peer_ID 2]
        represents the peer who sent the message.'''
        self.logger.info(f"received the 'interested' message from {neighbor_id}.")

    def log_received_not_interested(self, neighbor_id:int) -> None:
        '''receiving 'not interested' message

        Whenever a peer receives a 'not interested' message, it generates the following log:
        [Time]: Peer [peer_ID 1] received the 'not interested' message from [peer_ID 2]. '''
        self.logger.info(f"received the 'not interested' message from {neighbor_id}.")




    def log_downloaded_piece(self, neighbor_id: int, piece_index: int, num_pieces: int) -> None:
        '''
        Whenever a peer finishes downloading a piece, it generates the following log:
        [Time]: Peer [peer_ID 1] has downloaded the piece [piece index] from [peer_ID 2]. Now the
        number of pieces it has is [number of pieces].
        [peer_ID 1] represents the peer who downloaded the piece and [peer_ID 2] represents
        the peer who sent the piece. [piece index] is the piece index the peer has downloaded.
        [number of pieces] represents the number of pieces the peer currently has.
        '''
        
        self.logger.info(f"has downloaded the piece {piece_index} from {neighbor_id}. Now the number of pieces it has is {num_pieces}.")

    def log_download_complete(self) -> None:
        '''
        Whenever a peer downloads the complete file, it generates the following log:
        [Time]: Peer [peer_ID] has downloaded the complete file.
        '''
        
        self.logger.info("has downloaded the complete file.")

