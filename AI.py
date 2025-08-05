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

        return State(score= score, materials= gameEngine.materials)
    
    def minimax(self, gameEngine: GameManager, depth: int, maximizing: bool) -> State:
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
                state = self.minimax(gameEngine, depth - 1, maximizing=False)
                gameEngine.undo_move(undo_info= undo_info)
                if state and state.score > best_score:
                    best_score = state.score
                    best_state = State(score=best_score, materials=gameEngine.materials, move=move)
        else:
            best_score = math.inf
            for move in all_moves:
                undo_info = gameEngine.make_move("black", move)
                state = self.minimax(gameEngine, depth - 1, maximizing=True)
                gameEngine.undo_move(undo_info= undo_info)
                if state and state.score < best_score:
                    best_score = state.score
                    best_state = State(score=best_score, materials=gameEngine.materials, move=move)

        return best_state

        
ai = AI()
gameEngine = GameManager(materials= materials)

best_state = ai.minimax(gameEngine= gameEngine, depth= 2, maximizing= True)

print(best_state.move)