import chess
import random
import time

def piece_value(piece):
    if piece is None:
        return 0
    values = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }
    return values.get(piece, 0)

pawn_table = [
  [0, 0, 0, 0, 0, 0, 0, 0],
  [50, 50, 50, 50, 50, 50, 50, 50],
  [10, 10, 20, 30, 30, 20, 10, 10],
  [5, 5, 10, 55, 55, 10, 5, 5],
  [0, 0, -10, 50, 50, -10, 0, 0],
  [5, -10, -5, 20, 20, -5, -10, 5],
  [5, 10, 10, -20, -20, 10, 10, 5],
  [0, 0, 0, 0, 0, 0, 0, 0]
]

knight_table = [
  [-50, -40, -30, -30, -30, -30, -40, -50],
  [-40, -20, 0, 5, 5, 0, -20, -40],
  [-30, 5, 10, 15, 15, 10, 5, -30],
  [-30, 5, 15, 20, 20, 15, 5, -30],
  [-30, 5, 15, 20, 20, 15, 5, -30],
  [-30, 5, 20, 15, 15, 20, 5, -30],
  [-40, -20, 0, 5, 5, 0, -20, -40],
  [-50, -40, -30, -30, -30, -30, -40, -50]
]

bishop_table = [
  [-20, -10, -10, -10, -10, -10, -10, -20],
  [-10, 0, 5, 10, 10, 5, 0, -10],
  [-10, 5, 10, 15, 15, 10, 5, -10],
  [-10, 10, 15, 20, 20, 15, 10, -10],
  [-10, 5, 10, 15, 15, 10, 5, -10],
  [-10, 0, 5, 10, 10, 5, 0, -10],
  [-20, -10, -10, -10, -10, -10, -10, -20],
  [-20, -10, -10, -10, -10, -10, -10, -20]
]

rook_table = [
  [0, 0, 0, 5, 5, 0, 0, 0],
  [0, 0, 5, 10, 10, 5, 0, 0],
  [0, 5, 10, 15, 15, 10, 5, 0],
  [5, 10, 15, 20, 20, 15, 10, 5],
  [5, 10, 15, 20, 20, 15, 10, 5],
  [0, 5, 10, 15, 15, 10, 5, 0],
  [0, 0, 5, 10, 10, 5, 0, 0],
  [0, 0, 0, 5, 5, 0, 0, 0]
]

queen_table = [
  [-20, -10, -10, -5, -5, -10, -10, -20],
  [-10, 0, 5, 10, 10, 5, 0, -10],
  [-10, 5, 10, 15, 15, 10, 5, -10],
  [-5, 10, 15, 20, 20, 15, 10, -5],
  [-5, 10, 15, 20, 20, 15, 10, -5],
  [-10, 5, 10, 15, 15, 10, 5, -10],
  [-10, 0, 5, 10, 10, 5, 0, -10],
  [-20, -10, -10, 10, -5, -10, -10, -20]
]

king_table = [
  [-30, -40, -50, -60, -60, -50, -40, -30],
  [-40, -50, -60, -70, -70, -60, -50, -40],
  [-50, -60, -70, -80, -80, -70, -60, -50],
  [-60, -70, -80, -90, -90, -80, -70, -60],
  [-60, -70, -80, -90, -90, -80, -70, -60],
  [-50, -60, -70, -80, -80, -70, -60, -50],
  [-40, -50, -60, -70, -70, -60, -50, -40],
  [-30, -40, -50, -60, -60, -50, -40, -30]
]

def stage(board):
    total_material = 0
    for piece_type in [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]:
        total_material += len(board.pieces(piece_type, chess.WHITE)) * 1
        total_material += len(board.pieces(piece_type, chess.BLACK)) * 1
    
    if total_material <= 6:
        return 'endgame'
    else:
        return 'middlegame'
        
def is_king_move(move, board):
    piece = board.piece_at(move.from_square)
    return piece and piece.piece_type == chess.KING
def is_queen_move(move, board):
    piece = board.piece_at(move.from_square)
    return piece and piece.piece_type == chess.QUEEN
def evaluate_king_move_penalty(move, board):
    if is_king_move(move, board):
        if board.fullmove_number <= 15:
            return -50  
    return 0  
    
def evaluate_queen_move_penalty(move, board):
    if is_queen_move(move, board):
        if board.fullmove_number <= 15:
            return -10
    return 0 
    
def evaluate_protected_capture(move, board):
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        if captured_piece:
   
            moving_piece = board.piece_at(move.from_square)

            defenders = board.attackers(not board.turn, move.to_square)
            
            if defenders and moving_piece:
                if piece_value(moving_piece.piece_type) <= piece_value(captured_piece.piece_type):
     
                    return piece_value(captured_piece.piece_type)
                else:

                    return 0
            else:
                return piece_value(captured_piece.piece_type)
    return 0
    
