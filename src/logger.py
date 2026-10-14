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
        self.logger.info(f"makes a connection to Peer {neighbor_id}.")
 
    def log_received_connection(self, neighbor_id: int) -> None:
        self.logger.info(f"is connected from Peer {neighbor_id}.")

    def log_changed_preferred_neighbors(self, neighbors: list[int]) -> None:
        neighbors_string = ",".join(map(str, neighbors))
        self.logger.info(f"has the preferred neighbors {neighbors_string}.")
        
    def log_changed_optimistically_unchoked_neighbor(self, neighbor_id:int) -> None:
        self.logger.info(f"has the optimistically unchoked neighbor {neighbor_id}.")

    def log_unchoked(self, neighbor_id:int) -> None:
        self.logger.info(f"is unchoked by {neighbor_id}.")
    
    def log_choked(self, neighbor_id: int) -> None:
        self.logger.info(f"is choked by {neighbor_id}.")


    def log_received_have(self, neighbor_id:int, piece_index: int) -> None:
        self.logger.info(f"received the 'have' message from {neighbor_id} for the piece {piece_index}.")


    def log_received_interested(self, neighbor_id: int) -> None:  
        self.logger.info(f"received the 'interested' message from {neighbor_id}.")

    def log_received_not_interested(self, neighbor_id:int) -> None:
        self.logger.info(f"received the 'not interested' message from {neighbor_id}.")

    def log_downloaded_piece(self, neighbor_id: int, piece_index: int, num_pieces: int) -> None:
        self.logger.info(f"has downloaded the piece {piece_index} from {neighbor_id}. Now the number of pieces it has is {num_pieces}.")

    def log_download_complete(self) -> None:
        self.logger.info("has downloaded the complete file.")

