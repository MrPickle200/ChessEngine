from Piece import Piece
from Move import Move
from Materials import materials
from Move_Generator import Move_Generator

class GameManager:
    def __init__(self, materials : list[Piece]):
        self.materials : list[Piece] = materials
        self.current_player : str = "white"
        self.bitboards : dict[str : Piece] = {}

        for piece in materials:
                self.bitboards[piece.symbol] = piece 

        white_materials : list[Piece] = self.materials[0:6]
        black_materials : list[Piece] = self.materials[6:]
        self.white_occupancy : int = white_materials[0].bitboard
        self.black_occupancy : int = black_materials[0].bitboard

        for i in range(1,6):
            self.white_occupancy |= white_materials[i].bitboard
            self.black_occupancy |= black_materials[i].bitboard

        self.all_occupancy : int = (self.white_occupancy | self.black_occupancy)

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

    def make_move(self, move : tuple[str]) -> None:
        movement = Move(self.materials, move)
        movement.make_move()
    
    def generate_move(self, current_player : str) -> list:
        all_moves = []
        white_materials : list[Piece] = self.materials[0:6]
        black_materials : list[Piece] = self.materials[6:]
        move_generator = Move_Generator()

        if current_player == "white":
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


gameManager = GameManager(materials)
gameManager.print_board()
print(gameManager.generate_move("black"))