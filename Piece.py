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
    
white_pawns   = Piece('P','white',0x000000000000FF00)
white_rooks   = Piece('R','white',0x0000000000000081)
white_knights = Piece('N','white',0x0000000000000042)
white_bishops = Piece('B','white',0x0000000000000024)
white_queen   = Piece('Q','white',0x0000000000000008)
white_king    = Piece('K','white',0x0000000000000010)

black_pawns   = Piece('p','black',0x00FF000000000000)
black_rooks   = Piece('r','black',0x8100000000000000)
black_knights = Piece('n','black',0x4200000000000000)
black_bishops = Piece('b','black',0x2400000000000000)
black_queen   = Piece('q','black',0x0800000000000000)
black_king    = Piece('k','black',0x1000000000000000)

white_occupancy = (white_pawns.bitboard | white_rooks.bitboard | white_knights.bitboard |
                   white_bishops.bitboard | white_queen.bitboard | white_king.bitboard)
#white_occupancy = (white_pawns.bitboard | white_rooks.bitboard)

black_occupancy = (black_pawns.bitboard | black_rooks.bitboard | black_knights.bitboard |
                   black_bishops.bitboard | black_queen.bitboard | black_king.bitboard)

all_occupancy = white_occupancy | black_occupancy