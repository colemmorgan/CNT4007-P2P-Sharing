'''Bitfield implmentation so peers can track what pieces they have and what they don't'''

class Bitfield:
    # Init bitfield, set has piece to true or false for all entries based on starting state from cfg
    def __init__(self, num_pieces:int, has_pieces:bool = False):
        self.num_pieces = num_pieces
        self.piece_mask = [has_pieces] * num_pieces

    def has_piece(self, i:int) -> bool:
        return self.piece_mask[i]

    def set_has_piece(self, i:int) -> None:
        # we only get a piece, but never delete
        self.piece_mask[i] = True

    def count(self) -> int:
        # return amount of pieces we have
        raise NotImplementedError

    def is_empty(self) -> bool:
        # do we have any pieces?
        raise NotImplementedError

    def piece_mask_as_bytes(self) -> bytes:
        # return the piece mask as byte array
        raise NotImplementedError

    # alternate constructror to make a bitfield from a byte array it bitfield msg format
    @classmethod
    def bitfield_from_bytes(cls, byte_arr: bytes, num_pieces: int) -> "Bitfield":
        raise NotImplementedError

    # See what pieces another peer has that we dont
    def missing_pieces(self, peer: "Bitfield") -> list[int]:
        raise NotImplementedError
