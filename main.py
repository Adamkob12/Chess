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
				print(f"rank,{rank_}, file{ file_}")
				new_move[F] = rank_*8+file_
				F = True

		if -1 not in new_move:
			print(board.LegalMoves())
			if new_move in board.LegalMoves():
				board.update_board(move=new_move)
				print(new_move)
				board.turn = not board.turn
				print(board.isCheck())
				F = False
				new_move = [-1,-1]
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