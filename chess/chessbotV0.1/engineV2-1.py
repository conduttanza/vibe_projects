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
        chess.KING: 10000
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
  [-20, -10, -10, 0, -5, -10, -10, -20]
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

def Eval(board):
    score = 0
    central_squares = [chess.D4, chess.D5, chess.E4, chess.E5, chess.E6, chess.D6, chess.E3, chess.D3]
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
                continue 
        #base values
        value = piece_value(piece.piece_type)
        
        rank = chess.square_rank(square)
        file = chess.square_file(square)
        
        if piece.color == chess.BLACK:
            rank = 7 - rank  # flip for black
            
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
        #central control
        if square in central_squares:
            if piece.piece_type == chess.PAWN:
                value += 50
            elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                value += 25
        #early development
        if piece.piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP] and len(board.move_stack) < 5:
            value += 25
        #repetition penalty
        if board.is_repetition(2):
            value -= 50
        elif board.is_repetition(3):
            value -= 500
        #value to score conversion
        if piece.color == chess.WHITE:
            score -= value
        elif piece.color == chess.BLACK:
            score += value
        print("EVAL SCORE IS ", score)  
    return score

def minimax(board, depth, max, start_time, time_limit):
    #time limit set
    TIME_BUFFER = 0.05
    if time.time() - start_time > time_limit - TIME_BUFFER:
        raise TimeoutError
    #starting constants
    score = 0
    best_move = None
    #end of game
    if depth == 0 or board.is_game_over():
        return Eval(board), None
    #choose score, max = beneficial for WHITE, else - BLACK
    if max:
        max_eval = -float('inf')
        #improvement with any eval score
        legalmoves = list(board.legal_moves)
        random.shuffle(legalmoves)
        #random moves (hopefully)
        for move in legalmoves:
            piece = board.piece_at(move.from_square)
            #last moved piece
            score = Eval(board)

            from_sq = move.from_square
            to_sq = move.to_square
            piece = board.piece_at(from_sq)
            
            currently_attacked = board.is_attacked_by(not board.turn, from_sq)
            defenders_now = len(board.attackers(board.turn, from_sq))
            attackers_now = len(board.attackers(not board.turn, from_sq))

            #start simulation - study //bruteforcing SLOW//
            board.push(move)
            if board.is_checkmate():
                score -= 100000
                break
            #still?
            still_attacked = board.is_attacked_by(not board.turn, to_sq)
            defenders_after = len(board.attackers(board.turn, to_sq))
            attackers_after = len(board.attackers(not board.turn, to_sq))
            
            if currently_attacked and (attackers_now > defenders_now) and (not still_attacked or defenders_after >= attackers_after):
                score += 150
            
            if board.is_attacked_by(board.turn, move.to_square):
                attackers = board.attackers(board.turn, move.to_square)
                defenders = board.attackers(not board.turn, move.to_square)
                
                if piece and (not defenders or len(attackers) > len(defenders)):
                    value = piece_value(piece.piece_type)

                if attackers and (len(defenders) < len(attackers)):
                    value -= piece_value(piece.piece_type) * 0.9 if piece else 0
                    if value >= 50: 
                        board.pop()
                        continue
                if board.is_capture(move):
                    captured_piece = board.piece_at(move.to_square)
                    if captured_piece:
                        score += 0.75 * piece_value(captured_piece.piece_type)
                legals2 = list(board.legal_moves)
                for move1 in legals2:
                    #try to see next move if opponent can capture something else
                    board.push(move1)
                    if board.is_capture(move1):
                        captured_piece = board.piece_at(move.to_square)
                        if captured_piece:
                            score -= 0.75 * piece_value(captured_piece.piece_type)
                    board.pop()
            try:
                eval, _ = minimax(board, depth - 1, False, start_time, time_limit)
            
            
                last_move = board.peek() if board.move_stack else None
                if last_move and last_move.to_square == move.from_square:
                    score -= 50
                
                score += eval
                
                board.pop()
                
                if score > max_eval:
                    max_eval = score
                    best_move = move
            except TimeoutError:
                board.pop()
                raise     
            
        return max_eval, best_move
    else:
        min_eval = float('inf')
        #improvement with any eval score
        legalmoves = list(board.legal_moves)
        #random moves (hopefully)
        for move in legalmoves:
            piece = board.piece_at(move.from_square)
            #last moved piece
            score = Eval(board)
            #safety check
            from_sq = move.from_square
            to_sq = move.to_square
            piece = board.piece_at(from_sq)
            
            currently_attacked = board.is_attacked_by(not board.turn, from_sq)
            defenders_now = len(board.attackers(board.turn, from_sq))
            attackers_now = len(board.attackers(not board.turn, from_sq))

            #start simulation - study //bruteforcing SLOW//
            board.push(move)
            if board.is_checkmate():
                score -= 100000
                break
            #still?
            still_attacked = board.is_attacked_by(not board.turn, to_sq)
            defenders_after = len(board.attackers(board.turn, to_sq))
            attackers_after = len(board.attackers(not board.turn, to_sq))
            
            if currently_attacked and (attackers_now > defenders_now) and (not still_attacked or defenders_after >= attackers_after):
                score -= 150
                
            if board.is_attacked_by(board.turn, move.to_square):
                attackers = board.attackers(board.turn, move.to_square)
                defenders = board.attackers(not board.turn, move.to_square)
                
                if piece and (not defenders or len(attackers) > len(defenders)):
                    value = piece_value(piece.piece_type)

                if attackers and (len(defenders) < len(attackers)):
                    value += piece_value(piece.piece_type) * 0.9 if piece else 0
                    if value >= 50: 
                        board.pop()
                        continue
                if board.is_capture(move):
                    captured_piece = board.piece_at(move.to_square)
                    if captured_piece:
                        score -= 0.75 * piece_value(captured_piece.piece_type)
                legals2 = list(board.legal_moves)
                for move1 in legals2:
                    #try to see next move if opponent can capture something else
                    board.push(move1)
                    if board.is_capture(move1):
                        captured_piece = board.piece_at(move.to_square)
                        if captured_piece:
                            score += 0.75 * piece_value(captured_piece.piece_type)
                    board.pop()
            try:
                eval, _ = minimax(board, depth - 1, True, start_time, time_limit)
            
            
                last_move = board.peek() if board.move_stack else None
                if last_move and last_move.to_square == move.from_square:
                    score += 50
                
                score -= eval
                
                board.pop()
                
                if score > min_eval:
                    min_eval = score
                    best_move = move
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

        while depth <= 3:
            try:
                _, move = minimax(board, depth, True, start_time, time_limit)
                if move is not None:
                    best_move = move
                depth += 1
                print(move)
                print("depth is", depth)
            except TimeoutError:
                break
        return best_move

def get_best_move_minimax(board, time_limit=30):
    best_move = iterative_deepening(board, time_limit)
    return best_move

rand = random.randint(1,2)