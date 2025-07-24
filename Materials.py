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

materials : dict[str : Piece] = {"white_pawns" : white_pawns, 
                                 "white_rooks": white_rooks , 
                                 "white_knights" : white_knights , 
                                 "white_bishops" : white_bishops , 
                                 "white_queen" : white_queen , 
                                 "white_king" : white_king , 
                                 "black_pawns" : black_pawns , 
                                 "black_rooks" : black_rooks , 
                                 "black_knights" : black_knights , 
                                 "black_bishops" : black_bishops , 
                                 "black_queen" : black_queen , 
                                 "black_king" : black_king
                                 }