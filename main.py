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
from AI import EvolutionModel

OUTPUT_GAME_RECORD_PATH = "games_played\\"

def main():
	global GAME_RECORD
	global White
	global Black
	global RESULT
	global RECORD
	global RENDER
	global White_Bot
	global Black_Bot
	global NODRAW
 
	GAME_RECORD = []
	RESULT = 0
	parser = argparse.ArgumentParser(description='Flags for controlling the game')
	parser.add_argument('--p', type=int, help='USER vs USER , AI vs USER, USER vs AI, AI vs AI (1,2,3,4)')
	parser.add_argument('--r', type=int, help='RECORD GAME OR NOT (0,1)')
	parser.add_argument('--g', type=str, help='PLAY FROM POSITION (FEN)')
	parser.add_argument('--w', type=str, help='TYPE OF AI TO PLAY WHITE')
	parser.add_argument('--b', type=str, help='TYPE OF AI TO PLAY BLACK')
	parser.add_argument('--render', type=int, help='render board? (0,1)')
	parser.add_argument('--nodraw', type=int, help='1- Dont record draw (tie) 0/Nothing- record draw')
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
		if bool(args.render):
			init_render()
			RENDER = True
		else: 
			RENDER = False
		NODRAW = bool(args.nodraw)
		RECORD = args.r
	except Exception as e:
		print(f"{e}: unexpected flag values")
		return 0

	 # The Board.
	board = Board()
	Legal_Moves_arr = board.LegalMoves()
	if White == None:
		White = "AI"
		White_Bot = EvolutionModel(board)
	if Black == None:
		Black_Bot = EvolutionModel(board)
		Black = "AI"

	run = True # Continue running the game.
	F = False # position in new_move array (T=1,F=0)
	new_move = [-1,-1] # The next that will be played. 
	p = True # Don't know what this variable does, afraid to del.
	fifty_move_rule = 0 # Counts moves untill draw by 50 move rule
	get_from_screen = True # Get the next move from screen (mouse)
	count = 0
	while run:
		# Get white's move
		if board.turn:
			if White == "AI":
				new_move = White_Bot.make_move(legal_moves=Legal_Moves_arr)
				get_from_screen = False
			else:
				get_from_screen = True
		else:
			if Black == "AI":
				new_move = Black_Bot.make_move(legal_moves=Legal_Moves_arr)
				get_from_screen = False
			else:
				get_from_screen = True

		if RENDER and get_from_screen:
			for event in pg.event.get():
				if event.type==pg.QUIT:
					run = False
				if event.type == pg.MOUSEBUTTONDOWN:
					x, y = pg.mouse.get_pos()
					rank_ = int(((render.WINDOW_SIZE-y) // render.SQUARE_SIZE))
					file_ = int((x // render.SQUARE_SIZE))
					#print(f"rank,{rank_}, file{ file_}")
					new_move[F] = rank_*8+file_
					F = True

		# Found move, will check if it is legal.
		if -1 not in new_move:
			# Checks if move is legal.
			if new_move in Legal_Moves_arr:
				fifty_move_rule+=1
				if abs(board.pia[new_move[0]]) == 1 or board.pia[new_move[1]] != 0:
					fifty_move_rule = 0
				board.update_board(move=new_move)
				count=0
				GAME_RECORD.append(uci_notation(new_move))
				board.turn = not board.turn
				board.last_move = new_move
				F = False

				# Check Promotion
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
						for index, piece_to_promote in enumerate(board.white_pieces):
							if piece_to_promote == None:
								continue
							if piece_to_promote.pos == i:
								piece_to_promote.terminate()
								board.white_pieces[index] = None
						board.white_pieces.append(tmp_piece)
						board.pia[i] = {"q":9,"r":5,"n":3,"b":3.1}[new_move[2]]
					else:
						for index, piece_to_promote in enumerate(board.black_pieces):
							if piece_to_promote == None:
								continue
							if piece_to_promote.pos == i:
								piece_to_promote.terminate()
								board.black_pieces[index] = None
						board.black_pieces.append(tmp_piece)
						board.pia[i] = {"q":9,"r":5,"n":3,"b":3.1}[new_move[2]] * -1

			# move is illegal.			
			else:
				F = False
			new_move = [-1,-1]

		# Draw everything
		if RENDER:
			draw_everything(board.pia)

		# Check if game ended
		Legal_Moves_arr = board.LegalMoves()
		if len(Legal_Moves_arr) == 0:
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
			return RESULT

		if fifty_move_rule>=50:
			RESULT = 0
			print("~~~~~~~~~~~~~~~~~")
			print("       DRAW      ")
			print("~~~~~~~~~~~~~~~~~")
			return RESULT	
		
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

if RECORD and not (NODRAW and RESULT=="0.5-0.5"):
	f = open(OUTPUT_GAME_RECORD_PATH + "game_dataset1.pgn", "a")
	#f.write(str(game) + "\n\n")
	if White == "AI" and not RESULT=="0-1":
		w_genome = White_Bot.getGenome()
		f.write(str(w_genome["good_squares_to_leave"])+","+ str(w_genome["good_squares_to_go"])+","+str(w_genome["capture_weight"])+","+str(w_genome["check_weight"])+"\n")
	if Black == "AI" and not RESULT=="1-0":
		b_genome = Black_Bot.getGenome()
		f.write(str(b_genome["good_squares_to_leave"])+","+ str(b_genome["good_squares_to_go"])+","+str(b_genome["capture_weight"])+","+str(b_genome["check_weight"])+"\n")
	
	f.close()