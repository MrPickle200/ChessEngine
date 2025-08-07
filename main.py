from GameManager import GameManager
from Materials import materials
from Piece import Piece
from AI import AI
from Move import Move

import math
import pygame
pygame.init()

# Initalize setting

    # COLORS
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT = (240, 217, 181)
DARK = (181, 136, 99)

    # PARAMETERS
WIDTH : int = 800
HEIGHT : int = 800
SQUARE_SIZE : int = 100
SELECTED_POS : int = None
SELECTED_PIECE : Piece = None

gameEngine = GameManager(materials)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("CHESS")

# Global image dictionary
PIECE_IMAGES = {}

def load_piece_images():
    pieces = ['wP', 'wN', 'wB', 'wR', 'wQ', 'wK',
              'bP', 'bN', 'bB', 'bR', 'bQ', 'bK']
    for name in pieces:
        # You might want to scale them here too
        img = pygame.image.load(f"images/{name}.svg")
        PIECE_IMAGES[name] = pygame.transform.scale(img, (SQUARE_SIZE, SQUARE_SIZE))

def draw_board(screen=screen, width: int=WIDTH, height: int=HEIGHT, square_size: int=SQUARE_SIZE) -> None:
    for y in range(8):
        for x in range(8):
            screen_y = 7 - y  # flip vertical so white is at bottom
            rect = pygame.Rect(x * square_size, screen_y * square_size, square_size, square_size)

            # Color the square
            color = LIGHT if (x + y) % 2 == 0 else DARK
            pygame.draw.rect(screen, color, rect)

            # Highlight selected square
            if SELECTED_POS == y * 8 + x:
                pygame.draw.rect(screen, WHITE, rect)

            # Highlight valid moves for selected piece
            if SELECTED_PIECE and SELECTED_POS:
                valid_moves = gameEngine.generate_move_for_single_piece(SELECTED_PIECE)
                for move in valid_moves:
                    from_pos = gameEngine.convert_idx_to_pos_for_UI(SELECTED_POS)
                    if move.move[0] == from_pos:
                        to_sq = gameEngine.convert_pos_to_idx_for_UI(move.move[1])
                        to_x = to_sq % 8
                        to_y = 7 - (to_sq // 8)
                        pygame.draw.rect(screen, WHITE, pygame.Rect(to_x * square_size, to_y * square_size, square_size, square_size))

def draw_pieces(screen=screen, pieces=gameEngine.materials.values()):
    board = ["."] * 64

    for piece in pieces:
        for square in range(64):
            if (piece.bitboard >> square) & 1:
                board[square] = piece

    for idx in range(64):
        piece = board[idx]
        if piece != ".":
            image_key = piece.get_image_key()
            image = PIECE_IMAGES[image_key]

            x = idx % 8
            y = 7 - (idx // 8)  # Flip vertically so a1 is bottom-left
            screen.blit(image, (x * SQUARE_SIZE, y * SQUARE_SIZE))

def main() -> None:
    global SELECTED_POS, SELECTED_PIECE
    load_piece_images()
    move : list[str] = []
    ai = AI()
    running = True
    printed = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for y in range(8):
                    for x in range(8):
                        square : int = (7 - y) * 8 + x
                        if x * SQUARE_SIZE <= mouse_pos[0] < (x + 1) * SQUARE_SIZE \
                                and y * SQUARE_SIZE <= mouse_pos[1] < (y + 1) * SQUARE_SIZE:
                                    
                                    SELECTED_POS = square
                                    if gameEngine.get_piece_at(SELECTED_POS):
                                        SELECTED_PIECE = gameEngine.get_piece_at(SELECTED_POS)
                                    # If there is piece at SELECTED_POS, continue processing.
                                    if SELECTED_PIECE:
                                        move.append(gameEngine.convert_idx_to_pos_for_UI(SELECTED_POS))
                                    break
            if not printed:
                print(f"{gameEngine.current_player.upper()}'S TURN.")
                printed = True
                
            if gameEngine.current_player == "white":
                if len(move) == 2:
                    if move[0] != move[1]:
                        white_move = gameEngine.make_move(player= gameEngine.current_player, move= Move(materials= gameEngine.materials, move= tuple(move)))                               
                    move = []
                    SELECTED_POS = None
                    SELECTED_PIECE = None
            else:
                print("THINKING.......................")
                ai_move = ai.minimax(gameEngine= gameEngine, depth= 2, alpha= -math.inf, beta= math.inf, maximizing= False)
                print("DONE.")
                black_move = gameEngine.make_move(player= "black", move= ai_move.move)
                
            if gameEngine.made_move:
                gameEngine.change_player()    
                gameEngine.made_move = False
                printed = False
                        
        draw_board()
        draw_pieces()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
