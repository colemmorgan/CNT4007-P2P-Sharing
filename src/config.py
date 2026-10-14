'''Reads .cfg files to create p2p configuration. Examples at ../example-data'''
from dataclasses import dataclass
from pathlib import Path
import math

@dataclass
class CommonCfg:
    num_preferred_neighbors: int
    unchoking_interval: int
    optimistic_unchoking_interval: int
    file_name: str
    file_size: int
    piece_size:int
    # derived, not included in .cfg, needed for bitfield
    num_pieces: int

def create_common_cfg(path:Path = Path("Common.cfg")) -> CommonCfg:
    #to hold the parsed vals
    config = {}
    #open in read
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            #split by spaces
            parts = line.split()
            #needs to be a key value pair
            if len(parts) == 2:
                config[parts[0]] = parts[1]


    file_size = int(config["FileSize"])
    piece_size = int(config["PieceSize"])
    #if theres a smalll part at the end it still counts
    num_pieces = math.ceil(file_size/piece_size)

    return CommonCfg(
        num_preferred_neighbors=int(config["NumberOfPreferredNeighbors"]),
        unchoking_interval=int(config["UnchokingInterval"]),
        optimistic_unchoking_interval=int(config["OptimisticUnchokingInterval"]),
        file_name=config["FileName"],
        file_size=file_size,
        piece_size=piece_size,
        num_pieces=num_pieces
    )
    

@dataclass
class PeerInfo:
    peer_id: int
    host_name: str
    listening_port: int
    has_file: bool

def create_peer_info(path:Path = Path("PeerInfo.cfg")) -> list[PeerInfo]:
    #holds peerinfo objects
    peers = []
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            #split by spaces and should be into 4 parts from PeerIndo.cfg
            parts = line.split()
            if len(parts) == 4:
                #id string to int, port string to int, and 1 is counted as true and 0 false
                peer = PeerInfo(peer_id=int(parts[0]), host_name=parts[1], listening_port=int(parts[2]), has_file=(parts[3] == "1"))
                peers.append(peer)
    return peers



  


