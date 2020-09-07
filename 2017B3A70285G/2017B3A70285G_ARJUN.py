#!/usr/bin/env python3
import time
import numpy as np
from heapq import *  # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************

from enum import Enum  # Imported built-in "enum.Enum" class for declaring enumerations


# TODO: Add to presentation slide: Since it's a 15 puzzle problem the possible number of states is very large and so
#       majority of the searches in the explored set will result in False. That means all the elements in the set would
#       be checked conventionally. To avoid this I have used the self balancing Red Black BST
# class RedBlackTree:
# 	class Node:
# 		def __init__(self, key, color='r'):
# 			self.key = key
# 			self.parent = None
# 			self.left = None
# 			self.right = None
# 			self.color = color
#
# 		def __lt__(self, other):
# 			return self.key < other.key
#
# 		def __le__(self, other):
# 			return self.__lt__(other)
#
# 		def __gt__(self, other):
# 			return not self.__lt__(other)
#
# 		def __ge__(self, other):
# 			return not self.__lt__(other)
#
# 	def __init__(self):
# 		self.root = None
# 		self.number_of_nodes = 0
#
# 	def add_node(self, key):
# 		new_node = RedBlackTree.Node(key)
# 		if self.root is None:
# 			new_node.color = 'b'
# 			self.root = new_node
# 		else:
# 			cur_node = self.root
#
# 			while True:
# 				if new_node < cur_node:
# 					if cur_node.left is None:
# 						cur_node.left = new_node
# 						new_node.parent = cur_node
# 						break
# 					else:
# 						cur_node = cur_node.left
# 				else:
# 					if cur_node.right is None:
# 						cur_node.right = new_node
# 						new_node.parent = cur_node
# 						break
# 					else:
# 						cur_node = cur_node.right
#
# 			self._balance(new_node)
# 		self.number_of_nodes += 1
#
# 	def exists(self, key):
# 		cur_node = self.root
#
# 		while cur_node is not None:
# 			if cur_node.key == key: return True
# 			if key < cur_node.key:
# 				cur_node = cur_node.left
# 			else:
# 				cur_node = cur_node.right
#
# 		return False
#
#
# 	def _balance(self, red_node):
# 		if red_node is self.root:
# 			red_node.color = 'b'
# 		elif red_node.color != 'r':
# 			raise ValueError('Node provided should be coloured red')
# 		else:
# 			mother = red_node.parent
#
# 			if mother.color == 'r':
# 				aunt = self._get_sister(mother)
# 				grandmother = mother.parent
#
# 				if aunt is not None and aunt.color == 'r':
# 					mother.color = 'b'
# 					if aunt is not None: aunt.color = 'b'
# 					grandmother.color = 'r'
#
# 					self._balance(grandmother)
# 				else:
# 					case = np.array(['x', 'x'], dtype=str)
# 					if grandmother.left is mother:
# 						case[0] = 'l'
# 					else:
# 						case[0] = 'r'
# 					if mother.left is red_node:
# 						case[1] = 'l'
# 					else:
# 						case[1] = 'r'
#
# 					if case[0] == 'l':
# 						if case[1] == 'r':
# 							self._rotate_left(mother)
# 							red_node.color = 'b'
# 						else:
# 							mother.color = 'b'
#
# 						self._rotate_right(grandmother)
# 					else:
# 						if case[1] == 'l':
# 							self._rotate_right(mother)
# 							red_node.color = 'b'
# 						else:
# 							mother.color = 'b'
#
# 						self._rotate_left(grandmother)
#
# 					grandmother.color = 'r'
#
# 	@staticmethod
# 	def _get_sister(node):
# 		if node.parent is None: raise ValueError('Node provided does not have a parent')
# 		mother = node.parent
# 		left = mother.left
# 		right = mother.right
#
# 		if left is node: return right
# 		return left
#
# 	def _rotate_left(self, node):
# 		rightChild = node.right
# 		if rightChild is None: raise IndexError('Rotate left operation not possible')
# 		rightLeftGrandchild = rightChild.left
#
# 		source = node.parent
# 		if source is not None:
# 			if source.left is node:
# 				source.left = rightChild
# 			else:
# 				source.right = rightChild
# 		else:
# 			self.root = rightChild
# 		rightChild.parent = node.parent
#
# 		rightChild.left = node
# 		node.parent = rightChild
#
# 		node.right = rightLeftGrandchild
# 		if rightLeftGrandchild is not None: rightLeftGrandchild.parent = node
#
# 	def _rotate_right(self, node):
# 		leftChild = node.left
# 		if leftChild is None: raise IndexError('Rotate right operation not possible')
# 		leftRightGrandchild = leftChild.right
#
# 		source = node.parent
# 		if source is not None:
# 			if source.left is node:
# 				source.left = leftChild
# 			else:
# 				source.right = leftChild
# 		else:
# 			self.root = leftChild
# 		leftChild.parent = node.parent
#
# 		leftChild.right = node
# 		node.parent = leftChild
#
# 		node.left = leftRightGrandchild
# 		if leftRightGrandchild is not None: leftRightGrandchild.parent = node


