from Piece import Piece
from Move import Move
from Materials import materials

class GameManager:
    def __init__(self, materials : list[Piece]):
        self.materials = materials

        self.bitboards = {}
        for piece in materials:
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

    def make_move(self, move : tuple[str]) -> None:
        movement = Move(self.materials, move)
        movement.make_move()
    
gameManager = GameManager(materials)
gameManager.print_board()
gameManager.make_move(("a2","a7"))
gameManager.print_board()