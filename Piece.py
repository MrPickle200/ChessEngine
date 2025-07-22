class Piece:
    def __init__(self, symbol:str, color:str, bitboard:int):
        self.symbol = symbol
        self.color = color 
        self.bitboard = bitboard
    def set_square(self, square:int):
        #set piece at targeted square
        self.bitboard |= (1 << square)
    def clear_square(self, square:int):
        #clear piece at targeted square
        self.bitboard &= ~(1 << square)
    def is_on_square(self, square:int) -> bool:
        #check if piece is on targeted square
        return (self.bitboard >> square) & 1 == 1
    def get_squares(self) -> list[int]:
        # get squares wwhere pieces on
        return [i for i in range(64) if (self.bitboard >> i) & 1]
    def get_pos(self) -> list[str]:
        return [self.__convert_idx_to_pos(i) for i in range(64) if (self.bitboard >> i) & 1]
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