class _15Puzzle:
	# An enumeration for storing the possible moves that can be made in the 15 Puzzle Problem
	class Moves(Enum):
		UP = 'UP'
		DOWN = 'DOWN'
		LEFT = 'LEFT'
		RIGHT = 'RIGHT'


	class State:
		def __init__(self, arr, zero_location=None):
			self.layout = np.array(arr, dtype=str)

			if zero_location is None: zero_location = self._find_zero()
			self.zero_location = zero_location

		# TODO: To optimize further, think of an ordering function which does not require a lot of rotations during
		#       insertions (consider the moves that are taken, most of the places don't change)
		def __lt__(self, other):
			if not isinstance(other, _15Puzzle.State): raise TypeError

			for i, x in np.ndenumerate(self.layout):
				y = other.layout[i]
				if x != y: return x < y
			return False

		def __hash__(self):
			return hash(self.layout.tobytes())

		def __le__(self, other):
			return self.__lt__(other)

		def __gt__(self, other):
			return not self.__lt__(other)

		def __ge__(self, other):
			return not self.__lt__(other)

		def __eq__(self, other):
			return np.array_equal(self.layout, other.layout)

		def __ne__(self, other):
			return not self.__eq__(other)

		def __str__(self):
			return str(self.layout)

		def get_possible_moves(self):
			possible_moves = []
			if self.zero_location[0] > 0: possible_moves.append(_15Puzzle.Moves.DOWN)
			if self.zero_location[0] < 3: possible_moves.append(_15Puzzle.Moves.UP)
			if self.zero_location[1] > 0: possible_moves.append(_15Puzzle.Moves.RIGHT)
			if self.zero_location[1] < 3: possible_moves.append(_15Puzzle.Moves.LEFT)

			return possible_moves

		def get_possible_next_states(self):
			possible_next_states = {}

			for direction in self.get_possible_moves():
				possible_next_states[direction] = self._move(direction)

			return possible_next_states

		def _move(self, direction):
			if direction is _15Puzzle.Moves.UP:
				return self._move_up()
			elif direction is _15Puzzle.Moves.DOWN:
				return self._move_down()
			elif direction is _15Puzzle.Moves.LEFT:
				return self._move_left()
			elif direction is _15Puzzle.Moves.RIGHT:
				return self._move_right()

			raise TypeError


		def _move_left(self):
			if self.zero_location[1] == 3: raise IndexError('Cannot move left in the puzzle')

			new_layout = self.layout.copy()
			zl = self.zero_location
			new_layout[zl[0], (zl[1], zl[1] + 1)] = new_layout[zl[0], (zl[1] + 1, zl[1])]  # swap the elements

			return _15Puzzle.State(new_layout, (zl[0], zl[1] + 1))

		def _move_right(self):
			if self.zero_location[1] == 0: raise IndexError('Cannot move right in the puzzle')

			new_layout = self.layout.copy()
			zl = self.zero_location
			new_layout[zl[0], (zl[1] - 1, zl[1])] = new_layout[zl[0], (zl[1], zl[1] - 1)]  # swap the elements

			return _15Puzzle.State(new_layout, (zl[0], zl[1] - 1))

		def _move_up(self):
			if self.zero_location[0] == 3: raise IndexError('Cannot move up in the puzzle')

			new_layout = self.layout.copy()
			zl = self.zero_location
			new_layout[(zl[0], zl[0] + 1), zl[1]] = new_layout[(zl[0] + 1, zl[0]), zl[1]]  # swap the elements

			return _15Puzzle.State(new_layout, (zl[0] + 1, zl[1]))

		def _move_down(self):
			if self.zero_location[0] == 0: raise IndexError('Cannot move down in the puzzle')

			new_layout = self.layout.copy()
			zl = self.zero_location
			new_layout[(zl[0] - 1, zl[0]), zl[1]] = new_layout[(zl[0], zl[0] - 1), zl[1]]  # swap the elements

			return _15Puzzle.State(new_layout, (zl[0] - 1, zl[1]))

		def _find_zero(self):
			loc = np.where(self.layout == '0')
			return loc[0][0], loc[1][0]


	def __init__(self, problem, goal_state):
		# Converts the problem to numpy arrays for lesser memory usage as well as quick operations
		# !! Input is assumed to be correctly formatted in a 2 dimensional array with 4 rows and 4 columns !!
		self.init_state = _15Puzzle.State(problem)
		self.goal_state = _15Puzzle.State(goal_state)

	def solve(self):
		return self._a_star('MD')

	def _a_star(self, heuristic='PD'):
		min_path = []
		nodes_generated = 0

		def get_char_from_direction(direction):
			if direction is _15Puzzle.Moves.UP:
				return 'u'
			if direction is _15Puzzle.Moves.DOWN:
				return 'd'
			if direction is _15Puzzle.Moves.LEFT:
				return 'l'
			if direction is _15Puzzle.Moves.RIGHT:
				return 'r'

			raise TypeError('Provided direction is not a valid move')

		def get_direction_from_char(char):
			if char == 'u':
				return _15Puzzle.Moves.UP
			if char == 'd':
				return _15Puzzle.Moves.DOWN
			if char == 'l':
				return _15Puzzle.Moves.LEFT
			if char == 'r':
				return _15Puzzle.Moves.RIGHT

			raise ValueError('Provided character is not a valid move')

		explored = set()
		frontier = []

		init_total_manhattan_distance = 0
		for i in range(0, 4):
			for j in range(0, 4):
				n = self.init_state.layout[i, j]
				if n != '0':
					init_total_manhattan_distance += self._get_manhattan_distance(n, (i, j))

		heappush(frontier, (init_total_manhattan_distance, init_total_manhattan_distance, self.init_state, ''))

		while True:         # It is given that problem is solvable
			cur_estimated_cost, cur_total_manhattan_distance, cur_state, cur_path = heappop(frontier)

			# print(cur_estimated_cost, cur_estimated_cost - cur_total_manhattan_distance, cur_path)

			if cur_total_manhattan_distance == 0:
				for c in cur_path:
					min_path.append(get_direction_from_char(c).value)
				break

			explored.add(cur_state)
			possible_next_states = cur_state.get_possible_next_states()
			for direction, possible_next_state in possible_next_states.items():
				if possible_next_state not in explored:
					changed_tile = possible_next_state.layout[cur_state.zero_location]
					new_total_manhattan_distance = cur_total_manhattan_distance - \
					                               self._get_manhattan_distance(changed_tile, possible_next_state.zero_location) + \
					                               self._get_manhattan_distance(changed_tile, cur_state.zero_location)
					new_estimated_cost = cur_estimated_cost - cur_total_manhattan_distance + 1 + new_total_manhattan_distance

					heappush(frontier, (
								new_estimated_cost,
								new_total_manhattan_distance,
								possible_next_state,
								cur_path + get_char_from_direction(direction))
					         )

					nodes_generated += 1

		return min_path, nodes_generated


	def _get_manhattan_distance(self, node_value, node_loc):
		distance = 0

		i, j = node_loc
		x, y = (a[0] for a in np.where(self.goal_state.layout == node_value))

		distance += abs(x - i) + abs(y - j)

		return distance


def FindMinimumPath(initialState, goalState):
	# minPath = []  # This list should contain the sequence of actions in the optimal solution
	# nodesGenerated = 0  # This variable should contain the number of nodes that were generated while finding the optimal solution

	puzzle = _15Puzzle(initialState, goalState)
	minPath, nodesGenerated = puzzle.solve()

	return minPath, nodesGenerated


### TODO: !!!!!!!!!!!!!! CHECK BEFORE SUBMISSION !!!!!!!!!!!!!!
# **************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
	# TODO: CHANGE BEFORE SUBMISSION
	with open("test_state2.txt", "r") as file:  # IMP: If you change the file name, then there will be an error when
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
