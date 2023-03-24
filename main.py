import pygame as pg
from pygame.locals import *
import sys
import random
from Board import Board
from Pieces import *
import numpy as np
from util import *
import time

path = 'assets\\used_assets\\'
WINDOW_SIZE = 1024
SQUARE_SIZE = WINDOW_SIZE / 8
FACTOR_OF_REDUCTION = 0.9
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pg.time.Clock()

board_img = pg.image.load(path + "chessboard2.png").convert_alpha()

img_P = pg.transform.scale(pg.image.load(path + "P_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_R = pg.transform.scale(pg.image.load(path + "R_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_N = pg.transform.scale(pg.image.load(path + "N_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_B = pg.transform.scale(pg.image.load(path + "B_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_Q = pg.transform.scale(pg.image.load(path + "Q_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_K = pg.transform.scale(pg.image.load(path + "K_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_p = pg.transform.scale(pg.image.load(path + "p.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_r = pg.transform.scale(pg.image.load(path + "r.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_n = pg.transform.scale(pg.image.load(path + "n.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_b = pg.transform.scale(pg.image.load(path + "b.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_q = pg.transform.scale(pg.image.load(path + "q.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
img_k = pg.transform.scale(pg.image.load(path + "k.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))

STANDARD_BLIT_SPACER = 8
PIECE_VALUE_TO_IMG_MATCH = {1.0:img_P, 3.0:img_N, 3.1:img_B, 5.0:img_R,9.0:img_Q,100.0:img_K,
							-1.0:img_p,-3.0:img_n,-3.1:img_b,-5.0:img_r,-9.0:img_q,-100.0:img_k}

def draw_everything(board):
	# recieves pia, draws everything including board
	screen.blit(board_img, (0,0))
	for index, piece in enumerate(board):
		if piece!=0:
			screen.blit(PIECE_VALUE_TO_IMG_MATCH[piece], ((f(index)-1) *SQUARE_SIZE + STANDARD_BLIT_SPACER,(8-r(index)) * SQUARE_SIZE + STANDARD_BLIT_SPACER ))
	pg.display.update()

def main():
	board = Board()
	run = True
	F = False # position in new_move
	new_move = [-1,-1]

	while run:
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
			print(new_move)
			#print([p.possible_moves(board.pia, pkgd_info={"Last move": new_move, "WKM": board.white_king_moved, "BKM": board.black_king_moved, "WKR": board.wkr_moved, "WQR": board.wqr_moved, "BKR": board.bkr_moved, "BQR": board.bqr_moved}) for p in board.white_pieces if p.name == "P"])
			#tmp_p = [p.possible_moves(board.pia, pkgd_info={"Last move": new_move, "WKM": board.white_king_moved, "BKM": board.black_king_moved, "WKR": board.wkr_moved, "WQR": board.wqr_moved, "BKR": board.bkr_moved, "BQR": board.bqr_moved}) for p in board.black_pieces if p.name == "B"]
			#print([[move_, board.isCheck(board=tmp_board(board.pia, move_),last_move=move_)] for flatten_ in tmp_p for move_ in flatten_])
			if new_move in board.LegalMoves():
				board.update_board(move=new_move)
				board.turn = not board.turn
				board.last_move = new_move
				F = False
				new_move = [-1,-1]

				i = isPromotion(board.pia)
				if i != -1:
					tmp_queen = Queen(pos=i , color=(i>10) , name="Q")
					if i>10:
						for piece_to_promote in board.white_pieces:
							if piece_to_promote.pos == i:
								piece_to_promote.terminate()
								board.white_pieces.remove(piece_to_promote)
						board.white_pieces.append(tmp_queen)
						board.pia[i] = 9
					else:
						for piece_to_promote in board.black_pieces:
							if piece_to_promote.pos == i:
								piece_to_promote.terminate()
								board.black_pieces.remove(piece_to_promote)
						board.black_pieces.append(tmp_queen)
						board.pia[i] = -9

				#print([wpawn.pos for wpawn in board.white_pieces if wpawn.name == "P"])
				#print([bpawn.pos for bpawn in board.black_pieces if bpawn.name == "P"])
			else:
				new_move = [-1,-1]
				F = False

		draw_everything(board.pia) # Draw everything
		# Check if the game is over
	
		clock.tick(10)
		
if __name__ == '__main__':
	pg.init()
	main()
	sys.exit()