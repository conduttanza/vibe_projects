import chess

pieces_value = {
    chess.PAWN : 1,
    chess.KNIGHT : 3,
    chess.BISHOP : 3,
    chess.ROOK : 5,
    chess.QUEEN : 9,
    chess.KING : 100 
}

pawn_table = [
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
     0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2,
     0.1,-0.1, 0.1, 0.1, 0.1, 0.1,-0.1, 0.1,
     0.0,-0.1,-0.3, 0.5, 0.5,-0.3,-0.3, 0.0,
     0.0,-0.1,-0.1, 0.5, 0.5,-0.2,-0.4,-0.3,
    -0,2,-0.2,-0,1,-0,1,-0,1,-0,1,-0,2,-0,2,
     0.1, 0.1, 0.1,-0.2,-0.2, 0.2, 0.3, 0.3,
     0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
]
knight_table = [
    -0.5,-0.3,-0.3,-0.2,-0.2,-0.3,-0.3,-0.5,
    -0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,-0.3,
    -0.2, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1,-0.2,
    -0.2, 0.0, 0.2, 0.3, 0.3, 0.2, 0.0,-0.2,
    -0.2, 0.0, 0.1, 0.2, 0.2, 0.1, 0.0,-0.2,
    -0.2, 0.0, 0.1, 0.1, 0.1, 0.1, 0.0,-0.2,
    -0.3, 0.1, 0.1, 0.1, 0.1, 0.1, 0.1,-0.3,
    -0.5,-0.1,-0.3,-0.2,-0.2,-0.3,-0.1,-0.5
]
bishop_table = [
     0.0, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.0,
     0.1, 0.2, 0.1, 0.1, 0.1, 0.1, 0.2, 0.1,
     0.2, 0.1, 0.1, 0.2, 0.2, 0.1, 0.1, 0.1,
    -0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1,-0.1,
    -0.1, 0.1, 0.3, 0.3, 0.3, 0.3, 0.1,-0.1,
     0.2, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.2,
     0.1, 0.35, 0.1, 0.1, 0.1, 0.1, 0.35, 0.1,
     0.1, 0.2,-0.1,-0.1,-0.1,-0.1, 0.2, 0.1,
]
rook_table = [
     0.0, 0.1, 0.2, 0.3, 0.3, 0.2, 0.1, 0.0,
    -0.1,-0.2,-0.1,-0.1,-0.1,-0.1,-0.2,-0.1,
    -0.2, 0.1, 0.0,-0.2,-0.2, 0.0, 0.1,-0.2,
    -0.1, 0.1, 0.2,-0.3,-0.3, 0.2, 0.1,-0.1,
    -0.1, 0.1, 0.2,-0.3,-0.3, 0.2, 0.1,-0.1,
    -0.2, 0.1, 0.0,-0.2,-0.2, 0.0, 0.1,-0.2,
     0.3, 0.4, 0.4, 0.5, 0.5, 0.4, 0.4, 0.3,
    -0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,-0.2,
]
queen_table = [
    -0.4,-0.3, 0.1, 0.2, 0.2, 0.1,-0.3,-0.4,
    -0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4,-0.3,
     0.1, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.1,
     0.2, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.2,
     0.2, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.2,
     0.1, 0.3, 0.3, 0.4, 0.4, 0.3, 0.3, 0.1,
    -0.3, 0.4, 0.3, 0.3, 0.3, 0.3, 0.4,-0.3,
    -0.4,-0.3, 0.1, 0.2, 0.2, 0.1,-0.3,-0.4,
]



def Eval(board):
    piece_score = 0
    score = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            
            value = pieces_value[piece.piece_type]
            
            position_bonus = 0 
            flipped_square = square if piece.color == chess.WHITE else chess.square_mirror(square)
            piece = board.piece_at(square)
            if piece.piece_type == chess.PAWN and board.fullmove_number < 10:
                score -= 0.2
            if piece.piece_type in [chess.KNIGHT, chess.BISHOP] and board.fullmove_number < 10:
                score += 0.2
            if piece.piece_type == chess.PAWN:
                position_bonus = pawn_table[flipped_square]
            elif piece.piece_type == chess.KNIGHT:
                position_bonus = knight_table[flipped_square]
            elif piece.piece_type == chess.BISHOP:
                position_bonus = bishop_table[flipped_square]
            elif piece.piece_type == chess.ROOK:
                position_bonus = rook_table[flipped_square]
            elif piece.piece_type == chess.QUEEN:
                position_bonus = queen_table[flipped_square]
            
            score += 0.1 * len(list(board.legal_moves))
                
            piece_score = value + position_bonus
            
        score += piece_score if piece and piece.color == chess.WHITE else -piece_score
        if board.is_capture(board.peek()):
            last_move = board.move_stack[-1]
            if last_move.to_square == square and board.is_capture(last_move):
                captured_piece = board.piece_at(last_move.to_square)
                if captured_piece and captured_piece.color != board.turn:
                    score += pieces_value.get(captured_piece, 0)
    if board.fullmove_number < 5:
        if piece and piece.piece_type == chess.PAWN and square in [chess.E4, chess.D4, chess.E5, chess.D5]:
            position_bonus += 0.3

        if piece and piece.piece_type in (chess.KNIGHT, chess.BISHOP):
            if (piece.color == chess.WHITE and chess.square_rank(square) > 0) or \
            (piece.color == chess.BLACK and chess.square_rank(square) < 7):
                position_bonus += 0.4
        # Penalty for undeveloped minor pieces
        if piece and piece.color == board.turn and piece.piece_type in (chess.KNIGHT, chess.BISHOP):
            if (piece.color == chess.WHITE and chess.square_rank(square) == 0) or \
            (piece.color == chess.BLACK and chess.square_rank(square) == 7):
                score -= 0.9


    if board.is_repetition(2): 
        score -= 0.3  
    elif board.is_repetition(3): 
        score -= 10  

    return score

def minimax(board, depth, maximizing_player):
    
    if depth == 0 or board.is_game_over():
        return Eval(board), None


    best_move = None
    if maximizing_player:
        max_eval = -float('inf')
        for move in board.legal_moves:
            
            board.push(move)
            score = Eval(board)
            piece = board.piece_at(move.to_square)
            attackers = board.attackers(not board.turn, move.to_square)
            defenders = board.attackers(board.turn, move.to_square)
            if attackers and (len(defenders) < len(attackers)):
                score -= pieces_value.get(piece.piece_type, 0) * 0.9 if piece else 0
            eval, _ = minimax(board, depth - 3, False)
            
            last_move = board.peek() if board.move_stack else None
            if last_move and last_move.to_square == move.from_square:
                score -= 0.5
                
            board.pop()
            
            if eval > max_eval:
                max_eval = eval
                best_move = move
        return max_eval, best_move
    else:
        min_eval = float('inf')
        for move in board.legal_moves:
            board.push(move)
            eval, _ = minimax(board, depth - 3, True)
            board.pop()

            if eval < min_eval:
                min_eval = eval
                best_move = move
        return min_eval, best_move

def get_best_move_minimax(board, depth=3):
    _, best_move = minimax(board, depth, board.turn == chess.WHITE)
    return best_move