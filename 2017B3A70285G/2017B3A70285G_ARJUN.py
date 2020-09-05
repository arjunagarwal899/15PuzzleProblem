#!/usr/bin/env python3
import time
import numpy as np
from heapq import *  # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************

from enum import Enum  # Imported built-in "enum.Enum" class for declaring enumerations


# An enumeration for storing the possible moves that can be made in the 15 Puzzle Problem
class Moves(Enum):
	UP = 'UP'
	DOWN = 'DOWN'
	LEFT = 'LEFT'
	RIGHT = 'RIGHT'


class _15Puzzle:

	def __init__(self, problem, goal_state):
		# Create two copies of the problem given and store it as initial state as well as current state
		self.init_state = problem[:]
		self.cur_state = problem[:]
		self.goal_state = goal_state
		self.zero_location = self._find_zero()
		pass

	def solve(self):
		pass

	def move(self, direction):
		if direction is Moves.UP:
			new_state = self._move_up_state()
			pass
		elif direction is Moves.DOWN:
			new_state = self._move_down_state()
			pass
		elif direction is Moves.LEFT:
			new_state = self._move_left_state()
			pass
		elif direction is Moves.RIGHT:
			new_state = self._move_right_state()
			pass

	def get_possible_moves(self):
		pass

	def get_possible_next_states(self):
		possible_next_states = np.array([], ndmin=3)
		possible_moves = self.get_possible_moves()

		for possible_move in possible_moves:
			if possible_move is Moves.UP:
				np.append(possible_next_states, self._move_up_state(), axis=0)
			elif possible_move is Moves.DOWN:
				np.append(possible_next_states, self._move_down_state(), axis=0)
			elif possible_move is Moves.LEFT:
				np.append(possible_next_states, self._move_left_state(), axis=0)
			elif possible_move is Moves.RIGHT:
				np.append(possible_next_states, self._move_right_state(), axis=0)

		return possible_next_states


	def _move_up_state(self):
		pass

	def _move_down_state(self):
		pass

	def _move_left_state(self):
		pass

	def _move_right_state(self):
		pass

	def _find_zero(self):
		pass


def FindMinimumPath(initialState, goalState):
	minPath = []  # This list should contain the sequence of actions in the optimal solution
	nodesGenerated = 0  # This variable should contain the number of nodes that were generated while finding the optimal solution

	### Your Code for FindMinimumPath function
	### Write your program in an easy to read manner. You may use several classes and functions.
	### Your function names should indicate what they are doing

	puzzle = _15Puzzle(initialState, goalState)

	### Your Code ends here. minPath is a list that contains actions.
	### For example, minPath = ['Up','Right','Down','Down','Left']

	return minPath, nodesGenerated


### TODO: !!!!!!!!!!!!!! CHECK BEFORE SUBMISSION !!!!!!!!!!!!
# **************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
	# TODO: CHANGE BEFORE SUBMISSION
	with open("initial_state4.txt", "r") as file:  # IMP: If you change the file name, then there will be an error when
		#               evaluators test your program. You will lose 2 marks.
		initialState = [[x for x in line.split()] for i, line in enumerate(file) if i < 4]
	return initialState


def ShowState(state, heading=''):
	print(heading)
	for row in state:
		print(*row, sep=" ")


def main():
	initialState = ReadInitialState()
	ShowState(initialState, 'Initial state:')
	goalState = [['0', '1', '2', '3'], ['4', '5', '6', '7'], ['8', '9', 'A', 'B'], ['C', 'D', 'E', 'F']]
	ShowState(goalState, 'Goal state:')

	start = time.time()
	minimumPath, nodesGenerated = FindMinimumPath(initialState, goalState)
	timeTaken = time.time() - start

	if len(minimumPath) == 0:
		minimumPath = ['Up', 'Right', 'Down', 'Down', 'Left']
		print('Example output:')
	else:
		print('Output:')

	print('   Minimum path cost : {0}'.format(len(minimumPath)))
	print('   Actions in minimum path : {0}'.format(minimumPath))
	print('   Nodes generated : {0}'.format(nodesGenerated))
	# print('   Time taken : {0} s'.format(round(timeTaken, 4)))    # TODO: CHANGE BEFORE SUBMISSION
	print('   Time taken : {0} s'.format(timeTaken))  # TODO: CHANGE BEFORE SUBMISSION


if __name__ == '__main__':
	main()
