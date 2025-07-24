from Piece import Piece

class Move:

    def __init__(self, materials : dict[str : Piece], move : tuple[str]):
        self.materials : dict[str : Piece] = materials
        self.move = move
        self.piece : Piece = None
        self.target : Piece = None
        self.en_passant_sq : int = None

        for piece in materials.values():
            if ((piece.bitboard >> self.__convert_pos_to_idx(move[0])) & 1) == 1:
                self.piece = piece
            if ((piece.bitboard >> self.__convert_pos_to_idx(move[1])) & 1) == 1:
                self.target = piece

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
        if self.get_en_passant_piece():
            self.get_en_passant_piece().clear_square(self.en_passant_sq)

        self.piece.set_square(target)
        self.piece.clear_square(current_pos)

    def undo_move(self) -> None:
        target: int = self.__convert_pos_to_idx(self.move[1])
        current_pos: int = self.__convert_pos_to_idx(self.move[0])

        self.piece.set_square(current_pos)
        self.piece.clear_square(target)
        if self.target:
            self.target.set_square(target)
    
    def update_materials(self) -> dict[str : Piece]:
        return self.materials

    def is_capture(self) -> bool: # Use to check if the move was captured opponent piece
        return self.target is not None

    def get_en_passant_piece(self) -> Piece | None:
        for piece in self.materials.values():
            if self.en_passant_sq:
                if ((piece.bitboard >> self.en_passant_sq) & 1) == 1:
                    return piece

    def get_piece(self) -> Piece | None:
        return self.piece