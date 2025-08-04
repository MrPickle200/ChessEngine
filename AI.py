from Piece import Piece
from GameManager import GameManager
import math

class State:
    def __init__(self, score : int, materials : dict):
        self.score = score
        self.materials = materials

class AI:
    def __init__(self):
        pass

    def evaluate(self, move : tuple[str], gameEngine : GameManager) -> State:

        PIECE_VALUES = {
            'P': 100,
            'N': 320,
            'B': 330,
            'R': 500,
            'Q': 900,
            'K': 10000
        }
        
        gameEngine.make_move(move= move)
        score : int = 0
        for piece in gameEngine.materials.values():
            count = bin(piece.bitboard).count("1")
            value = PIECE_VALUES[piece.symbol.upper()]

            if piece.color == "white":
                score += value * count
            else:
                score -= value * count

        return State(score= score, materials= gameEngine.materials)
    
    def minimax(self, gameEngine : GameManager, move : tuple[str], depth : int, maximizing : bool) -> State:
        player = "white" if maximizing else "black"

        if depth == 0 or gameEngine.game_is_over:
            evaluation : State = self.evaluate(move= move, gameEngine= gameEngine)
            gameEngine.materials = evaluation.materials
            return evaluation
        
        if maximizing:
            all_moves = gameEngine.get_all_legal_moves(player= player)
            max_score = -math.inf

            for MOVE in all_moves:
                evaluation : State = self.minimax(gameEngine= gameEngine, move= MOVE, depth= depth - 1, maximizing= False)
                if max_score <= evaluation.score:
                    gameEngine.materials = evaluation.materials
                max_score = max(max_score, evaluation.score)

        else:
            all_moves = gameEngine.get_all_legal_moves(player= player)
            min_score = math.inf

            for MOVE in all_moves:
                evaluation : State = self.minimax(gameEngine= gameEngine, move= MOVE, depth= depth - 1, maximizing= True)
                if min_score >= evaluation.score:
                    gameEngine.materials = evaluation.materials
                min_score = min(max_score, evaluation.score)
    
        


