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

# TODO: Add to presentation slide: Since it's a 15 puzzle problem the possible number of states is very large and so
#       majority of the searches in the explored set will result in False. That means all the elements in the set would
#       be checked conventionally. To avoid this I have used the self balancing Red Black BST
class RedBlackTree:
	class Node:
		def __init__(self, key, color='r'):
			self.key = key
			self.parent = None
			self.left = None
			self.right = None
			self.color = color

		def __lt__(self, other):
			return self.key < other.key

		def __le__(self, other):
			return self.__lt__(other)

		def __gt__(self, other):
			return not self.__lt__(other)

		def __ge__(self, other):
			return not self.__lt__(other)

	def __init__(self):
		self.root = None
		self.number_of_nodes = 0

	def add_node(self, key):
		new_node = RedBlackTree.Node(key)
		if self.root is None:
			new_node.color = 'b'
			self.root = new_node
		else:
			cur_node = self.root

			while True:
				if new_node < cur_node:
					if cur_node.left is None:
						cur_node.left = new_node
						new_node.parent = cur_node
						break
					else:
						cur_node = cur_node.left
				else:
					if cur_node.right is None:
						cur_node.right = new_node
						new_node.parent = cur_node
						break
					else:
						cur_node = cur_node.right

			self._balance(new_node)
		self.number_of_nodes += 1

	def exists(self, key):
		cur_node = self.root

		while cur_node is not None:
			if cur_node.key == key: return True
			if key < cur_node.key:
				cur_node = cur_node.left
			else:
				cur_node = cur_node.right

		return False


	def _balance(self, red_node):
		if red_node is self.root:
			red_node.color = 'b'
		elif red_node.color != 'r':
			raise ValueError('Node provided should be coloured red')
		else:
			mother = red_node.parent

			if mother.color == 'r':
				aunt = self._get_sister(mother)
				grandmother = mother.parent

				if aunt is not None and aunt.color == 'r':
					mother.color = 'b'
					if aunt is not None: aunt.color = 'b'
					grandmother.color = 'r'

					self._balance(grandmother)
				else:
					case = np.array(['x', 'x'], dtype=str)
					if grandmother.left is mother:
						case[0] = 'l'
					else:
						case[0] = 'r'
					if mother.left is red_node:
						case[1] = 'l'
					else:
						case[1] = 'r'

					if case[0] == 'l':
						if case[1] == 'r':
							self._rotate_left(mother)
							red_node.color = 'b'
						else:
							mother.color = 'b'

						self._rotate_right(grandmother)
					else:
						if case[1] == 'l':
							self._rotate_right(mother)
							red_node.color = 'b'
						else:
							mother.color = 'b'

						self._rotate_left(grandmother)

					grandmother.color = 'r'

	@staticmethod
	def _get_sister(node):
		if node.parent is None: raise ValueError('Node provided does not have a parent')
		mother = node.parent
		left = mother.left
		right = mother.right

		if left is node: return right
		return left

	def _rotate_left(self, node):
		right = node.right
		if right is None: raise IndexError('Rotate left operation not possible')
		right_left = right.left

		source = node.parent
		if source is not None:
			if source.left is node:
				source.left = right
			else:
				source.right = right
		else:
			self.root = right
		right.parent = node.parent

		right.left = node
		node.parent = right

		node.right = right_left
		if right_left is not None: right_left.parent = node

	def _rotate_right(self, node):
		left = node.left
		if left is None: raise IndexError('Rotate right operation not possible')
		left_right = left.right

		source = node.parent
		if source is not None:
			if source.left is node:
				source.left = left
			else:
				source.right = left
		else:
			self.root = left
		left.parent = node.parent

		left.right = node
		node.parent = left

		node.left = left_right
		if left_right is not None: left_right.parent = node


class _15Puzzle:
	class State:
		def __init__(self, arr):
			self.state = np.array(arr, dtype=str)

		# Following comparison functions will be used to order states in the red black tree
		def __lt__(self, other):
			if not isinstance(other, _15Puzzle.State): raise TypeError

			for i, x in np.ndenumerate(self.state):
				y = other.state[i]
				if x != y: return x < y
			return False

		def __le__(self, other):
			return self.__lt__(other)

		def __gt__(self, other):
			return not self.__lt__(other)

		def __ge__(self, other):
			return not self.__lt__(other)

		def __eq__(self, other):
			return np.array_equal(self.state, other.state)

		def __ne__(self, other):
			return not self.__eq__(other)


	def __init__(self, problem, goal_state):
		# Convert the problem to numpy arrays for lesser memory usage as well as quick operations
		# !! Input is assumed to be correctly formatted in a 2 dimensional array with 4 rows and 4 columns !!
		self.init = _15Puzzle.State(problem)
		self.goal = _15Puzzle.State(goal_state)

		self.zero_location = self._find_zero(self.init.state)
		print(self.zero_location)

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

	@staticmethod
	def _find_zero(state):
		return np.where(state == '0')





# TODO: Delete test function before submitting
def test(initialState, number_of_nodes = 1000):
	init = _15Puzzle.State(initialState)
	reshaped = np.reshape(init.state, 16)

	print('\n\nArrays: ')
	arrays = []
	start = time.time()
	for i in range(0, number_of_nodes):
		np.random.shuffle(reshaped)
		new = _15Puzzle.State(np.reshape(reshaped, (4, 4)).copy())
		if new not in arrays:
			arrays.append(new)
	print(len(arrays), 'nodes generated')
	print(time.time() - start)

	print('\nRBT: ')
	rbt = RedBlackTree()
	start = time.time()
	for i in range(0, number_of_nodes):
		np.random.shuffle(reshaped)
		new = _15Puzzle.State(np.reshape(reshaped, (4, 4)).copy())
		if not rbt.exists(new):
			rbt.add_node(new)
	print(rbt.number_of_nodes, 'nodes generated')
	print(time.time() - start, '\n')





def FindMinimumPath(initialState, goalState):
	minPath = []  # This list should contain the sequence of actions in the optimal solution
	nodesGenerated = 0  # This variable should contain the number of nodes that were generated while finding the optimal solution


	puzzle = _15Puzzle(initialState, goalState)

	# test(initialState)

	return minPath, nodesGenerated


### TODO: !!!!!!!!!!!!!! CHECK BEFORE SUBMISSION !!!!!!!!!!!!!!
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
