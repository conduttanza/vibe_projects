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

def manual_see(board, move):
    # Retrieve the captured piece (if any)
    captured_piece = board.piece_at(move.to_square)
    
    if not captured_piece:
        return 0  # No capture, no material gain or loss

    # Material value of the captured piece
    captured_value = piece_value(captured_piece)

    # Find all attackers and defenders on the destination square
    attackers = board.attackers(not board.turn, move.to_square)
    defenders = board.attackers(board.turn, move.to_square)

    # Debugging output
    print(f"Move: {move}, to_square: {move.to_square} ({chess.square_name(move.to_square)})")
    print(f"Attackers: {attackers}")
    print(f"Defenders: {defenders}")
    attackers_value = 0
    if attackers:
        print(f"Pieces attacking {chess.square_name(move.to_square)}: ")
        for square in attackers:
            piece = board.piece_at(square)
            print(f"Attacker at {chess.square_name(square)}: {piece}")
            attackers_value = piece_value(piece.piece_type)
    defenders_value = 0
    if defenders:
        print(f"Pieces defending {chess.square_name(move.to_square)}: ")
        for square in defenders:
            piece = board.piece_at(square)
            print(f"Defender at {chess.square_name(square)}: {piece}")
            defenders_value += piece_value(piece.piece_type)



    # Debug print to check attackers/defenders values
    print(f"Attackers Value: {attackers_value}, Defenders Value: {defenders_value}")

    # If attackers are stronger than defenders, it's a bad capture
    if attackers_value > defenders_value:
        return -captured_value  # Negative value (bad trade)

    # If defenders are stronger than attackers, it's a good capture
    elif defenders_value > attackers_value:
        return captured_value  # Positive value (good trade)

    # If attackers and defenders have equal value, it's a neutral trade
    else:
        return 0  # Neutral (no advantage)

def game_phase(board):
    total_material = sum(
        piece_value(piece.piece_type)
        for piece in board.piece_map().values()
        if piece.piece_type != chess.KING
    )
    # Endgame threshold: tune based on testing — try 14 as a good starting point
    return "endgame" if total_material < 14 else "middlegame"

#def opening(board, rand):
    while True:
        continue

def handle_player_move(board, mouse_pos):
    # convert mouse position to square (depends on your setup)
    # track clicked squares to make a move
    # once a legal move is formed, push it

    # Let's assume you already store `selected_square`
    global selected_square  # if you're tracking across clicks
    square = get_square_from_mouse(mouse_pos)  # implement this

    if selected_square is None:
        selected_square = square
    else:
        move = chess.Move(from_square=selected_square, to_square=square)
        if move in board.legal_moves:
            board.push(move)
        selected_square = None
    return 0

def move_value(board, move):
    score = 0
    if board.is_capture(move):
        captured_piece = board.piece_at(move.to_square)
        capturing_piece = board.piece_at(move.from_square)
        attacked_squares = board.attacks(move.to_square)
        
        attacked_my_pieces = set() #check if pieces are being attacked and which
        for square, piece in board.piece_map().items():
            piece = board.piece_at(square)
            if piece and piece.color == board.turn and board.is_attacked_by(not board.turn, square):
                if board.is_attacked_by(not board.turn, square):
                    attacked_my_pieces.add(square)
                
        board.push(move)
        
        for square in attacked_squares:
            piece = board.piece_at(square)
            if piece and piece.color != board.turn:  # board.turn has already switched after push
                print(f"Attacking opponent piece: {piece.symbol()} on {chess.square_name(square)}")
        
        for move in list(board.legal_moves):
            piece = board.piece_at(move.from_square)
            piece_val = piece_value(piece.piece_type)
            if move.from_square in attacked_my_pieces:
                # Push to see if the piece escapes attack
                board.push(move)
                if not board.is_attacked_by(not board.turn, move.to_square):
                    # We moved a piece that was under attack to safety
                    score += 50  # You can tune this value
                board.pop()
            board.push(move)
            escaped_attack = (
                move.from_square in attacked_my_pieces and
                not board.is_attacked_by(not board.turn, move.to_square)
            )
            # Detect if the destination is now attacked
            moved_into_danger = board.is_attacked_by(not board.turn, move.to_square)
            # Reward escape
            if escaped_attack:
                score += int(1 * piece_val)
            # Penalize if it moved into attack (i.e., hung itself)
            if moved_into_danger:
                score -= int(1 * piece_val)  # Penalty can be stronger than reward
            board.pop()
        hanging_after = board.is_attacked_by(not board.turn, move.to_square)

        gain = piece_value(captured_piece.piece_type) if captured_piece else 0
        loss = piece_value(capturing_piece.piece_type) if hanging_after else 0

        score += (gain - loss) * 1.5  # avoid bad trades
        if captured_piece and captured_piece.piece_type == chess.QUEEN:
            score += 1000  # really loves capturing queen
        if capturing_piece and capturing_piece.piece_type == chess.QUEEN and hanging_after:
            score -= 900  # really hates losing queen
        if captured_piece and piece_value(captured_piece) > 300:
            score += piece_value(captured_piece) * 1.2  # really loves capturing queen
        if capturing_piece and piece_value(captured_piece) > 300 and hanging_after:
            score -= piece_value(captured_piece) * 1.2  # really hates losing queen
        board.pop()
    return score

