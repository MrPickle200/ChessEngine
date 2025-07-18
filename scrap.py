white_pawns   = 0x000000000000FF00
white_rooks   = 0x0000000000000081
white_knights = 0x0000000000000042
white_bishops = 0x0000000000000024
white_queen   = 0x0000000000000008
white_king    = 0x0000000000000010

black_pawns   = 0x00FF000000000000
black_rooks   = 0x8100000000000000
black_knights = 0x4200000000000000
black_bishops = 0x2400000000000000
black_queen   = 0x0800000000000000
black_king    = 0x1000000000000000

white_occupancy = (white_pawns | white_rooks | white_knights |
                   white_bishops | white_queen | white_king)

black_occupancy = (black_pawns | black_rooks | black_knights |
                   black_bishops | black_queen | black_king)

all_occupancy = white_occupancy | black_occupancy

bitboards = {
    'P': white_pawns,
    'N': white_knights,
    'B': white_bishops,
    'R': white_rooks,
    'Q': white_queen,
    'K': white_king,
    'p': black_pawns,
    'n': black_knights,
    'b': black_bishops,
    'r': black_rooks,
    'q': black_queen,
    'k': black_king,
}

def print_board(bitboards:dict) -> None:
    board = ['.'] * 64

    # Fill in the board
    for piece, bb in bitboards.items():
        for square in range(64):
            if (bb >> square) & 1:
                board[square] = piece

    # Print the board top-down
    print("  +-----------------+")
    for rank in range(7, -1, -1):  # rank 8 to 1
        row = f"{rank + 1} | "
        for file in range(8):
            index = rank * 8 + file
            row += board[index] + ' '
        row += "|"
        print(row)
    print("  +-----------------+")
    print("    a b c d e f g h")


def get_piece_on_square(bitboards:dict, square:int) -> str:
    for piece, bb in bitboards.items():
        if (bb >> square) & 1:
            return piece
    return "."

def set_piece_on_square(square:int, piece:str) -> None:
    global bitboards
    bitboards[piece] |= 1 << square 

def clear_piece_on_square(square:int) -> None:
    global bitboards
    for piece in bitboards.keys():
        bitboards[piece] &= ~(1 << square)

def check_consistency(bitboards:dict) -> None:
    for square in range(64):
        count = 0
        for bb in bitboards.values():
            if (bb >> square) & 1:
                count += 1
        if count > 1:
            print(f"⚠️  Square {square} has multiple pieces!")

def move_piece(start_pos:str, target_pos:str) -> None:
    global bitboards
    start = convert_pos_to_idx(start_pos)
    target = convert_pos_to_idx(target_pos)

    moved_piece = None

    for piece, bb in bitboards.items():
        if (bb >> start) & 1:
            moved_piece = piece
            bitboards[piece] &= ~(1 << start)
            break
    if moved_piece is None:
        print("No piece at " + start_pos)
        return
    for piece, bb in bitboards.items():
        if (bb >> target) & 1:
            bitboards[piece] &= ~(1 << target)
    
    bitboards[moved_piece] |= (1 << target)

def convert_pos_to_idx(pos:str) -> int:
    table = {
        "a1":0,
        "b1":1,
        "c1":2,
        "d1":3,
        "e1":4,
        "f1":5,
        "g1":6,
        "h1":7
             }
    for i in range(2,8):
        for char in ['a','b','c','d','e','f','g','h']:
            table[char + str(i)] = table[char + str(i - 1)] + 8
    return table[pos]

check_consistency(bitboards)
print_board(bitboards)
move_piece("a2","a4")
print_board(bitboards)