def PreventSkewers(board, move):
    score = 0
    attacked_white = {sq for sq in chess.SQUARES if board.is_attacked_by(chess.WHITE, sq)}
    attacked_black = {sq for sq in chess.SQUARES if board.is_attacked_by(chess.BLACK, sq)}
    moving_piece = board.piece_at(move.from_square)
    if not moving_piece:
        return 0  
    color = moving_piece.color
    opponent_color = not color
    attacked_by_opponent = attacked_black if color == chess.WHITE else attacked_white
    if move.from_square in attacked_by_opponent:
        friendsrank = set()
        friendsfile = set()
        enemyrank = set()
        enemyfile = set()
        rank = chess.square_rank(move.from_square)
        file = chess.square_file(move.from_square)
        for sq in chess.SQUARES:
            piece = board.piece_at(sq)
            if piece:
                if chess.square_rank(sq) == rank:
                    if piece.color == color:
                        friendsrank.add(piece)
                    else:
                        enemyrank.add(piece)
                if chess.square_file(sq) == file:
                    if piece.color == color:
                        friendsfile.add(piece)
                    else:
                        enemyfile.add(piece)
        if (friendsrank and enemyrank) or (friendsfile and enemyfile):
            board.push(move)
            after_piece = board.piece_at(move.to_square)
            
            board.pop()
            if after_piece:
                piece_value_now = piece_value(after_piece)
                friendsvaluerank = sum(piece_value(f) for f in friendsrank)
                friendsvaluefile = sum(piece_value(f2) for f2 in friendsfile)
                enemyvaluerank = sum(piece_value(e) for e in enemyrank)
                enemyvaluefile = sum(piece_value(e2) for e2 in enemyfile)
                net_friend_value = friendsvaluerank + friendsvaluefile
                net_enemy_value = enemyvaluerank + enemyvaluefile
                if piece_value_now > net_friend_value and net_enemy_value < piece_value_now:
                    score += (piece_value_now - (net_friend_value - net_enemy_value))
                else:
                    score -= (piece_value_now - (net_friend_value - net_enemy_value))
    return score

def king_safety(board, move, stage):
    score = 0
    piece = board.piece_at(move.from_square)
    if piece and piece.piece_type == chess.KING:
        rank = chess.square_rank(move.to_square)
        if stage != 'endgame':
            if piece.color == chess.WHITE and rank == 0:
                score += 200
            elif piece.color == chess.BLACK and rank == 7:
                score -= 200
    return score
    
def pawn_structure(board, move):
    score = 0
    piece = board.piece_at(move.from_square)
    piece_color = piece.color
    if piece and piece.piece_type == chess.PAWN:
        connectedOZ = 0
        connectedTOT = 0
        adjacent = set()
        connected = set()
        pawn_rank = chess.square_rank(move.to_square)
        pawn_file = chess.square_file(move.to_square)
        if pawn_file < 7:
            adjacent.add(pawn_file + 1)
        if pawn_file > 0:
            adjacent.add(pawn_file - 1)
        if pawn_rank < 7:
            connected.add(pawn_rank + 1)
        if pawn_rank > 0:
            connected.add(pawn_rank - 1)
        for file in adjacent:
            square = chess.square(file, pawn_rank)
            near = board.piece_at(square)
            if near and near.color == piece_color and near.piece_type == chess.PAWN:
                connectedOZ += 1
            for rank in connected:
                sq = chess.square(file, rank)
                near1 = board.piece_at(sq)
                if near1 and near1.color == piece_color and near1.piece_type == chess.PAWN:
                    connectedTOT += 1
        score += 5 * connectedOZ
        score += 10 * connectedTOT
        if connectedTOT == 0 and connectedOZ == 0:
            score -= 20
    return score
    
