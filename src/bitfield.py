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
        _count: int = 0
        for i in self.piece_mask:
            if(i == True):
                _count += 1
        return _count
    
    def is_empty(self) -> bool:
        # do we have any pieces?
        return self.count() == 0

    def piece_mask_as_bytes(self) -> bytes:
        # return the piece mask as byte array where each piece is a bit
        # Convert piece mask to string
        bits = "".join("1" if has_piece else "0" for has_piece in self.piece_mask)
        # pad bits string to ensure length is a multiple of 8
        bits = bits.ljust(((self.num_pieces + 7) // 8) *8, "0")
        # return formatted bits as a byte array
        return int(bits,2).to_bytes(len(bits) // 8, "big")

    # alternate constructror to make a bitfield from a byte array it bitfield msg format
    @classmethod
    def bitfield_from_bytes(cls, byte_arr: bytes, num_pieces: int) -> "Bitfield":
        if len(byte_arr) != ((num_pieces +7) //8):
            raise ValueError("Expected and actual byte lengths do not match")
        # bytes -> bits
        bits = format(int.from_bytes(byte_arr, "big"), f"0{len(byte_arr) *8}b")
        bitfield = cls(num_pieces)

        #trim ending bits
        bitfield.piece_mask = [val == "1" for val in bits[:num_pieces]]
        return bitfield


    # See what pieces another peer has that we dont
    def missing_pieces(self, neighbor: "Bitfield") -> list[int]:
        missing = []
        for i in range(len(self.piece_mask)):
            if (self.piece_mask[i] == False and neighbor.piece_mask[i] == True):
                missing.append(i)
        return missing
