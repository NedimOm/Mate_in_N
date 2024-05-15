import chess

nodes = 0

def sort_moves(board):
    forced_moves = []
    forced_moves2 = []
    forced_moves3 = []
    more_checks = []
    check_capture_moves = []
    check_moves = []
    capture_queen_moves = []
    capture_rook_moves = []
    capture_bishop_moves = []
    capture_knight_moves = []
    capture_moves = []
    other_moves = []
    
    for move in board.legal_moves:
        if board.gives_check(move):
            board.push(move)
            if(board.is_checkmate()):
                board.pop()
                return [move]
            possibleMoves = board.legal_moves.count()
            if(possibleMoves==1):
                forced_moves.append(move)
                board.pop()
                continue
            if(possibleMoves==2):
                forced_moves2.append(move)
                board.pop()
                continue
            if(possibleMoves==3):
                forced_moves3.append(move)
                board.pop()
                continue
            if(len(board.checkers())>1):
                more_checks.append(move)
                board.pop()
                continue
            board.pop()
            if board.is_capture(move):
                check_capture_moves.append(move)
            else:
                check_moves.append(move)
        elif board.is_capture(move):
            captured_piece = board.piece_type_at(move.to_square) or chess.PAWN
            if captured_piece == chess.QUEEN:
                capture_queen_moves.append(move)
            elif captured_piece == chess.ROOK:
                capture_rook_moves.append(move)
            elif captured_piece == chess.BISHOP:
                capture_bishop_moves.append(move)
            elif captured_piece == chess.KNIGHT:
                capture_knight_moves.append(move)
            else:
                capture_moves.append(move)
        else:
            other_moves.append(move)
        
    return (forced_moves + forced_moves2 + forced_moves3 + more_checks +
            check_capture_moves +
            capture_queen_moves +
            check_moves + capture_rook_moves + capture_bishop_moves + capture_knight_moves +
            capture_moves +
            other_moves)

def evaluate(board, depth, black_first):
    if(black_first):
        winner = chess.BLACK
    else:
        winner = chess.WHITE
    mate = board.is_checkmate()
    if mate and not board.turn == winner:
            return 2000 + depth
    elif mate and board.turn == winner:
            return -2000 - depth
    return 0

def minimax_alpha_beta(board, depth, maximizing_player, alpha, beta, black_first):
    global nodes
    if depth == 0 or board.is_game_over():
        eval = evaluate(board, depth, black_first)
        return None, eval

    if maximizing_player:
        max_eval = float('-inf')
        best_move = None
        for move in sort_moves(board):
            board.push(move)
            _, eval = minimax_alpha_beta(board, depth - 1, False, alpha, beta, black_first)
            if(eval > max_eval):
                max_eval = eval
                best_move = move
                if(eval == 2000):
                    board.pop()
                    return best_move, max_eval

            alpha = max(alpha, eval)
            board.pop()
            nodes += 1
            if beta <= eval:
                break
        return best_move, max_eval
    else:
        min_eval = float('inf')
        best_move = None
        for move in sort_moves(board):
            board.push(move)
            _, eval = minimax_alpha_beta(board, depth - 1, True, alpha, beta, black_first)
            if(eval < min_eval):
                min_eval = eval
                best_move = move
                if(eval == -2000):
                    board.pop()
                    return best_move, eval

            beta = min(beta, eval)
            board.pop()
            nodes += 1
            if eval <= alpha:
                break
        return best_move, min_eval

def solve_mate_in_N(N, board, depth, black, black_first):
    global nodes

    alpha = float('-inf')
    beta = float('inf')
    
    best_move, _ = minimax_alpha_beta(board, depth, black, alpha, beta, black_first)

    return best_move, nodes

nodes = 0
