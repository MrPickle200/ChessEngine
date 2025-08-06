from Piece import Piece
from GameManager import GameManager
from Materials import materials
import math

class State:
    def __init__(self, score : int, materials : dict, move : tuple[str] = None):
        self.score = score
        self.materials = materials
        self.move = move

class AI:
    def __init__(self):
        pass
    def get_piece_square_value(self, piece: Piece, square: int) -> int:
        PAWN_TABLE = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10,-20,-20, 10, 10,  5,
            5, -5,-10,  0,  0,-10, -5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5,  5, 10,25, 25, 10,  5,  5,
            10, 10, 20,30, 30, 20, 10, 10,
            50, 50, 50,50, 50, 50, 50, 50,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
        KNIGHT_TABLE = [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -30,  5, 10,15, 15, 10,  5,-30,
            -30,  0, 15,20, 20, 15,  0,-30,
            -30,  5, 15,20, 20, 15,  5,-30,
            -30,  0, 10,15, 15, 10,  0,-30,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ]
        BISHOP_TABLE = [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -10, 10, 10,10, 10, 10, 10,-10,
            -10,  0, 10,10, 10, 10,  0,-10,
            -10,  5,  5,10, 10,  5,  5,-10,
            -10,  0,  5,10, 10,  5,  0,-10,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ]
        ROOK_TABLE = [
            0,  0,  0,  0,  0,  0,  0,  0,
            5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            0,  0,  0,  5,  5,  0,  0,  0
        ]
        QUEEN_TABLE = [
            -20,-10,-10, -5, -5,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5,  5,  5,  5,  0,-10,
            -5,  0,  5,  5,  5,  5,  0, -5,
            0,  0,  5,  5,  5,  5,  0, -5,
            -10,  5,  5,  5,  5,  5,  0,-10,
            -10,  0,  5,  0,  0,  0,  0,-10,
            -20,-10,-10, -5, -5,-10,-10,-20
        ]
        KING_TABLE_MID = [
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -30,-40,-40,-50,-50,-40,-40,-30,
            -20,-30,-30,-40,-40,-30,-30,-20,
            -10,-20,-20,-20,-20,-20,-20,-10,
            20, 20,  0,  0,  0,  0, 20, 20,
            20, 30, 10,  0,  0, 10, 30, 20
        ]

        if piece.symbol.upper() == "P":
            return PAWN_TABLE[square if piece.color == "white" else 63 - square]
        elif piece.symbol.upper() == "N":
            return KNIGHT_TABLE[square if piece.color == "white" else 63 - square]
        elif piece.symbol.upper() == "B":
            return BISHOP_TABLE[square if piece.color == "white" else 63 - square]
        elif piece.symbol.upper() == "R":
            return ROOK_TABLE[square if piece.color == "white" else 63 - square]
        elif piece.symbol.upper() == "Q":
            return QUEEN_TABLE[square if piece.color == "white" else 63 - square]
        elif piece.symbol.upper() == "K":
            return KING_TABLE_MID[square if piece.color == "white" else 63 - square]
        
        return 0

    def evaluate(self, gameEngine : GameManager) -> State:

        PIECE_VALUES = {
            'P': 100,
            'N': 320,
            'B': 330,
            'R': 500,
            'Q': 900,
            'K': 10000
        }
        
        score : int = 0
        for piece in gameEngine.materials.values():
            count = bin(piece.bitboard).count("1")
            value = PIECE_VALUES[piece.symbol.upper()]

            if piece.color == "white":
                score += value * count
            else:
                score -= value * count

            for square in range(64):
                if (piece.bitboard >> square) & 1:
                    psq_bonus = self.get_piece_square_value(piece, square)
                    if piece.color == "white":
                        score += value + psq_bonus
                    else:
                        score -= value + psq_bonus
                    break

        return State(score= score, materials= gameEngine.materials)
    
    def minimax(self, gameEngine: GameManager, depth: int, alpha: float, beta: float, maximizing: bool) -> State:
        if depth == 0 or gameEngine.game_is_over:
            return self.evaluate(gameEngine)

        best_state = None

        all_moves = gameEngine.get_all_legal_moves(player="white" if maximizing else "black")

        if not all_moves:
            # Return evaluation anyway if no legal moves (e.g. stalemate/checkmate)
            return self.evaluate(gameEngine)

        if maximizing:
            best_score = -math.inf
            for move in all_moves:
                undo_info = gameEngine.make_move("white", move)
                state = self.minimax(gameEngine, depth - 1, alpha = alpha, beta= beta, maximizing=False)
                gameEngine.undo_move(undo_info= undo_info)
                if state and state.score > best_score:
                    best_score = state.score
                    best_state = State(score=best_score, materials=gameEngine.materials, move=move)
                # Prunning
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
        else:
            best_score = math.inf
            for move in all_moves:
                undo_info = gameEngine.make_move("black", move)
                state = self.minimax(gameEngine, depth - 1, alpha = alpha, beta= beta, maximizing=True)
                gameEngine.undo_move(undo_info= undo_info)
                if state and state.score < best_score:
                    best_score = state.score
                    best_state = State(score=best_score, materials=gameEngine.materials, move=move)
                # Prunning
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
        return best_state

        
# gameEngine = GameManager(materials= materials)        
# ai = AI()
# move = ai.minimax(gameEngine= gameEngine, depth= 2, alpha= -math.inf, beta= math.inf, maximizing= False)
# print(move.move)