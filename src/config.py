'''Reads .cfg files to create p2p configuration. Examples at ../example-data'''
from dataclasses import dataclass
from pathlib import Path

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
    raise NotImplementedError

@dataclass
class PeerInfo:
    peer_id: int
    host_name: str
    listening_port: int
    has_file: bool

def create_peer_info(path:Path = Path("PeerInfo.cfg")) -> list[PeerInfo]:
    raise NotImplementedError