def Eval(board):
    score = 0
    central_squares = [chess.D4, chess.D5, chess.E4, chess.E5, chess.E6, chess.D6, chess.E3, chess.D3]
    attacked_w_sq = set()
    attacked_b_sq = set()
    for square in chess.SQUARES:
        if board.is_attacked_by(chess.WHITE, square):
            attacked_w_sq.add(square)
        if board.is_attacked_by(chess.BLACK, square):
            attacked_b_sq.add(square)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        if piece.color == chess.WHITE:
            if square in attacked_b_sq and not board.is_attacked_by(chess.WHITE, square):
                score -= int(piece_value(piece.piece_type) * 0.6)
        if piece.color == chess.BLACK:
            if square in attacked_w_sq and not board.is_attacked_by(chess.BLACK, square):
                score += int(piece_value(piece.piece_type) * 0.6)
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
                continue 
        value = piece_value(piece.piece_type)
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        if piece.color == chess.BLACK:
            rank = 7 - rank
        if piece.piece_type == chess.PAWN:
            value += pawn_table[rank][file]
        elif piece.piece_type == chess.KNIGHT:
            value += knight_table[rank][file]
        elif piece.piece_type == chess.BISHOP:
            value += bishop_table[rank][file]
        elif piece.piece_type == chess.ROOK:
            value += rook_table[rank][file]
        elif piece.piece_type == chess.QUEEN:
            value += queen_table[rank][file]
        elif piece.piece_type == chess.KING:
            value += king_table[rank][file]
        if square in central_squares and piece.piece_type == chess.PAWN:
            value += 30
        if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP] and square in central_squares:
            value += 30
        elif piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP] and not square in central_squares:
            value -= 10
        if board.is_attacked_by(chess.WHITE, square):
            if piece.color == chess.BLACK:
                score += value
        if board.is_attacked_by(chess.BLACK, square):
            if piece.color == chess.WHITE:
                score -= value
        if piece.color == chess.WHITE:
            if square in attacked_b_sq:
                if piece.piece_type in [chess.ROOK, chess.QUEEN]:
                    value -= int(piece_value(piece.piece_type) * 1.2)
                else:
                    value -= int(piece_value(piece.piece_type) * 0.8)
        if piece.color == chess.BLACK:
            if square in attacked_w_sq:
                if piece.piece_type in [chess.ROOK, chess.QUEEN]:
                    value -= int(piece_value(piece.piece_type) * 1.2)
                elif piece.piece_type in [chess.PAWN, chess.BISHOP, chess.KNIGHT]:
                    value -= int(piece_value(piece.piece_type) * 0.8)
        if piece.color == chess.WHITE:
            score += value
        elif piece.color == chess.BLACK:
            score -= value 
    if board.is_repetition(2):
        score -= 50 if board.turn == chess.WHITE else -50
    elif board.is_repetition(3):
        score -= 500 if board.turn == chess.WHITE else -500
        if piece.color == chess.WHITE:
            score += value
        elif piece.color == chess.BLACK:
            score -= value
    return score
    
    
def minimax(board, depth, alpha, beta, boardturn, start_time, time_limit):
    TIME_BUFFER = 0.05
    if time.time() - start_time > time_limit - TIME_BUFFER:
        raise TimeoutError
    if depth == 0 or board.is_game_over():
        return Eval(board), None
    legalmoves = list(board.legal_moves)
    if not legalmoves:
        return Eval(board), None

    random.shuffle(legalmoves)
    best_move = None

    if board.turn == chess.WHITE:
        max_eval = float('-inf')

        for move in legalmoves:
            score = 0
            stage1 = stage(board)

            score += evaluate_king_move_penalty(move, board)
            score += evaluate_queen_move_penalty(move, board)
            #score += Moveval(board, move)
            score += PreventSkewers(board, move)
            score += king_safety(board, move, stage1)
            score += pawn_structure(board, move)
            score += evaluate_protected_capture(move, board)
            board.push(move)

            # Repetition check
            if board.is_repetition(3):
                score -= 500
            elif board.is_repetition(2):
                score -= 50
            
            try:
                eval, _ = minimax(board, depth - 1, alpha, beta, board.turn == chess.BLACK, start_time, time_limit)
                eval += score
                
                score += evaluate_protected_capture(move, board)
    
                
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
    
                alpha = max(alpha, eval)
                board.pop()
                if beta <= alpha:
                    
                    break
            except TimeoutError:
                    board.pop()
                    raise
        
        return max_eval, best_move
    else:  # Minimizing for Black
        min_eval = float('inf')
        legalmoves = list(board.legal_moves)
        for move in legalmoves:
           
            score = 0
            stage1 = stage(board)

            score -= evaluate_king_move_penalty(move, board)
            score -= evaluate_queen_move_penalty(move, board)
            #score -= Moveval(board, move)
            score -= PreventSkewers(board, move)
            score += king_safety(board, move, stage1)
            score -= pawn_structure(board, move)
            score -= evaluate_protected_capture(move, board)
            board.push(move)
            
             

            # Repetition check
            if board.is_repetition(3):
                score += 500
            elif board.is_repetition(2):
                score += 50
            
            
            try:
                eval, _ = minimax(board, depth - 1, alpha, beta, board.turn == chess.WHITE, start_time, time_limit)
                eval += score
                
                score -= evaluate_protected_capture(move, board)
    
                
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
    
                beta = min(beta, eval)
                board.pop()
                if beta <= alpha:
                    
                    break
            except TimeoutError:
                board.pop()
                raise
        
        return min_eval, best_move

def iterative_deepening(board, time_limit):
    if len(board.move_stack) == 1:
        if rand == 1:
            board.push(chess.Move.from_uci("e7e5"))
        elif rand == 2:
            board.push(chess.Move.from_uci("d7d5"))
    else:
        start_time = time.time()
        best_move = None
        depth = 1

        while depth <= 4:
            alpha = -float("inf")
            beta = float("inf")
            try:
                _, move = minimax(board, depth, alpha, beta, board.turn == chess.BLACK, start_time, time_limit)
                if move is not None and move in board.legal_moves:
                    best_move = move
                print(best_move)
                print("depth is", depth)
                depth += 1
                
            except TimeoutError:
                best = best_move
                return best
#        if best_move is None:
#            best_move = random.choice(list(board.legal_moves))
        return best_move

def get_best_move_minimax(board, time_limit=45):
    best_move = iterative_deepening(board, time_limit)
    return best_move

rand = random.randint(1,2)