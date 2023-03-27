import pygame as pg
import sys
import random
from Pieces import *
import numpy as np

def r(index): return (index // 8) + 1

def f(index): return (index % 8) + 1

def tmp_board(board, move):
	# recieves pia, returns pia, doesn't chagnge inner vars of Board class for temp reasons.
	a = board.copy()
	if board[move[0]]==1 and board[move[1]] == 0 and f(move[0]) != f(move[1]):
		a[move[1]-8] = 0
	elif board[move[0]]==-1 and board[move[1]] == 0 and f(move[0]) != f(move[1]):
		a[move[1]+8] = 0
	a[move[1]] = a[move[0]]
	a[move[0]] = 0
	'''if len(move) == 3:
					i = move[1]
					a[i] = {"q":9,"r":5,"n":3,"b":3.1}[move[2]] * ((i>10)-0.5)*2'''
	return a

def distance(a, b):
	# returns distance in a chess board between 2 squares.
	return max(abs(r(b)-r(a)), abs(f(b)-f(a)))

def neg_diag(index):
	# returns array of the indexes in the same negetive diagonal (TL->BR)
	g = r(index)+ f(index)
	return [i for i in range(64) if r(i) + f(i) == g]

def pos_diag(index):
	# ' 		'		 '	(BL->TR)    
	g = r(index)- f(index)
	return [i for i in range(64) if r(i) - f(i) == g]

def rank(index):
	# returns array of all the indexes in the same rank
	g = r(index)
	return [i for i in range(64) if r(i) == g]

def file(index):
	# returns array ` 		` 		`		`	file
	g = f(index)
	return [i for i in range(64) if f(i) == g]

def uci_notation(move):
	# recieves array of len 2 with index of pia array.
	m = ""
	num_to_letter = ['a','b','c','d','e','f','g','h']
	m+=f"{num_to_letter[f(move[0])-1]}{r(move[0])}"
	m+=f"{num_to_letter[f(move[1])-1]}{r(move[1])}"
	if len(move) == 3:
		m+=move[2]
	return m

def diagonals_pm(index, board, color):
	moves = []
	piece = board[index]
	row, col = index // 8, index % 8

	# Check if the piece is a valid diagonally moving piece (bishop or queen)
	if abs(piece) not in [3.1, 9]:
		return moves

	# Check moves in four diagonal directions: up-left, up-right, down-left, down-right
	directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
	for dr, dc in directions:
		r, c = row + dr, col + dc
		while 0 <= r < 8 and 0 <= c < 8:
			target = board[r * 8 + c]

			# If the target square is empty, the piece can move there
			if target == 0:
				moves.append(r * 8 + c)
			else:
				# If the target square has an opposing piece, the piece can capture it
				if piece * target < 0:
					moves.append(r * 8 + c)
				# In any case, the piece cannot continue moving in this direction
				break

			# Continue in the same direction
			r += dr
			c += dc
	return moves

def file_rank_pm(index, board, color):
	moves = []
	piece = board[index]
	row, col = index // 8, index % 8

	# Check if the piece is a valid horizontally and vertically moving piece (rook or queen)
	if abs(piece) not in [5, 9]:
		return moves

	# Check moves in four directions: up, down, left, and right
	directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
	for dr, dc in directions:
		r, c = row + dr, col + dc
		while 0 <= r < 8 and 0 <= c < 8:
			target = board[r * 8 + c]

			# If the target square is empty, the piece can move there
			if target == 0:
				moves.append(r * 8 + c)
			else:
				# If the target square has an opposing piece, the piece can capture it
				if piece * target < 0:
					moves.append(r * 8 + c)
				# In any case, the piece cannot continue moving in this direction
				break

			# Continue in the same direction
			r += dr
			c += dc

	return moves

def isPromotion(board):
	# input: pia
	# If there is a pawn on the last rank, return its index
	for i in range(8):
		if abs(board[i]) == 1: return i
		if abs(board[63-i]) == 1: return 63-i
	return -1