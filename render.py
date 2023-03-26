import pygame as pg
from util import f,r

WINDOW_SIZE = 468
screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
board_img = pg.transform.scale(pg.image.load('assets\\used_assets\\' + "chessboard2.png").convert_alpha(), (468, 468))
def init_render():
	pg.init()

	global screen
	global PATH
	global WINDOW_SIZE
	global SQUARE_SIZE
	global FACTOR_OF_REDUCTION
	global clock
	global board_img
	global img_P
	global img_R
	global img_N
	global img_B
	global img_Q
	global img_K
	global img_p
	global img_r
	global img_n
	global img_b
	global img_q
	global img_k
	global STANDARD_BLIT_SPACER
	global PIECE_VALUE_TO_IMG_MATCH

	PATH = 'assets\\used_assets\\'
	WINDOW_SIZE = 468
	screen = pg.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
	SQUARE_SIZE = WINDOW_SIZE / 8
	FACTOR_OF_REDUCTION = 0.95
	clock = pg.time.Clock()
	board_img = pg.transform.scale(pg.image.load(PATH + "chessboard2.png").convert_alpha(), (WINDOW_SIZE, WINDOW_SIZE))
	img_P = pg.transform.scale(pg.image.load(PATH + "P_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_R = pg.transform.scale(pg.image.load(PATH + "R_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_N = pg.transform.scale(pg.image.load(PATH + "N_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_B = pg.transform.scale(pg.image.load(PATH + "B_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_Q = pg.transform.scale(pg.image.load(PATH + "Q_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_K = pg.transform.scale(pg.image.load(PATH + "K_.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_p = pg.transform.scale(pg.image.load(PATH + "p.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_r = pg.transform.scale(pg.image.load(PATH + "r.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_n = pg.transform.scale(pg.image.load(PATH + "n.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_b = pg.transform.scale(pg.image.load(PATH + "b.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_q = pg.transform.scale(pg.image.load(PATH + "q.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	img_k = pg.transform.scale(pg.image.load(PATH + "k.png").convert_alpha(), (SQUARE_SIZE*FACTOR_OF_REDUCTION, SQUARE_SIZE*FACTOR_OF_REDUCTION))
	STANDARD_BLIT_SPACER = 2
	PIECE_VALUE_TO_IMG_MATCH = {1.0:img_P, 3.0:img_N, 3.1:img_B, 5.0:img_R,9.0:img_Q,100.0:img_K,
								-1.0:img_p,-3.0:img_n,-3.1:img_b,-5.0:img_r,-9.0:img_q,-100.0:img_k}

def draw_everything(board):
	# recieves pia, draws everything including board
	screen.blit(board_img, (0,0))
	for index, piece in enumerate(board):
		if piece!=0:
			screen.blit(PIECE_VALUE_TO_IMG_MATCH[piece], ((f(index)-1) *SQUARE_SIZE + STANDARD_BLIT_SPACER,(8-r(index)) * SQUARE_SIZE + STANDARD_BLIT_SPACER ))
	pg.display.update()