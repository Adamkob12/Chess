from util import r, f, rank, file, neg_diag, pos_diag, tmp_board
from Board import Board
b = Board()

while True:
	print(tmp_board(b.pia, [int(input()), int(input())]))