def hanging_penalty(board):
    penalty = 0
    for square in board.piece_map():
        piece = board.piece_at(square)
        if piece and piece.color == board.turn:
            if is_hanging(board, square, color = board.turn):
                penalty -= 500  # or a tuned factor
    return penalty

def is_hanging(board, square, color):
    attackers = board.attackers(not color, square)
    defenders = board.attackers(color, square)
    return len(attackers) > len(defenders)

def safe_moves(board, color):
    safe_moves = []
    for move in board.legal_moves:
        piece = board.piece_at(move.from_square)
        board.push(move)
        if piece and piece.color == color:
            if is_hanging(board, move.from_square, color):
                
                if not is_hanging(board, move.to_square, color):
                    safe_moves.append(move)
        board.pop()
    return safe_moves

def is_square_attacked_after_move(board, move):
    score = 0
    is_attacked = board.is_attacked_by(not board.turn, move.to_square)
    if is_attacked == True:
        score -= 500
    return score

def Eval(board):
    score = 0
    central_squares = [chess.D4, chess.D5, chess.E4, chess.E5, chess.E6, chess.D6, chess.E3, chess.D3]
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        value = piece_value(piece.piece_type)

        # Positional bonuses
        if piece.piece_type == chess.PAWN:
            value += pawn_table[chess.square_rank(square)][chess.square_file(square)]
        elif piece.piece_type == chess.KNIGHT:
            value += knight_table[chess.square_rank(square)][chess.square_file(square)]
        elif piece.piece_type == chess.BISHOP:
            value += bishop_table[chess.square_rank(square)][chess.square_file(square)]
        elif piece.piece_type == chess.ROOK:
            value += rook_table[chess.square_rank(square)][chess.square_file(square)]
            if len(board.move_stack) < 10:
                value -= 50  # discourage early rook moves
        elif piece.piece_type == chess.QUEEN:
            value += queen_table[chess.square_rank(square)][chess.square_file(square)]
            if board.is_attacked_by(not piece.color, square):
                value -= 900  # penalize hanging queen
                if len(board.move_stack) < 10:
                    value -= 500
            # Inside the Eval() piece loop
        if piece and piece.piece_type in [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            if board.is_attacked_by(not piece.color, square) and not board.is_attacked_by(piece.color, square):
                value -= 1000  # big penalty if attacked and not defended

        elif piece.piece_type == chess.KING:
            value += king_table[chess.square_rank(square)][chess.square_file(square)]
            if game_phase != "endgame":
                value -= 5000  # discourage early king moves
        # Central control
        if square in central_squares:
            if piece.piece_type == chess.PAWN:
                value += 100
            elif piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
                value += 150
        
        # Development bonus
        if piece.piece_type in [chess.KNIGHT, chess.BISHOP]:
            if (piece.color == chess.WHITE and chess.square_rank(square) > 0) or \
               (piece.color == chess.BLACK and chess.square_rank(square) < 7):
                value += 50
           # Repetition penalty
    if board.is_repetition(2):
        value -= 50
    elif board.is_repetition(3):
        value -= 400         
        # Add or subtract from total score
        if piece.color == chess.WHITE:
            score -= value
        else:
            score += value



    score += hanging_penalty(board)
    for move in list(board.legal_moves):
        board.push(move)
        score += is_square_attacked_after_move(board, move)
        board.pop()
        
    return score

def minimax(board, depth, maximizing_player, start_time, time_limit):
    
    TIME_BUFFER = 0.05
    if time.time() - start_time > time_limit - TIME_BUFFER:
        raise TimeoutError
    score = 0
    
    if depth == 0 or board.is_game_over():
        return Eval(board), None
    
    best_move = None

    if maximizing_player:
        #print("maxplayer")
        max_eval = -float('inf')
        legalmoves = list(board.legal_moves)
        random.shuffle(legalmoves)
        for move in legalmoves:
            piece = board.piece_at(move.from_square)
            
            score = Eval(board) + move_value(board, move)
            
            if board.is_capture(move):
                score += manual_see(board, move)
                #print("Manual SEE for move {move}: {see_score}")
                
            if piece and piece.piece_type == chess.QUEEN:
                board.push(move)
                if board.is_attacked_by(board.turn, move.to_square):
                    score -= 900  # discourage hanging queen
                    board.pop()
                    continue
                board.pop()
            board.push(move)
            # Example usage inside minimax:



            if board.is_checkmate():
                score = 100000  # Assign a very high value if the move delivers mate
            else:
                score = score
                
            if board.is_attacked_by(not board.turn, move.to_square):
                attackers = board.attackers(not board.turn, move.to_square)
                defenders = board.attackers(board.turn, move.to_square)

                #print(f"Attackers: {attackers}, Defenders: {defenders}")
                if piece and (not defenders or len(attackers) > len(defenders)):
                    value = piece_value(piece.piece_type)
                    #print(f"Evaluating move: {move} - Piece: {piece}, Value: {value}")
                    if attackers and (len(defenders) < len(attackers)):
                        score -= piece_value(piece.piece_type) * 0.9 if piece else 0
                    if value >= 150: 
                        #print(f"Skipping move: {move} - Piece {piece} is hanging and under attack!")
                        board.pop()
                        continue
    
            if board.is_capture(move):
                captured_piece = board.piece_at(move.to_square)
                if captured_piece:
                    score += piece_value(captured_piece.piece_type)
    
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
        #print(best_move)
        return max_eval, best_move
    else: #score is inverted for black
        minimum_eval = 0
        min_eval = float('inf')
        legalmoves = list(board.legal_moves)
        random.shuffle(legalmoves)
        for move in legalmoves:
            piece = board.piece_at(move.from_square)
            score = Eval(board) + move_value(board, move)
            
            if board.is_capture(move):
                score += manual_see(board, move)
                #print(f"Manual SEE for move {move}: {see_score}")
                
            if piece and piece.piece_type == chess.QUEEN:
                board.push(move)
                if board.is_attacked_by(board.turn, move.to_square):
                    score += 900  # discourage hanging queen
                    board.pop()
                    #print("skipped queen hang")
                    continue
                board.pop()
                
            board.push(move)
            
            if board.is_checkmate():
                score = -100000  # Assign a very high value if the move delivers mate
            else:
                score = score
                
            if board.is_attacked_by(not board.turn, move.to_square):
                attackers = board.attackers(not board.turn, move.to_square)
                defenders = board.attackers(board.turn, move.to_square)

                #print(f"Attackers: {attackers}, Defenders: {defenders}")
                if piece and (not defenders or len(attackers) > len(defenders)):
                    value = piece_value(piece.piece_type)
                    #print(f"Evaluating move: {move} - Piece: {piece}, Value: {value}")
                    if attackers and (len(defenders) < len(attackers)):
                        score += piece_value(piece.piece_type) * 0.9 if piece else 0
                    if value <= -300: 
                        #print(f"Skipping move: {move} - Piece {piece} is hanging and under attack!")
                        board.pop()
                        continue

            try:
                eval, _ = minimax(board, depth - 1, True, start_time, time_limit)
            
            
                last_move = board.peek() if board.move_stack else None
                if last_move and last_move.to_square == move.from_square:
                    score += 250
                    
                board.pop()
                if score < minimum_eval:
                    min_eval = score
                    minimum_eval = score
                    best_move = move
            except TimeoutError:
                board.pop()
                raise
        #print(best_move)
        return min_eval, best_move
    
rand = random.randint(1,2)

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