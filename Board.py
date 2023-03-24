from Pieces import *
import numpy as np

class Board():
	def __init__(self):
		# PURE OBJECT ARRAY numpy array of len 16, each piece is an object defined in Pieces.py
		# Temp vars for the pieces

		q_R = Rook(0, True, "R")
		q_N = Knight(1, True, "N")
		q_B = Bishop(2, True, "B") 
		Q = Queen(3, True, "Q")
		K = King(4, True, "K")
		k_B = Bishop(5, True, "B") 
		k_N = Knight(6, True, "N")
		k_R = Rook(7, True, "R")

		a_P = Pawn(8 , True, "P")
		b_P = Pawn(9, True, "P")
		c_P = Pawn(10, True, "P")
		d_P = Pawn(11, True, "P")
		e_P = Pawn(12, True, "P")
		f_P = Pawn(13, True, "P")
		g_P = Pawn(14, True, "P")
		h_P = Pawn(15, True, "P")

		q_r = Rook(56, False, "R")
		q_n = Knight(57, False, "N")
		q_b = Bishop(58, False, "B") 
		q  = Queen(59, False, "Q")
		k  = King(60, False, "K")
		k_b = Bishop(61, False, "B") 
		k_n = Knight(62, False, "N")
		k_r = Rook(63, False, "R")

		a_p = Pawn(48, False, "P")
		b_p = Pawn(49, False, "P")
		c_p = Pawn(50, False, "P")
		d_p = Pawn(51, False, "P")
		e_p = Pawn(52, False, "P")
		f_p = Pawn(53, False, "P")
		g_p = Pawn(54, False, "P")
		h_p = Pawn(55, False, "P")

		self.white_pieces = [q_R,q_N,q_B,Q,K,k_B,k_N,k_R,a_P,b_P,c_P,d_P,e_P,f_P,g_P,h_P]
		self.black_pieces = [a_p,b_p,c_p,d_p,e_p,f_p,g_p,h_p,q_r,q_n,q_b,q,k,k_b,k_n,k_r]

		# PURE INT ARRAY numpy array of length 64, standard piece value (sign = color), empty 0, king +-100
		# self.pia[0] = a1, self.pia[63] = h8
		self.pia = [5,3,3.1,9,100,3.1,3,5
			,1,1,1,1,1,1,1,1
			,0,0,0,0,0,0,0,0
			,0,0,0,0,0,0,0,0
			,0,0,0,0,0,0,0,0
			,0,0,0,0,0,0,0,0
			,-1,-1,-1,-1,-1,-1,-1,-1
			,-5,-3,-3.1,-9,-100,-3.1,-3,-5]

		self.turn = True # T/F
		self.last_move = [] # [pos_of_moved_piece, destination]
		self.black_king_moved = False
		self.black_king_pos = 60
		self.white_king_moved = False
		self.white_king_pos = 4
		self.wkr_moved = False
		self.wqr_moved = False
		self.bkr_moved = False
		self.bqr_moved = False
		#  The common dictionary "pkgd_info" is formatted as follows:
		#  {"Last move": self.last_move = [], "WKM" : self.white_king_moved, "BKM":  self.black_king_moved,
		#  "WKR" : self.wkr_moved, "WQR": self.wqr_moved, "BKR" : self.bkr_moved, "BQR" : self.bqr_moved}		

	def toFEN(self):
		pass

	def update_board(self, move):
		# Assuming move is legal.
		for index, piece in enumerate(self.black_pieces+self.white_pieces):
			# if the move is a capture
			if piece.pos == move[1]:
				piece.terminate()
				if index < len(self.black_pieces):
					self.black_pieces.remove(piece)
				else:
					self.white_pieces.remove(piece)

			if piece.pos == move[0]:
				if piece.name == "R":
					if piece.color:
						if piece.pos == 0:
							self.wqr_moved = True
						elif piece.pos == 7:
							self.wkr_moved = True
					else:
						if piece.pos == 63:
							self.bkr_moved = True
						elif piece.pos == 56:
							self.bqr_moved = True

				elif piece.name == "P":
					if self.pia[move[1]] == 0 and f(move[0]) != f(move[1]):
						if piece.color:
							for index, p in enumerate(self.black_pieces):
								if p.pos == move[1] - 8:
									p.terminate()
									self.black_pieces.remove(p)
									self.pia[move[1]-8] = 0
						else:
							for index, p in enumerate(self.white_pieces):
								if p.pos == move[1] + 8:
									p.terminate()
									self.white_pieces.remove(p)
									self.pia[move[1]+8] = 0

				if piece.name == "K":
					if piece.color: 
						self.white_king_pos = move[1]
						self.white_king_moved = True
						if distance(move[0], move[1]) == 2:
							if self.white_king_pos == 6:
								print(1)
								self.update_board([7,5])
							elif self.white_king_pos == 2:
								self.update_board([0,3])
					else: 
						self.black_king_pos = move[1]
						self.black_king_moved = True
						if distance(move[0], move[1]) == 2:
							if self.black_king_pos == 62:
								self.update_board([63,61])
							elif self.black_king_pos == 58:
								self.update_board([56,59])

				piece.pos = move[1]
		self.pia[move[1]] = self.pia[move[0]]
		self.pia[move[0]] = 0
	def LegalMoves(self):
		legal_moves = []
		if self.turn:
			for w_piece in self.white_pieces:
				legal_moves += [move for move in w_piece.possible_moves(self.pia, pkgd_info={"Last move": self.last_move, "WKM": self.white_king_moved, "BKM": self.black_king_moved, "WKR": self.wkr_moved, "WQR": self.wqr_moved, "BKR": self.bkr_moved, "BQR": self.bqr_moved}) if move[0]!=-1 and self.isLegal(move)]
		else:
			for b_piece in self.black_pieces:
				legal_moves += [move for move in b_piece.possible_moves(self.pia, pkgd_info={"Last move": self.last_move, "WKM": self.white_king_moved, "BKM": self.black_king_moved, "WKR": self.wkr_moved, "WQR": self.wqr_moved, "BKR": self.bkr_moved, "BQR": self.bqr_moved}) if move[0]!=-1 and self.isLegal(move)]
		return legal_moves

	def isLegal(self, move):
		if abs(self.pia[move[0]]) == 100:
			if distance(move[0], move[1]) == 2:
				if self.isCheck() or self.isCheck(board=tmp_board(self.pia, [[move[0], move[1] + NOOOOvanish] for NOOOOvanish in [-1,1] if distance(move[0], move[1] + NOOOOvanish) == 1][0])):
					return False
		return not (self.isCheck(board=tmp_board(self.pia, move),last_move=move)==((not self.turn)-0.5)*2)

	def isCheck(self, board=None, last_move=None):
		if board is None:
			board = self.pia
		if last_move is None:
			last_move = self.last_move
		# We want to check if the white pieces are checking black
		for w_piece in self.white_pieces:
			for move in w_piece.possible_moves(board, pkgd_info={"Last move": last_move, "WKM": self.white_king_moved, "BKM": self.black_king_moved, "WKR": self.wkr_moved, "WQR": self.wqr_moved, "BKR": self.bkr_moved, "BQR": self.bqr_moved}):
				if board[move[1]] == -100:
					return 1
		# checking if the black pieces are checking white
		for b_piece in self.black_pieces:
			for move in b_piece.possible_moves(board, pkgd_info={"Last move": last_move, "WKM": self.white_king_moved, "BKM": self.black_king_moved, "WKR": self.wkr_moved, "WQR": self.wqr_moved, "BKR": self.bkr_moved, "BQR": self.bqr_moved}):
				if board[move[1]] == 100:
					return -1
		return 0
