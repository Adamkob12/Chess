import numpy as np
from util import *

class Piece():
	def __init__(self, pos, color, name):
		self.pos = pos #0-63
		self.color = color #T/F
		self.name = name # B / Q / R ...
		self.pm = []

	def terminate(self):
		self.pos = -1

	def possible_moves(self, board, pkgd_info): 
		pass

		#  The common dictionary "pkgd_info" is formatted as follows:
		#  {"Last move": self.last_move = [], "WKM" : self.white_king_moved, "BKM":  self.black_king_moved,
		#  "WKR" : self.wkr_moved, "WQR": self.wqr_moved, "BKR" : self.bkr_moved, "BQR" : self.bqr_moved}		

class Pawn(Piece):
	def possible_moves(self, board, pkgd_info):
		if board[self.pos] != (self.color-0.5)*2:
			return []
		pm = []
		if self.color:	
			# first move double
			if 7 < self.pos < 16 and board[self.pos+8]==board[self.pos+16] and board[self.pos+8]==0:
				pm.append([self.pos, self.pos+16])
			# normal one-move ahead
			if 0<=self.pos+8<64 and board[self.pos+8]==0:
				if r(self.pos+8)==8:
					pm.append([self.pos, self.pos+8, 'r'])
					pm.append([self.pos, self.pos+8, 'q'])
					pm.append([self.pos, self.pos+8, 'b'])
					pm.append([self.pos, self.pos+8, 'n'])
				else:
					pm.append([self.pos, self.pos+8])
			# capture right
			if (self.pos+1) % 8 != 0:
				if 0<=self.pos+9<64 and board[self.pos + 9] < 0:
					if r(self.pos+9)==8:
						pm.append([self.pos, self.pos+9, 'r'])
						pm.append([self.pos, self.pos+9, 'q'])
						pm.append([self.pos, self.pos+9, 'b'])
						pm.append([self.pos, self.pos+9, 'n'])
					else:
						pm.append([self.pos, self.pos+9])
				else:
					pm.append([-1, self.pos+9])
				# en-passent
				if board[self.pos+1] == -1 and pkgd_info["Last move"][1] == self.pos+1 and pkgd_info["Last move"][0] - pkgd_info["Last move"][1] == 16:
					pm.append([self.pos, self.pos+9])

			# capture left
			if self.pos % 8 != 0:
				if 0<=self.pos+7<64 and board[self.pos + 7] < 0:
					if r(self.pos+7)==8:
						pm.append([self.pos, self.pos+7, 'r'])
						pm.append([self.pos, self.pos+7, 'q'])
						pm.append([self.pos, self.pos+7, 'b'])
						pm.append([self.pos, self.pos+7, 'n'])
					else:
						pm.append([self.pos, self.pos+7])
				else:
					pm.append([-1, self.pos+7])
				if board[self.pos-1] == -1 and pkgd_info["Last move"][1] == self.pos-1 and pkgd_info["Last move"][0] - pkgd_info["Last move"][1] == 16:
					pm.append([self.pos, self.pos+7])
		else:
			# first move double
			if 47 < self.pos < 56 and board[self.pos-8]==board[self.pos-16] and board[self.pos-8]==0:
				pm.append([self.pos, self.pos-16])
			# normal one-move ahead
			if 0<=self.pos-8<64 and board[self.pos-8]==0:
				if r(self.pos-8)==1:
					pm.append([self.pos, self.pos-8, 'r'])
					pm.append([self.pos, self.pos-8, 'q'])
					pm.append([self.pos, self.pos-8, 'b'])
					pm.append([self.pos, self.pos-8, 'n'])
				else:
					pm.append([self.pos, self.pos-8])
			# capture right
			if self.pos % 8 != 0:
				if 0<=self.pos-9<64 and board[self.pos - 9] > 0:
					if r(self.pos-8)==1:
						pm.append([self.pos, self.pos-9, 'r'])
						pm.append([self.pos, self.pos-9, 'q'])
						pm.append([self.pos, self.pos-9, 'b'])
						pm.append([self.pos, self.pos-9, 'n'])
					else:
						pm.append([self.pos, self.pos-9])
				else:
					pm.append([-1, self.pos-9])
				if board[self.pos-1] == 1 and pkgd_info["Last move"][1] == self.pos-1 and pkgd_info["Last move"][1] - pkgd_info["Last move"][0] == 16:
					pm.append([self.pos, self.pos-9])
			# capture left
			if (self.pos+1) % 8 != 0:
				if 0<=self.pos-7<64 and board[self.pos - 7] > 0:
					if r(self.pos-8)==1:
						pm.append([self.pos, self.pos-7, 'r'])
						pm.append([self.pos, self.pos-7, 'q'])
						pm.append([self.pos, self.pos-7, 'b'])
						pm.append([self.pos, self.pos-7, 'n'])
					else:
						pm.append([self.pos, self.pos-7])
				else:
					pm.append([-1, self.pos-7])
				if -1<self.pos+1<64 and board[self.pos+1] == 1 and pkgd_info["Last move"][1] == self.pos+1 and pkgd_info["Last move"][1] - pkgd_info["Last move"][0] == 16:
					pm.append([self.pos, self.pos-7])
		return pm

class King(Piece):
	def possible_moves(self, board, pkgd_info):
		normal = [[self.pos, i] for i in range(64) if distance(self.pos, i) < 2 and board[i]*(self.color-0.5) <= 0]
		castle = []
		# Castle
		if self.color:
			if not pkgd_info["WKM"] and self.pos == 4:
				if not pkgd_info["WKR"] and board[7] == 5 and board[5]==0 and board[6] == 0:
					castle.append([self.pos, self.pos+2])
				if not pkgd_info["WQR"] and board[0] == 5 and board[1]==0 and board[2] == 0 and board[3] == 0:
					castle.append([self.pos, self.pos-2])
		else:
			if not pkgd_info["BKM"] and self.pos == 60:
				if not pkgd_info["BKR"] and board[63] == -5 and board[62]==0 and board[61] == 0:
					castle.append([self.pos, self.pos+2])
				if not pkgd_info["BQR"] and board[56] == -5 and board[57]==0 and board[58] == 0 and board[59] == 0:
					castle.append([self.pos, self.pos-2])
		return normal + castle
		
class Knight(Piece):
	def possible_moves(self, board, pkgd_info):
		if board[self.pos] != (self.color-0.5)*6:
			return []
		return [[self.pos, i] for i in range(64) if distance(self.pos, i) == 2 and (abs(r(self.pos) - r(i))==1 or abs(f(self.pos) - f(i))==1) and board[i]*(self.color-0.5)<=0]

class Bishop(Piece):
	def possible_moves(self, board, pkgd_info):
		return [[self.pos, i] for i in diagonals_pm(board=board, index=self.pos, color=self.color)]

class Rook(Piece):
	def possible_moves(self, board, pkgd_info):
		return [[self.pos, i] for i in file_rank_pm(board=board, index=self.pos, color=self.color)]
		
class Queen(Piece):
	def possible_moves(self, board, pkgd_info):
		return [[self.pos, i] for i in (file_rank_pm(board=board, index=self.pos, color=self.color) + diagonals_pm(board=board, index=self.pos, color=self.color))]
		