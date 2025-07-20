from Piece import *

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

def print_bitboard(bb):
    for rank in range(7, -1, -1):
        row = ""
        for file in range(8):
            sq = rank * 8 + file
            row += '1 ' if (bb >> sq) & 1 else '. '
        print(row)
    print("")

def print_board(bitboards:dict) -> None:
    board = ['.'] * 64

    # Fill in the board
    for piece, bb in bitboards.items():
        for square in range(64):
            if (bb.bitboard >> square) & 1:
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
    for i in range(2,9):
        for char in ['a','b','c','d','e','f','g','h']:
            table[char + str(i)] = table[char + str(i - 1)] + 8
    return table[pos]

def convert_idx_to_pos(idx:int) -> str:
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
    for i in range(2,9):
        for char in ['a','b','c','d','e','f','g','h']:
            table[char + str(i)] = table[char + str(i - 1)] + 8
    for key, value in table.items():
        if idx == value:
            return key
        
def generate_white_pawns_move(white_pawns:Piece, all_occupancy:int, black_occupancy:int) -> list:
    all_moves = []
    for i in range(64):
        if white_pawns.is_on_square(i):
            #Single push
            from_sq = i
            one_step = i + 8
            if one_step < 64 and is_square_empty(all_occupancy, one_step): # (all_occupancy >> one_step) & 1 == 0 use to check if the targeted square is empty
                all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(one_step)))
                
                #Double push if the pawn is in rank 2
                if 8 <= i <= 15:
                    two_step = i + 16
                    if is_square_empty(all_occupancy, two_step):
                        all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(two_step)))
            # Capture left (<< 7)
            if from_sq % 8 != 0: # Not in rank A
                left_capture = i + 7
                if left_capture < 64 and is_square_occupied_by_black(black_occupancy, left_capture):
                    all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(left_capture)))
            # Capture riight (<< 9)
            if from_sq % 7 != 0: # Not in rank H
                right_capture = i + 9
                if right_capture < 64 and is_square_occupied_by_black(black_occupancy, right_capture):
                    all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(right_capture)))

    return all_moves

def generate_black_pawns_move(black_pawns:Piece, all_occupancy:int, white_occupancy:int) -> list:
    all_moves = []
    for i in range(64):
        if black_pawns.is_on_square(i):
            #Single push
            from_sq = i
            one_step = i - 8
            if one_step >= 0 and is_square_empty(all_occupancy, one_step): # (all_occupancy << one_step) & 1 == 0 use to check if the targeted square is empty
                all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(one_step)))
                
                #Double push if the pawn is in rank 2
                if 48 <= i <= 55:
                    two_step = i - 16
                    if is_square_empty(all_occupancy, two_step):
                        all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(two_step)))
            # Capture left (>> 7)
            if from_sq % 8 != 0: # Not in rank A
                left_capture = i + 7
                if left_capture < 64 and is_square_occupied_by_white(white_occupancy, left_capture):
                    all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(left_capture)))
            # Capture riight (>> 9)
            if from_sq % 7 != 0: # Not in rank H
                right_capture = i + 9
                if right_capture < 64 and is_square_occupied_by_white(white_occupancy, right_capture):
                    all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(right_capture)))

    return all_moves

def generate_white_knight_move(white_knights:Piece, all_occupancy:int, black_occupancy:int) -> list:
    all_moves = []
    OFFSET: list[int] = [-17, -15, -10, -6, 6, 10, 15, 17]
    for from_sq in range(64):
        if not white_knights.is_on_square(from_sq):
            continue

        file = from_sq % 8
        for offset in OFFSET:
            to_sq = from_sq + offset
            if to_sq < 0 or to_sq >= 64:
                continue

            file_diff = abs(file - (to_sq % 8))
            if file_diff > 2: # Knight's move never change file over 2
                continue
            if is_square_empty(all_occupancy, to_sq) or is_square_occupied_by_black(black_occupancy, to_sq):
                all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))

    return all_moves

def generate_black_knight_move(black_knights:Piece, all_occupancy:int, white_occupancy:int) -> list:
    all_moves = []
    OFFSET: list[int] = [-17, -15, -10, -6, 6, 10, 15, 17]
    for from_sq in range(64):
        if not black_knights.is_on_square(from_sq):
            continue

        file = from_sq % 8
        for offset in OFFSET:
            to_sq = from_sq + offset
            if to_sq < 0 or to_sq >= 64:
                continue

            file_diff = abs(file - (to_sq % 8))
            if file_diff > 2: # Knight's move never change file over 2
                continue
            if is_square_empty(all_occupancy, to_sq) or is_square_occupied_by_white(white_occupancy, to_sq):
                all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))

    return all_moves

def generate_white_rooks_move(white_rooks: Piece, white_occupancy: int, black_occupancy: int) -> list:
    all_moves = []

    for from_sq in range(64):
        if not white_rooks.is_on_square(from_sq):
            continue

        from_file = from_sq % 8

        # --- LEFT ---
        to_sq = from_sq - 1
        while to_sq >= 0 and to_sq % 8 < from_file:  # prevent wrapping
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            to_sq -= 1

        # --- RIGHT ---
        to_sq = from_sq + 1
        while to_sq < 64 and to_sq % 8 > from_file:  # prevent wrapping
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            to_sq += 1

        # --- UP ---
        to_sq = from_sq + 8
        while to_sq < 64:
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            to_sq += 8

        # --- DOWN ---
        to_sq = from_sq - 8
        while to_sq >= 0:
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            to_sq -= 8

    return all_moves

def generate_black_rooks_move(black_rooks: Piece, black_occupancy: int, white_occupancy: int) -> list:
    all_moves = []
    all_occupancy = black_occupancy | white_occupancy

    for from_sq in range(64):
        if not black_rooks.is_on_square(from_sq):
            continue

        from_file = from_sq % 8

        # --- LEFT ---
        to_sq = from_sq - 1
        while to_sq >= 0 and to_sq % 8 < from_file:  # prevents wrap from file A to H
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            to_sq -= 1

        # --- RIGHT ---
        to_sq = from_sq + 1
        while to_sq < 64 and to_sq % 8 > from_file:  # prevents wrap from file H to A
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            to_sq += 1

        # --- UP ---
        to_sq = from_sq + 8
        while to_sq < 64:
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            to_sq += 8

        # --- DOWN ---
        to_sq = from_sq - 8
        while to_sq >= 0:
            if is_square_occupied_by_black(black_occupancy, to_sq):
                break
            all_moves.append((convert_idx_to_pos(from_sq), convert_idx_to_pos(to_sq)))
            if is_square_occupied_by_white(white_occupancy, to_sq):
                break
            to_sq -= 8

    return all_moves


def is_square_empty(occupancy:int, square:int) -> bool:
    return ((occupancy >> square) & 1) == 0
def is_square_occupied_by_white(white_occupancy:int, square:int) -> bool:
    return (white_occupancy >> square) & 1 == 1
def is_square_occupied_by_black(black_occupancy:int, square:int) -> bool:
    return (black_occupancy >> square) & 1 == 1

print_board(bitboards)
print(generate_black_rooks_move(black_rooks, black_rooks.bitboard, white_occupancy))