from Piece import Piece

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

black_occupancy = (black_pawns.bitboard | black_rooks.bitboard | black_knights.bitboard |
                   black_bishops.bitboard | black_queen.bitboard | black_king.bitboard)

all_occupancy = white_occupancy | black_occupancy

materials : list[Piece] = [white_pawns , white_rooks , white_knights , white_bishops , white_queen , white_king , black_pawns , black_rooks , black_knights , black_bishops , black_queen , black_king]

bitboards = {
    white_pawns.symbol: white_pawns,
    white_knights.symbol: white_knights,
    white_bishops.symbol: white_bishops,
    white_rooks.symbol: white_rooks,
    white_queen.symbol: white_queen,
    white_king.symbol: white_king,
    black_pawns.symbol: black_pawns,
    black_knights.symbol: black_knights,
    black_bishops.symbol: black_bishops,
    black_rooks.symbol: black_rooks,
    black_queen.symbol: black_queen,
    black_king.symbol: black_king,
} 