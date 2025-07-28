from GameManager import GameManager
from Materials import materials
from Piece import Piece

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

def draw_board(screen = screen, width : int = WIDTH, height : int = HEIGHT, square_size : int = SQUARE_SIZE) -> None:
    for y in range(0, height // square_size):
        for x in range(0, width // square_size):
            if x % 2 == y % 2 :
                pygame.draw.rect(screen, LIGHT, (x * square_size, y * square_size, square_size, square_size))
            else:
                pygame.draw.rect(screen, DARK, (x * square_size, y * square_size, square_size, square_size))
            if SELECTED_POS:
                if (7 - y) * 8 + x == SELECTED_POS:
                    pygame.draw.rect(screen, WHITE, (x * square_size, y * square_size, square_size, square_size))
            if SELECTED_PIECE:
                valid_moves : list[tuple[str]] = gameEngine.generate_move_for_single_piece(SELECTED_PIECE)
                for move in valid_moves:
                    
                    square = gameEngine.convert_pos_to_idx_for_UI(move[1])
                    pos = gameEngine.convert_idx_to_pos_for_UI(SELECTED_POS)
                    if move[0] == pos:
                        y = 7 - square // 8
                        x = square % 8
                        pygame.draw.rect(screen, WHITE, (x * square_size, y * square_size, square_size, square_size))


def draw_pieces(screen = screen, pieces = gameEngine.materials.values()):
    
    for piece in pieces:
        image_key = piece.get_image_key()
        image = PIECE_IMAGES[image_key]
        for i in range(64):
            if (piece.bitboard >> i) & 1:
                row = (63 - i) // 8
                col = (63 - i) % 8
                screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main() -> None:
    global SELECTED_POS, SELECTED_PIECE

    move : list[str] = []
    running = True
    load_piece_images()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for file in range(8):
                    for rank in range(8):
                        square : int = (7 - rank) * 8 + file
                        if file * SQUARE_SIZE <= mouse_pos[0] < (file + 1) * SQUARE_SIZE \
                            and rank * SQUARE_SIZE <= mouse_pos[1] < (rank + 1) * SQUARE_SIZE:
                                
                                SELECTED_POS = square
                                if gameEngine.get_piece_at(SELECTED_POS):
                                    SELECTED_PIECE = gameEngine.get_piece_at(SELECTED_POS)
                                # If there is piece at SELECTED_POS, continue processing.
                                if SELECTED_PIECE:
                                    move.append(gameEngine.convert_idx_to_pos_for_UI(SELECTED_POS))  
                                    print("SELECTED POS:", SELECTED_POS)
                                    print("SELECTED PIECE:" , SELECTED_PIECE.symbol)

                                if len(move) == 2:
                                    print("START CHECKING.......")
                                    if move[0] != move[1] and tuple(move) in gameEngine.get_all_legal_moves(gameEngine.current_player):
                                        print("OK........")
                                        gameEngine.make_move(tuple(move))
                                        gameEngine.change_player()
                                    move = []
                                    SELECTED_POS = None
                                    SELECTED_PIECE = None


        draw_board()
        draw_pieces()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
