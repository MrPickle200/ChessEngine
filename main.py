from GameManager import GameManager
from Materials import materials

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
                pygame.draw.rect(screen, LIGHT, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            else:
                pygame.draw.rect(screen, DARK, (x * SQUARE_SIZE, y * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

def draw_pieces(screen = screen, pieces = gameEngine.materials.values()):
    
    for piece in pieces:
        image_key = piece.get_image_key()
        image = PIECE_IMAGES[image_key]
        for i in range(64):
            if (piece.bitboard >> (63 - i)) & 1:
                row = i // 8
                col = i % 8
                screen.blit(image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

def main() -> None:
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
                            print(f"Mouse at square: {square}, rank: {rank}, file: {file}")

        draw_board()
        draw_pieces()
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()
