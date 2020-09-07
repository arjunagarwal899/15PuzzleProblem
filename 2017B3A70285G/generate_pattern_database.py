from heapq import *
import numpy as np
from enum import Enum

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
		if self.zero_location[0] > 0: possible_moves.append(Moves.DOWN)
		if self.zero_location[0] < 3: possible_moves.append(Moves.UP)
		if self.zero_location[1] > 0: possible_moves.append(Moves.RIGHT)
		if self.zero_location[1] < 3: possible_moves.append(Moves.LEFT)

		return possible_moves

	def get_possible_next_states(self):
		possible_next_states = {}

		for direction in self.get_possible_moves():
			possible_next_states[direction] = self._move(direction)

		return possible_next_states

	def _move(self, direction):
		if direction is Moves.UP:
			return self._move_up()
		elif direction is Moves.DOWN:
			return self._move_down()
		elif direction is Moves.LEFT:
			return self._move_left()
		elif direction is Moves.RIGHT:
			return self._move_right()

		raise TypeError


	def _move_left(self):
		if self.zero_location[1] == 3: raise IndexError('Cannot move left in the puzzle')

		new_layout = self.layout.copy()
		zl = self.zero_location
		new_layout[zl[0], (zl[1], zl[1] + 1)] = new_layout[zl[0], (zl[1] + 1, zl[1])]  # swap the elements

		return State(new_layout, (zl[0], zl[1] + 1))

	def _move_right(self):
		if self.zero_location[1] == 0: raise IndexError('Cannot move right in the puzzle')

		new_layout = self.layout.copy()
		zl = self.zero_location
		new_layout[zl[0], (zl[1] - 1, zl[1])] = new_layout[zl[0], (zl[1], zl[1] - 1)]  # swap the elements

		return State(new_layout, (zl[0], zl[1] - 1))

	def _move_up(self):
		if self.zero_location[0] == 3: raise IndexError('Cannot move up in the puzzle')

		new_layout = self.layout.copy()
		zl = self.zero_location
		new_layout[(zl[0], zl[0] + 1), zl[1]] = new_layout[(zl[0] + 1, zl[0]), zl[1]]  # swap the elements

		return State(new_layout, (zl[0] + 1, zl[1]))

	def _move_down(self):
		if self.zero_location[0] == 0: raise IndexError('Cannot move down in the puzzle')

		new_layout = self.layout.copy()
		zl = self.zero_location
		new_layout[(zl[0] - 1, zl[0]), zl[1]] = new_layout[(zl[0], zl[0] - 1), zl[1]]  # swap the elements

		return State(new_layout, (zl[0] - 1, zl[1]))

	def _find_zero(self):
		loc = np.where(self.layout == '0')
		return loc[0][0], loc[1][0]


file = '2017B3A70285G_ARJUN.dat'
goal_states = np.array([
	np.char.array([['0', '1', '2', '3'],
	               ['*', '*', '*', '*'],
	               ['*', '*', '*', '*'],
		           ['*', '*', '*', '*']])
	,
	np.char.array([['0', '*', '*', '*'],
	               ['4', '5', '6', '*'],
	               ['*', '*', '*', '*'],
		           ['*', '*', '*', '*']])
	,
	np.char.array([['0', '*', '*', '*'],
	               ['*', '*', '*', '7'],
	               ['8', '9', '*', '*'],
		           ['*', '*', '*', '*']])
	,
	np.char.array([['0', '*', '*', '*'],
	               ['*', '*', '*', '*'],
	               ['*', '*', 'A', 'B'],
		           ['C', '*', '*', '*']])
	,
	np.char.array([['0', '*', '*', '*'],
	               ['*', '*', '*', '*'],
	               ['*', '*', '*', '*'],
		           ['*', 'D', 'E', 'F']])
	,
])

with open(file, 'ab+') as f:
	max_cost = 0
	for goal_state in goal_states:
		goal_state = State(goal_state)

		frontier = []
		explored = set()
		exploring = set()
		heappush(frontier, (0, goal_state))
		exploring.add(goal_state)

		def loc_in_bytes(layout):
			locs = []
			for i in range(0, 4):
				for j in range(0, 4):
					if layout[i, j] != '*':
						locs.append((i, j))

			s = 0
			for loc in locs:
				i, j = loc
				s <<= 2
				s += i
				s <<= 2
				s += j

			return s.to_bytes(2, byteorder='big', signed=False)


		while frontier:
			cost, node = heappop(frontier)
			exploring.remove(node)

			l = loc_in_bytes(node.layout)
			c = cost.to_bytes(1, byteorder='big', signed=False)
			f.write(l + c)

			# print(l, c)

			max_cost = max(max_cost, cost)
			print(len(frontier), cost)

			possible_next_states = node.get_possible_next_states()
			for direction, possible_next_state in possible_next_states.items():
				if possible_next_state not in explored and possible_next_state not in exploring:
					new_cost = cost
					if possible_next_state.layout[node.zero_location] != '*': new_cost += 1

					heappush(frontier, (new_cost, possible_next_state))
					exploring.add(possible_next_state)

			explored.add(node)

print(max_cost)