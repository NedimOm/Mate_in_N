from search import solve_mate_in_N
from flask import Flask, render_template, request
import chess.svg
import time

app = Flask("mateInN")

def getMoves(starting_board_FEN, depth, black_first):
    N = depth
    boards = []

    my_board = chess.Board(starting_board_FEN)
    board_svg = chess.svg.board(board=my_board, size=450)
    boards.append(board_svg)

    start_time = time.time()
    nodes = 0

    for i in range(N):
        best_move, nodes = solve_mate_in_N(N, my_board, 2*(N-i)-1, True, black_first)

        if(best_move):
            turn = my_board.turn
            if(my_board.is_check()):
                if(turn==chess.WHITE):
                    board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],check=my_board.king(chess.WHITE) ,size=450)
                else:
                    board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],check=my_board.king(chess.BLACK) ,size=450)
            else:
                board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],size=450)

            my_board.push(best_move)
            boards.append(board_svg)

        if(N-i>1):
            best_move, nodes = solve_mate_in_N(N, my_board, 2*(N-i)-2, False, black_first)
            
            if(best_move):
                turn = my_board.turn
                if(my_board.is_check()):
                    if(turn==chess.WHITE):
                        board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],check=my_board.king(chess.WHITE) ,size=450)
                    else:
                        board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],check=my_board.king(chess.BLACK) ,size=450)
                else:
                    board_svg = chess.svg.board(board=my_board, arrows=[chess.svg.Arrow(best_move.from_square, best_move.to_square, color="#0000cccc")],size=450)
                
                my_board.push(best_move) 
                boards.append(board_svg)
                
        if(N-i==1):
            if(my_board.is_checkmate()):
                if(my_board.turn == chess.WHITE):
                    board_svg = chess.svg.board(board=my_board, check=my_board.king(chess.WHITE), squares=chess.SquareSet([my_board.king(chess.WHITE)]) ,size=450)    
                else:
                    board_svg = chess.svg.board(board=my_board, check=my_board.king(chess.BLACK), squares=chess.SquareSet([my_board.king(chess.BLACK)]) ,size=450)           
            else:
                board_svg = chess.svg.board(board=my_board, size=450)
            boards.append(board_svg)
    
    end_time = time.time()            
    
    return boards, round(end_time-start_time, 2) , nodes

@app.route('/', methods=['GET', 'POST'])
def board():
    fen = ''
    depth = 0
    svg_filenames = []
    time = 0
    nodes = 0
    black_first = False

    if request.method == 'POST':
        fen = request.form['fen'] or ''
        depth = int(request.form['depth']) or 0
        if(request.form.get('blackFirst', '0') == 'on'):
            black_first = True
        else:
            black_first = False

        board_svgs, time, nodes = getMoves(fen, depth, black_first) or ([], 0, 0)
        
        svg_filename = ''

        for i in range(len(board_svgs)):
            svg_filename = 'static/board' + str(i) + '.svg'
            svg_filenames.append(svg_filename)
            with open(svg_filename, 'w') as svg_file:
                svg_file.write(board_svgs[i])

    return render_template('index.html', svg_filenames=svg_filenames, fen=fen, depth=depth, time=time, nodes=nodes)

app.run(debug=True)