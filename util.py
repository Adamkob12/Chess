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
	a[move[1]] = a[move[0]]
	a[move[0]] = 0
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

def diagonals_pm(index, board, color):
    pm = []

    # Negative diagonal
    for direction in [neg_diag, lambda x: reversed(neg_diag(x))]:
        tmp = []
        passed = False
        for i in direction(index):
            tmp_ = board[i]
            if not passed:
                if tmp_ == 0:
                    tmp.append(i)
                elif tmp_ * (color - 0.5) > 0:
                    if i == index:
                        pm.append(tmp)
                        passed = True
                    tmp = []
                else:
                    tmp = []
                    tmp.append(i)
            else:
                if tmp_ == 0:
                    tmp.append(i)
                else:
                    if tmp_ * (color - 0.5) > 0:
                        pm.append(tmp)
                    else:
                        tmp.append(i)
                        pm.append(tmp)
                    break

    # Positive diagonal
    for direction in [pos_diag, lambda x: reversed(pos_diag(x))]:
        tmp = []
        passed = False
        for j in direction(index):
            tmp_ = board[j]
            if not passed:
                if tmp_ == 0:
                    tmp.append(j)
                elif tmp_ * (color - 0.5) > 0:
                    if j == index:
                        pm.append(tmp)
                        passed = True
                    tmp = []
                else:
                    tmp = []
                    tmp.append(j)
            else:
                if tmp_ == 0:
                    tmp.append(j)
                else:
                    if tmp_ * (color - 0.5) > 0:
                        pm.append(tmp)
                        break
                    else:
                        tmp.append(j)
                        pm.append(tmp)
                        break
    return pm

def file_rank_pm(index, board, color):
    pm = []
    
    # File
    for direction in [file, lambda x: reversed(file(x))]:
        tmp = []
        passed = False
        for i in direction(index):
            tmp_ = board[i]
            if not passed:
                if tmp_ == 0:
                    tmp.append(i)
                elif tmp_*(color-0.5)>0:
                    if i == index:
                        pm.append(tmp)
                        passed = True
                    tmp = []
                else:
                    tmp = []
                    tmp.append(i)
            else:
                if tmp_ == 0:
                    tmp.append(i)
                else:
                    if tmp_*(color-0.5)>0:
                        pm.append(tmp)
                    else:
                        tmp.append(i)
                        pm.append(tmp)
                    break
    # Rank
    for direction in [rank, lambda x: reversed(rank(x))]:
        tmp = []
        passed = False
        for j in direction(index):
            tmp_ = board[j]
            if not passed:
                if tmp_ == 0:
                    tmp.append(j)
                elif tmp_*(color-0.5)>0:
                    if j == index:
                        pm.append(tmp)
                        passed = True
                    tmp = []
                else:
                    tmp = []
                    tmp.append(j)
            else:
                if tmp_ == 0:
                    tmp.append(j)
                else:
                    if tmp_*(color-0.5)>0:
                        pm.append(tmp)
                    else:
                        tmp.append(j)
                        pm.append(tmp)
                    break
    return pm

def isPromotion(board):
	# input: pia
	# If there is a pawn on the last rank, return its index
	for i in range(8):
		if abs(board[i]) == 1: return i
		if abs(board[63-i]) == 1: return 63-i
	return -1