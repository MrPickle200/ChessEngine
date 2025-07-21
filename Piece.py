class Piece:
    def __init__(self, symbol:str, color:str, bitboard:int):
        self.symbol = symbol
        self.color = color 
        self.bitboard = bitboard
    def set_square(self, square:int):
        #set piece at targeted square
        self.bitboard |= (1 << square)
    def clear_square(self, square:int):
        #clear piece at targeted square
        self.bitboard &= ~(1 << square)
    def is_on_square(self, square:int) -> bool:
        #check if piece is on targeted square
        return (self.bitboard >> square) & 1 == 1
    def get_squares(self) -> list[int]:
        # get squares wwhere pieces on
        return [i for i in range(64) if (self.bitboard >> i) & 1]
    