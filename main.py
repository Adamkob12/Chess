import pygame as pg
from pygame.locals import *
import sys
import random
from Board import Board
from Pieces import *
import numpy as np
from util import *
import time
import argparse
import chess
import chess.pgn
from render import init_render, draw_everything
import render

OUTPUT_GAME_RECORD_PATH = "games_played\\"

def main():
	global GAME_RECORD
	global White
	global Black
	global RESULT
	global RECORD
	global RENDER
	img_index_to_screenshot = 1

	GAME_RECORD = []
	RESULT = 0
	parser = argparse.ArgumentParser(description='Flags for controlling the game')
	parser.add_argument('--p', type=int, help='USER vs USER , AI vs USER, USER vs AI, AI vs AI (1,2,3,4)')
	parser.add_argument('--r', type=int, help='RECORD GAME OR NOT (0,1)')
	parser.add_argument('--g', type=str, help='PLAY FROM POSITION (FEN)')
	parser.add_argument('--w', type=str, help='TYPE OF AI TO PLAY WHITE')
	parser.add_argument('--b', type=str, help='TYPE OF AI TO PLAY BLACK')
	parser.add_argument('--render', type=int, help='render board? (0,1)')
	args = parser.parse_args()
	
	if not (args.p in [1,2,3,4] and args.r in [0,1] and args.render in [0,1]):
		raise Exception("FlagError found by Argument Parser, flags --p or --r have recieved unexpected values.")
	if not args.render and args.p != 4:
		raise Exception("FlagError found by Argument Parser, must render if User is playing.")
	
	RENDER = True
	RECORD = True

	try:
		if args.p == 2 or args.p == 4:
			White = args.w
		else:
			White = "User"
		if args.p == 3 or args.p == 4:
			Black = args.b
		else:
			Black = "User"
		if args.render:
			init_render()
			RENDER = True
		else: 
			RENDER = False
		RECORD = args.r
	except Exception as e:
		print(f"{e}: unexpected flag values")
	
	while True:
		board = Board()
		run = True
		F = False # position in new_move
		new_move = [-1,-1]
		p = True
		board_test = chess.Board()
		fifty_move_rule = 0
		while run:
			engine_legal_moves = set(board_test.legal_moves)
			engine_legal_moves = [chess.Move.uci(ymove) for ymove in engine_legal_moves]
			my_legal_moves = board.LegalMoves()
			my_legal_moves_uci = [uci_notation(lmove) for lmove in my_legal_moves]
			
			if sorted(engine_legal_moves) == sorted(my_legal_moves_uci):
				new_move = random.sample(my_legal_moves , 1)[0]
				emove = chess.Move.from_uci(uci_notation(new_move))
				board_test.push(emove)
			else:
				run = False
				print("fail")
				print(sorted(engine_legal_moves))
				print(sorted(my_legal_moves_uci))
				game = chess.pgn.Game()
				game.headers["White"] = White
				game.headers["Black"] = Black
				node = game.add_variation(chess.Move.from_uci(GAME_RECORD[0]))
				for i, MOVE in enumerate(GAME_RECORD):
					if not i:
						continue
					node = node.add_variation(chess.Move.from_uci(MOVE))

				if RECORD:
					pg.image.save(render.screen, OUTPUT_GAME_RECORD_PATH + f'screenshot{img_index_to_screenshot}.png')
					img_index_to_screenshot+=1

			if RENDER:
				for event in pg.event.get():
					if event.type==pg.QUIT:
						run = False
					if event.type == pg.MOUSEBUTTONDOWN:
						x, y = pg.mouse.get_pos()
						rank_ = int(((WINDOW_SIZE-y) // SQUARE_SIZE))
						file_ = int((x // SQUARE_SIZE))
						#print(f"rank,{rank_}, file{ file_}")
						new_move[F] = rank_*8+file_
						F = True

			if -1 not in new_move:
				#print([p.possible_moves(board.pia, pkgd_info={"Last move": new_move, "WKM": board.white_king_moved, "BKM": board.black_king_moved, "WKR": board.wkr_moved, "WQR": board.wqr_moved, "BKR": board.bkr_moved, "BQR": board.bqr_moved}) for p in board.white_pieces if p.name == "P"])
				#tmp_p = [p.possible_moves(board.pia, pkgd_info={"Last move": new_move, "WKM": board.white_king_moved, "BKM": board.black_king_moved, "WKR": board.wkr_moved, "WQR": board.wqr_moved, "BKR": board.bkr_moved, "BQR": board.bqr_moved}) for p in board.black_pieces if p.name == "B"]
				#print([[move_, board.isCheck(board=tmp_board(board.pia, move_),last_move=move_)] for flatten_ in tmp_p for move_ in flatten_])
				if new_move in board.LegalMoves():
					fifty_move_rule+=1
					if abs(board.pia[new_move[0]]) == 1 or board.pia[new_move[1]] != 0:
						fifty_move_rule = 0
					board.update_board(move=new_move)
					emove = chess.Move.from_uci(uci_notation(new_move))
					GAME_RECORD.append(uci_notation(new_move))
					board.turn = not board.turn
					board.last_move = new_move
					F = False

					if len(new_move) == 3:
						i = new_move[1]
						if new_move[2] == 'q':
							tmp_piece = Queen(pos=i , color=(i>10) , name="Q")
						if new_move[2] == 'r':
							tmp_piece = Rook(pos=i , color=(i>10) , name="R")
						if new_move[2] == 'n':
							tmp_piece = Knight(pos=i , color=(i>10) , name="N")
						if new_move[2] == 'b':
							tmp_piece = Bishop(pos=i , color=(i>10) , name="B")
						if i>10:
							for piece_to_promote in board.white_pieces:
								if piece_to_promote.pos == i:
									piece_to_promote.terminate()
									board.white_pieces.remove(piece_to_promote)
							board.white_pieces.append(tmp_piece)
							board.pia[i] = {"q":9,"r":5,"n":3,"b":3.1}[new_move[2]]
						else:
							for piece_to_promote in board.black_pieces:
								if piece_to_promote.pos == i:
									piece_to_promote.terminate()
									board.black_pieces.remove(piece_to_promote)
							board.black_pieces.append(tmp_piece)
							board.pia[i] = {"q":9,"r":5,"n":3,"b":3.1}[new_move[2]] * -1


					#print([wpawn.pos for wpawn in board.white_pieces if wpawn.name == "P"])
					#print([bpawn.pos for bpawn in board.black_pieces if bpawn.name == "P"])
				else:
					F = False
				new_move = [-1,-1]

			
			# Draw everything
			if RENDER:
				draw_everything(board.pia)
			# Check if game ended
			if len(board.LegalMoves()) == 0:
				if board.isCheck():
					print("~~~~~~~~~~~~~~~~~")
					print("    CHECKMATE    ")
					print("~~~~~~~~~~~~~~~~~")
					RESULT = board.isCheck()
				else:
					print("~~~~~~~~~~~~~~~~~")
					print("    STALEMATE    ")
					print("~~~~~~~~~~~~~~~~~")
					RESULT = 0
				run = False
			if fifty_move_rule>=50:
				RESULT = 0
				print("~~~~~~~~~~~~~~~~~")
				print("       DRAW      ")
				print("~~~~~~~~~~~~~~~~~")
				run = False	
		
if __name__ == '__main__':
	main()

if RESULT == 1:
	RESULT = "1-0"
elif RESULT == -1:
	RESULT = "0-1"
else:
	RESULT="0.5-0.5"

game = chess.pgn.Game()
game.headers["White"] = White
game.headers["Black"] = Black
game.headers["Result"] = RESULT
node = game.add_variation(chess.Move.from_uci(GAME_RECORD[0]))
for i, MOVE in enumerate(GAME_RECORD):
	if not i:
		continue
	node = node.add_variation(chess.Move.from_uci(MOVE))

if RECORD:
	f = open(OUTPUT_GAME_RECORD_PATH + "game_dataset1.pgn", "a")
	f.write(str(game) + "\n\n")
	f.close()