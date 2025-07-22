from Piece import Piece

class Move:

    def __init__(self, materials : list[Piece], move : tuple[str]):
        self.materials = materials
        self.move = move
        self.piece = None
        self.target = None

        for piece in materials:
            if ((piece.bitboard >> self.__convert_pos_to_idx(move[0])) & 1) == 1:
                self.piece = piece
                break
        for piece in materials:
            if ((piece.bitboard >> self.__convert_pos_to_idx(move[1])) & 1) == 1:
                self.target = piece
                break

    def __convert_pos_to_idx(self,pos:str) -> int:
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
    
    def make_move(self) -> None:
        target: int = self.__convert_pos_to_idx(self.move[1])
        current_pos: int = self.__convert_pos_to_idx(self.move[0])
        
        if self.target:
            self.target.clear_square(target)

        self.piece.set_square(target)
        self.piece.clear_square(current_pos)

    def undo_move(self) -> None:
        target: int = self.__convert_pos_to_idx(self.move[1])
        current_pos: int = self.__convert_pos_to_idx(self.move[0])

        self.piece.set_square(current_pos)
        self.piece.clear_square(target)
        if self.target:
            self.target.set_square(target)
    
    def update_materials(self) -> list[Piece]:
        return self.materials

    def is_capture(self) -> bool: # Use to check if the move was captured opponent piece
        return self.target is not None

    def get_captured_piece(self) -> Piece | None:
        return self.target

    def display_move(self) -> str:
        return self.move[0] + self.move[1]