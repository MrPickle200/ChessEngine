from Piece import Piece
from Move import Move
from Materials import materials
from Move_Generator import Move_Generator

class GameManager:

    def __init__(self, materials : dict[str : Piece]):
        self.materials : dict[str : Piece] = materials
        self.current_player : str = "white"
        self.bitboards : dict[str : Piece] = {}
        self.game_is_over : bool = False
        self.made_move : bool = False
        self.promote_square : int = None
        self.last_move: tuple[str] = None
        self.last_moved_piece: Piece = None

        for piece in materials.values():
                self.bitboards[piece.symbol] = piece 

        self.white_occupancy : int = self.materials["white_pawns"].bitboard
        self.black_occupancy : int = self.materials["black_pawns"].bitboard

        for piece in self.materials.values():
            if piece.symbol != "P" and piece.color == "white":
                self.white_occupancy |= piece.bitboard
            elif piece.symbol != "p" and piece.color == "black":
                self.black_occupancy |= piece.bitboard
        self.all_occupancy : int = (self.white_occupancy | self.black_occupancy)

    def __update_occupancy(self) -> None:
        self.white_occupancy : int = self.materials["white_pawns"].bitboard
        self.black_occupancy : int = self.materials["black_pawns"].bitboard

        for piece in self.materials.values():
            if piece.symbol != "P" and piece.color == "white":
                self.white_occupancy |= piece.bitboard
            elif piece.symbol != "p" and piece.color == "black":
                self.black_occupancy |= piece.bitboard
        self.all_occupancy : int = (self.white_occupancy | self.black_occupancy)
       
        for piece in materials.values():
                self.bitboards[piece.symbol] = piece 

    def print_board(self) -> None:
        board = ['.'] * 64
        bitboards = self.bitboards

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

        

    def make_move(self, user_input : str) -> None:
            self.made_move = False
            legal_moves : list[tuple[str]] = self.get_all_legal_moves()

            move : tuple[str] = (user_input[0:2], user_input[2:])

            if move not in legal_moves:
                    print(f"{user_input} IS A ILLEGAL MOVE. PLEASE TRY AGAIN !!!")
            else :
                movement = Move(self.materials, move)

                # Track en-passant move
                if self.last_move and self.last_moved_piece:
                    en_passant : list[tuple[str]] = self.__en_passant()
                    if move in en_passant:
                        if self.current_player == "white":
                            movement.en_passant_sq = self.__convert_pos_to_idx(move[1]) - 8
                        else:
                            movement.en_passant_sq = self.__convert_pos_to_idx(move[1]) + 8
                self.last_move = move
                self.last_moved_piece = movement.get_piece()

                movement.make_move()
                
                # Update materials
                self.materials = movement.update_materials()
                self.__update_occupancy()
                self.made_move = True
                if self.__promotion():
                    self.__handle_promote()

        ## can't move pawn b7c8
                    
    def get_all_legal_moves(self) -> list[tuple[str]]:
        all_moves : list[tuple[str]] = self.__get_all_moves(self.current_player)
        legal_moves : list[tuple[str]] = []
        root_materials = self.materials

        for move in all_moves:
            movement = Move(self.materials, move)
            movement.make_move()
            self.materials = movement.update_materials()
            self.__update_occupancy()

            if self.is_king_in_check():
                movement.undo_move()
                self.materials = root_materials
                self.__update_occupancy()
                continue
            
            movement.undo_move()
            self.materials = root_materials
            self.__update_occupancy()
            legal_moves.append(move)

        if self.last_move and self.last_moved_piece:
            legal_moves.extend(self.__en_passant())

        return legal_moves

    def __get_all_moves(self, player : str) -> list[str]:
        all_moves = []
        white_materials : list[Piece] = [piece for piece in self.materials.values() if piece.color == "white"]
        black_materials : list[Piece] = [piece for piece in self.materials.values() if piece.color == "black"]
        move_generator = Move_Generator()

        if player == "white":
            for piece in white_materials:
                if piece.symbol == 'P': 
                    all_moves.extend(move_generator.generate_white_pawns_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'R':
                    all_moves.extend(move_generator.generate_white_rooks_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'N':
                    all_moves.extend(move_generator.generate_white_knights_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'B':
                    all_moves.extend(move_generator.generate_white_bishops_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'Q':
                    all_moves.extend(move_generator.generate_white_queens_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'K':
                    all_moves.extend(move_generator.generate_white_king_move(piece, self.white_occupancy, self.black_occupancy))
        else:
            for piece in black_materials:
                if piece.symbol == 'p': 
                    all_moves.extend(move_generator.generate_black_pawns_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'r':
                    all_moves.extend(move_generator.generate_black_rooks_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'n':
                    all_moves.extend(move_generator.generate_black_knights_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'b':
                    all_moves.extend(move_generator.generate_black_bishops_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'q':
                    all_moves.extend(move_generator.generate_black_queens_move(piece, self.white_occupancy, self.black_occupancy))
                elif piece.symbol == 'k':
                    all_moves.extend(move_generator.generate_black_king_move(piece, self.white_occupancy, self.black_occupancy))

        return all_moves

    def is_king_in_check(self) -> bool:
        opponent : str = "black" if self.current_player == "white" else "white"
        opponent_moves : list[tuple[str]] = self.__get_all_moves(opponent)
        king_pos : str = self.materials["white_king"].get_pos()[0] if self.current_player == "white" else self.materials["black_king"].get_pos()[0]

        for move in opponent_moves:
            if move[1] == king_pos:
                return True
        return False

    def change_player(self) -> None:
        self.current_player = "white" if self.current_player == "black" else "black"

    def __promotion(self) -> bool:
        signal : bool = False

        if self.current_player == "white":
            white_pawns : Piece = self.materials["white_pawns"]
            for square in white_pawns.get_squares():
                if 56 <= square < 64:
                    self.promote_square = square
                    white_pawns.clear_square(square)
                    signal = True
                    break
            self.materials["white_pawns"] = white_pawns
        else:
            black_pawns : Piece = self.materials["black_pawns"]
            for square in black_pawns.get_squares():
                if 0 <= square < 8:
                    self.promote_square = square
                    black_pawns.clear_square(square)
                    signal = True
                    break
            self.materials["black_pawns"] = black_pawns
        
        return signal
    
    def __handle_promote(self) -> None:
        if self.promote_square:
            bitboard : int = 1 << self.promote_square

            if self.current_player == "white":
                user_input = input("PROMOTE TO (Q/R/N/B)?: ")    
                if user_input == "Q":
                    self.materials["white_queen"].bitboard |= bitboard
                elif user_input == "R":
                    self.materials["white_rooks"].bitboard |= bitboard
                elif user_input == "N":
                    self.materials["white_knights"].bitboard |= bitboard
                elif user_input == "B":
                    self.materials["white_bishops"].bitboard |= bitboard
            else:
                user_input = input("PROMOTE TO (q/r/n/b)?: ")
                if user_input == "q":
                    self.materials["black_queen"].bitboard |= bitboard
                elif user_input == "r":
                    self.materials["black_rooks"].bitboard |= bitboard
                elif user_input == "n":
                    self.materials["black_knights"].bitboard |= bitboard
                elif user_input == "b":
                    self.materials["black_bishops"].bitboard |= bitboard
            
    def __en_passant(self) -> list[tuple[str]]:
        from_sq : int = self.__convert_pos_to_idx(self.last_move[0])
        to_sq : int = self.__convert_pos_to_idx(self.last_move[1])
        en_passant_moves : list[tuple[str]] = []
        target : int = None
        if (self.last_moved_piece.color == "white" and self.last_moved_piece.symbol == "P"):
            if 8 <= from_sq < 16:        
                target = to_sq - 8
                if target % 8 != 0:
                    if self.materials["black_pawns"].is_on_square(target + 7):
                        en_passant_moves.append((self.__convert_idx_to_pos(target + 7) , self.__convert_idx_to_pos(target)))
                if target % 8 != 7:
                    if self.materials["black_pawns"].is_on_square(target + 9):
                        en_passant_moves.append((self.__convert_idx_to_pos(target + 9) , self.__convert_idx_to_pos(target)))
        elif (self.last_moved_piece.color == "black" and self.last_moved_piece.symbol == "p"):
            if 48 <= from_sq < 56:        
                target = to_sq + 8
                if target % 8 != 0:
                    if self.materials["white_pawns"].is_on_square(target - 9):
                        en_passant_moves.append((self.__convert_idx_to_pos(target -9) , self.__convert_idx_to_pos(target)))
                if target % 8 != 7:
                    if self.materials["white_pawns"].is_on_square(target - 7):
                        en_passant_moves.append((self.__convert_idx_to_pos(target - 7) , self.__convert_idx_to_pos(target)))
        return en_passant_moves
    
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
