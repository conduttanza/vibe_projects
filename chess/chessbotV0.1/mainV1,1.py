from engine import get_best_move_minimax
import chess

board = chess.Board()

while not board.is_game_over():
    if board.turn == chess.WHITE:
        move = get_best_move_minimax(board)
        board.push(move)
    
    print(board)
    print(move)
    #print("Legal Moves: ", list(board.legal_moves))
    
    
    move = input("choose move: ")
    try:
        chess_move = chess.Move.from_uci(move)
        if chess_move in board.legal_moves:
            board.push(chess_move)
        else:
            print("illegal move, try again")
    except:
        print("invalid format--> ie e2e4 ")
        
print("CHECKMATE: ", board.result())
print(board)