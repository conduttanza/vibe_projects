import sys
import pygame
import chess
from engine2V3 import get_best_move_minimax

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

PIECES = {}

for piece in ["P", "N", "B", "R", "Q", "K"]:
    # White pieces
    PIECES[piece] = pygame.transform.scale(
        pygame.image.load(f"chessbotV0.1/assets/pieces/W/{piece}.png"), (SQ_SIZE, SQ_SIZE)
    )
    # Black pieces (lowercase)
    PIECES[piece.lower()] = pygame.transform.scale(
        pygame.image.load(f"chessbotV0.1/assets/pieces/B/{piece.lower()}.png"), (SQ_SIZE, SQ_SIZE)
    )
    
board = chess.Board()
selected_square = None
running = True
player_color = chess.WHITE

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

def draw_pieces():
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            file = chess.square_file(square)
            rank = 7 - chess.square_rank(square)  # flip vertically
            screen.blit(PIECES[piece.symbol()], pygame.Rect(file * SQ_SIZE, rank * SQ_SIZE, SQ_SIZE, SQ_SIZE))
# Game loop
def user_move(move):
    try:
        board.push(move)
        return True
    except:
        return False
while running:
    draw_board(board)
    draw_pieces()
    pygame.display.flip()

    if board.is_game_over():
        print("Game Over:", board.result())
        pygame.time.wait(2000)
        running = False
        continue

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if board.turn == player_color and event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            file = x // SQ_SIZE
            rank = 7 - (y // SQ_SIZE)
            clicked_square = chess.square(file, rank)

            if selected_square is None:
                piece = board.piece_at(clicked_square)
                if piece and piece.color == player_color:
                    selected_square = clicked_square
            else:
                move = chess.Move(selected_square, clicked_square)
                if move in board.legal_moves:
                    user_move(move)
                    selected_square = None
                else:
                    selected_square = None
    draw_board(board)
    draw_pieces()
    # Bot's turn
    if board.turn != player_color:
        bot_move = get_best_move_minimax(board)  # your minimax or evaluation function
        if bot_move:
            board.push(bot_move)

print("CHECKMATE: ", board.result())
print(board)