from Board import Board
import random
import numpy as np
from copy import deepcopy
import math

def sigmoid(x):
	return 1 / (1 + math.exp(-x))

class AI():
	def __init__(self):
		pass

class EvolutionModel(AI):
	def __init__(self, Board):
		super().__init__()
		self.Board = Board
		'''
		parameters:
		Board- Board class (definded in Board.py)
		
		This model will recieve several matrices, each will represent different interpetation
		of the board. The genome will be a vector of weights assigned to each matrix. We'll simulate a tournament
		and implement the classic evolution algorithm (Parent1-49%, Parent2-49%, mutation-2%)
		'''
		self.good_squares_to_leave = np.random.rand(64)
		self.good_squares_to_go = np.random.rand(64)

	def weight_move(self, move):
		pass

	def make_move(self, legal_moves):
		max_eval = -100
		move_to_return = []
		for move in legal_moves:
			eval_ = self.evaluate_position(move)
			if eval_ > max_eval:
				max_eval = eval_
				move_to_return = move
		return move_to_return

	def evaluate_position(self, move):
		return random.uniform(-0.1, 0.1)

	def getGenome(self):
		genome = {
			"good_squares_to_leave": self.good_squares_to_leave,
			"good_squares_to_go": self.good_squares_to_go
		}
		return genome

	def combine_genomes(self, other_genome):
		new_genome = EvolutionModel(self.Board)
		mutation_rate = 0.02

		def combine_and_mutate(value1, value2):
			combined_value = value1 * 0.5 + value2 * 0.5
			if random.random() < mutation_rate:
				mutation = random.uniform(-0.1, 0.1)
				return combined_value + mutation
			else:
				return combined_value

		for attr in ["good_squares_to_leave", "good_squares_to_go"]:
			new_genome.__dict__[attr] = np.vectorize(combine_and_mutate)(self.__dict__[attr], other_genome.__dict__[attr])

		return new_genome