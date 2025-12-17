import pygame
import chess
import time
from engine import get_bot_move

# Pygame setup
pygame.init()
WIDTH, HEIGHT = 480, 480
SQ_SIZE = WIDTH // 8
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess Bot GUI")
clock = pygame.time.Clock()

# Colors
WHITE = (240, 217, 181)
BROWN = (181, 136, 99)

# Load piece images
PIECES = {}
for piece in ["P", "N", "B", "R", "Q", "K", "p", "n", "b", "r", "q", "k"]:
    PIECES[piece] = pygame.transform.scale(
        pygame.image.load(f"https://images.chesscomfiles.com/chess-themes/pieces/neo/150/{piece}.png"), (SQ_SIZE, SQ_SIZE)
    )

# Draw the board and pieces
def draw_board(board):
    for row in range(8):
        for col in range(8):
            color = WHITE if (row + col) % 2 == 0 else BROWN
            pygame.draw.rect(screen, color, pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)
            if piece:
                screen.blit(PIECES[piece.symbol()], pygame.Rect(col * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))

# Game loop
def main():
    board = chess.Board()
    running = True

    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not board.is_game_over():
            move = get_bot_move(board)
            board.push(move)
            time.sleep(0.5)  # Add delay to see moves happen

        draw_board(board)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
