from Piece import Piece
from Move import Move
from Materials import *

class Move_Generator:
    def __init__(self):
        pass
    def generate_white_pawns_move(self, white_pawns:Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        all_occupancy = white_occupancy | black_occupancy
        for i in range(64):
            if white_pawns.is_on_square(i):
                #Single push
                from_sq = i
                one_step = i + 8
                if one_step < 64 and self.__is_square_empty(all_occupancy, one_step): # (all_occupancy >> one_step) & 1 == 0 use to check if the targeted square is empty
                    move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(one_step))
                    all_moves.append(move)
                    #Double push if the pawn is in rank 2
                    if 8 <= i <= 15:
                        two_step = i + 16
                        if self.__is_square_empty(all_occupancy, two_step):
                            move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(two_step))
                            all_moves.append(move)
                # Capture left (<< 7)
                if from_sq % 8 != 0: # Not in rank A
                    left_capture = i + 7
                    if left_capture < 64 and self.__is_square_occupied_by_black(black_occupancy, left_capture):
                        move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(left_capture))
                        all_moves.append(move)
                # Capture right (<< 9)
                if from_sq % 8 != 7: # Not in rank H
                    right_capture = i + 9
                    if right_capture < 64 and self.__is_square_occupied_by_black(black_occupancy, right_capture):
                        move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(right_capture))
                        all_moves.append(move)
        return all_moves

    def generate_black_pawns_move(self, black_pawns:Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        all_occupancy = white_occupancy | black_occupancy
        for i in range(64):
            if black_pawns.is_on_square(i):
                #Single push
                from_sq = i
                one_step = i - 8
                if one_step >= 0 and self.__is_square_empty(all_occupancy, one_step): # (all_occupancy << one_step) & 1 == 0 use to check if the targeted square is empty
                    move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(one_step))
                    all_moves.append(move)
                    
                    #Double push if the pawn is in rank 2
                    if 48 <= i <= 55:
                        two_step = i - 16
                        if self.__is_square_empty(all_occupancy, two_step):
                            move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(two_step))
                            all_moves.append(move)
                # Capture left 
                if from_sq % 8 != 0: # Not in rank A
                    left_capture = i - 9
                    if left_capture >= 0 and self.__is_square_occupied_by_white(white_occupancy, left_capture):
                        move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(left_capture))
                        all_moves.append(move)
                # Capture right 
                if from_sq % 8 != 7: # Not in rank H
                    right_capture = i - 7
                    if right_capture >= 0 and self.__is_square_occupied_by_white(white_occupancy, right_capture):
                        move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(right_capture))
                        all_moves.append(move)

        return all_moves

    def generate_white_knights_move(self, white_knights:Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        all_occupancy = white_occupancy | black_occupancy
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
                if self.__is_square_empty(all_occupancy, to_sq) or self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                    all_moves.append(move)

        return all_moves

    def generate_black_knights_move(self, black_knights:Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        all_occupancy = white_occupancy | black_occupancy
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
                if self.__is_square_empty(all_occupancy, to_sq) or self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                    all_moves.append(move)


        return all_moves

    def generate_white_rooks_move(self, white_rooks: Piece, white_occupancy: int, black_occupancy: int) -> list:
        all_moves = []

        for from_sq in range(64):
            if not white_rooks.is_on_square(from_sq):
                continue

            from_file = from_sq % 8

            # --- LEFT ---
            to_sq = from_sq - 1
            while to_sq >= 0 and to_sq % 8 < from_file:  # prevent wrapping
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq -= 1

            # --- RIGHT ---
            to_sq = from_sq + 1
            while to_sq < 64 and to_sq % 8 > from_file:  # prevent wrapping
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq += 1

            # --- UP ---
            to_sq = from_sq + 8
            while to_sq < 64:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq += 8

            # --- DOWN ---
            to_sq = from_sq - 8
            while to_sq >= 0:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq -= 8

        return all_moves

    def generate_black_rooks_move(self, black_rooks: Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []

        for from_sq in range(64):
            if not black_rooks.is_on_square(from_sq):
                continue

            from_file = from_sq % 8

            # --- LEFT ---
            to_sq = from_sq - 1
            while to_sq >= 0 and to_sq % 8 < from_file:  # prevents wrap from file A to H
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq -= 1

            # --- RIGHT ---
            to_sq = from_sq + 1
            while to_sq < 64 and to_sq % 8 > from_file:  # prevents wrap from file H to A
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq += 1

            # --- UP ---
            to_sq = from_sq + 8
            while to_sq < 64:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq += 8

            # --- DOWN ---
            to_sq = from_sq - 8
            while to_sq >= 0:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq -= 8

        return all_moves

    def generate_white_bishops_move(self, white_bishops: Piece, white_occupancy: int, black_occupancy: int) -> list:
        all_moves = []

        for from_sq in range(64):
            if not white_bishops.is_on_square(from_sq):
                continue

            from_file = from_sq % 8

            # --------- NORTH-EAST (↗) ---------
            to_sq = from_sq + 9
            while to_sq < 64 and to_sq % 8 > from_file:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq += 9
                from_file += 1  # to ensure we don't wrap around

            # --------- NORTH-WEST (↖) ---------
            to_sq = from_sq + 7
            temp_file = from_sq % 8
            while to_sq < 64 and to_sq % 8 < temp_file:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq += 7
                temp_file -= 1

            # --------- SOUTH-EAST (↘) ---------
            to_sq = from_sq - 7
            temp_file = from_sq % 8
            while to_sq >= 0 and to_sq % 8 > temp_file:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq -= 7
                temp_file += 1

            # --------- SOUTH-WEST (↙) ---------
            to_sq = from_sq - 9
            temp_file = from_sq % 8
            while to_sq >= 0 and to_sq % 8 < temp_file:
                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                to_sq -= 9
                temp_file -= 1

        return all_moves

    def generate_black_bishops_move(self, black_bishops: Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []

        for from_sq in range(64):
            if not black_bishops.is_on_square(from_sq):
                continue

            from_file = from_sq % 8

            # --------- NORTH-EAST (↗) ---------
            to_sq = from_sq + 9
            temp_file = from_file
            while to_sq < 64 and to_sq % 8 > temp_file:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq += 9
                temp_file += 1

            # --------- NORTH-WEST (↖) ---------
            to_sq = from_sq + 7
            temp_file = from_file
            while to_sq < 64 and to_sq % 8 < temp_file:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq += 7
                temp_file -= 1

            # --------- SOUTH-EAST (↘) ---------
            to_sq = from_sq - 7
            temp_file = from_file
            while to_sq >= 0 and to_sq % 8 > temp_file:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq -= 7
                temp_file += 1

            # --------- SOUTH-WEST (↙) ---------
            to_sq = from_sq - 9
            temp_file = from_file
            while to_sq >= 0 and to_sq % 8 < temp_file:
                if self.__is_square_occupied_by_black(black_occupancy, to_sq):
                    break
                move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                all_moves.append(move)

                if self.__is_square_occupied_by_white(white_occupancy, to_sq):
                    break
                to_sq -= 9
                temp_file -= 1

        return all_moves

    def generate_white_queens_move(self, white_queen: Piece, white_occupancy: int, black_occupancy: int) -> list:
        all_moves = []
        all_moves.extend(self.generate_white_rooks_move(white_queen, white_occupancy, black_occupancy)) 
        all_moves.extend(self.generate_white_bishops_move(white_queen, white_occupancy, black_occupancy))
        return all_moves

    def generate_black_queens_move(self, black_queen: Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        all_moves.extend(self.generate_black_rooks_move(black_queen, white_occupancy, black_occupancy))
        all_moves.extend(self.generate_black_bishops_move(black_queen, white_occupancy, black_occupancy))
        return all_moves

    def generate_white_king_move(self, white_king: Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        for from_sq in range(64):
            if not white_king.is_on_square(from_sq):
                continue
            from_file = from_sq % 8
                
            #----MOVE UP, DOWN, LEFT, RIGHT, NORTH EAST, NORTH WEST, SOUTH EAST, SOUTH WEST-----
            for i in [8 , -8 , -1 , 1 , 9, 7 , -7 , -9]:
                    to_sq = from_sq + i
                    if 0 <= to_sq <= 63:
                        if abs(to_sq % 8 - from_file) <= 1 and not self.__is_square_occupied_by_white(white_occupancy, to_sq):
                            move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                            all_moves.append(move)

            break
        return all_moves      

    def generate_black_king_move(self, black_king: Piece, white_occupancy:int, black_occupancy:int) -> list:
        all_moves = []
        for from_sq in range(64):
            if not black_king.is_on_square(from_sq):
                continue
            from_file = from_sq % 8
                
            #----MOVE UP, DOWN, LEFT, RIGHT, NORTH EAST, NORTH WEST, SOUTH EAST, SOUTH WEST-----
            for i in [8 , -8 , -1 , 1 , 9, 7 , -7 , -9]:
                    to_sq = from_sq + i
                    if 0 <= to_sq <= 63:
                        if abs(to_sq % 8 - from_file) <= 1 and not self.__is_square_occupied_by_black(black_occupancy, to_sq):
                            move = (self.__convert_idx_to_pos(from_sq), self.__convert_idx_to_pos(to_sq))
                            all_moves.append(move)
            break
        
        return all_moves        

    def __is_square_empty(self, occupancy:int, square:int) -> bool:
        return ((occupancy >> square) & 1) == 0
    def __is_square_occupied_by_white(self, white_occupancy:int, square:int) -> bool:
        return (white_occupancy >> square) & 1 == 1
    def __is_square_occupied_by_black(self, black_occupancy:int, square:int) -> bool:
        return (black_occupancy >> square) & 1 == 1
    def __convert_pos_to_idx(self, pos:str) -> int:
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
    def __convert_idx_to_pos(self, idx:int) -> str:
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
