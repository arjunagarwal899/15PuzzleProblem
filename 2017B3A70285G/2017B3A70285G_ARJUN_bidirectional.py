#!/usr/bin/env python3
import time
from heapq import *  # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************

from enum import Enum  # Imported built-in "enum.Enum" class for declaring enumerations


class Puzzle:
	# An enumeration for storing the possible moves that can be made in the 15 Puzzle Problem
	class Moves(Enum):
		UP = 'U'
		DOWN = 'D'
		LEFT = 'L'
		RIGHT = 'R'


	class State:
		def __init__(self, layout, zero_location=None):
			self.layout = layout
			if isinstance(layout, list):
				self.layout = ''.join(sum(layout, []))

			if zero_location is None: zero_location = self._find_zero()
			self.zero = zero_location

		def __lt__(self, other):
			if not isinstance(other, Puzzle.State): raise TypeError(
				'Can compare Puzzle.State only with another Puzzle.State')
			return self.layout < other.layout

		def __le__(self, other):
			if not isinstance(other, Puzzle.State): raise TypeError(
				'Can compare Puzzle.State only with another Puzzle.State')
			return self.layout <= other.layout

		def __ge__(self, other):
			return not self < other

		def __gt__(self, other):
			return not self <= other

		def __eq__(self, other):
			if not isinstance(other, Puzzle.State): raise TypeError(
				'Can compare Puzzle.State only with another Puzzle.State')
			return self.layout == other.layout

		def __hash__(self):
			return hash(self.layout)

		def __str__(self):
			return self.layout

		def get_possible_moves(self):
			possible_moves = set()
			if self.zero < 12: possible_moves.add(Puzzle.Moves.UP)
			if self.zero > 3: possible_moves.add(Puzzle.Moves.DOWN)
			if self.zero % 4 != 3: possible_moves.add(Puzzle.Moves.LEFT)
			if self.zero % 4 != 0: possible_moves.add(Puzzle.Moves.RIGHT)

			return possible_moves

		def get_possible_next_states(self):
			possible_next_states = {}

			for direction in self.get_possible_moves():
				possible_next_states[direction] = self._move(direction)

			return possible_next_states

		def get_forward_heuristic_cost(self, database, masking_tables):
			heuristic_cost = 0

			for masking_table in masking_tables:
				masked_state_layout = self._mask(masking_table)
				heuristic_cost += database[masked_state_layout]

			return heuristic_cost

		def get_backward_heuristic_cost(self, init_state, cur_loc, cur_value):
			d = abs(init_state.layout.find(cur_value) - cur_loc)
			return int(d / 4) + d % 4


		def _mask(self, masking_table):
			return self.layout.translate(masking_table)

		def _move(self, direction):
			if direction is Puzzle.Moves.UP:
				return self._move_up()
			elif direction is Puzzle.Moves.DOWN:
				return self._move_down()
			elif direction is Puzzle.Moves.LEFT:
				return self._move_left()
			elif direction is Puzzle.Moves.RIGHT:
				return self._move_right()

			raise TypeError

		def _move_up(self):
			new_layout = self.layout
			z = self.zero

			new_layout = new_layout[:z] + new_layout[z + 4] + new_layout[z + 1: z + 4] + new_layout[z] + new_layout[
			                                                                                             z + 5:]

			return Puzzle.State(new_layout, z + 4)

		def _move_down(self):
			new_layout = self.layout
			z = self.zero

			new_layout = new_layout[:z - 4] + new_layout[z] + new_layout[z - 3: z] + new_layout[z - 4] + new_layout[
			                                                                                             z + 1:]

			return Puzzle.State(new_layout, z - 4)

		def _move_left(self):
			new_layout = self.layout
			z = self.zero

			new_layout = new_layout[:z] + new_layout[z + 1] + new_layout[z] + new_layout[z + 2:]

			return Puzzle.State(new_layout, z + 1)

		def _move_right(self):
			new_layout = self.layout
			z = self.zero

			new_layout = new_layout[:z - 1] + new_layout[z] + new_layout[z - 1] + new_layout[z + 1:]

			return Puzzle.State(new_layout, z - 1)

		def _find_zero(self):
			return self.layout.find('0')


	def __init__(self, problem, goal_state):
		# !! Input is assumed to be correctly formatted in a 2 dimensional array with 4 rows and 4 columns !!
		self.init_state = Puzzle.State(problem)
		self._goal_state = Puzzle.State(goal_state)

		self._database = {}
		self._masking_tables = [
			''.maketrans('0123456789ABCDEF', '*1234***********'),
			''.maketrans('0123456789ABCDEF', '*****5678*******'),
			''.maketrans('0123456789ABCDEF', '*********9ABC***'),
			''.maketrans('0123456789ABCDEF', '*************DEF'),
		]

		self._heuristic_combinations = [
			('1234', 43680),
			('5678', 43680),
			('9ABC', 43680),
			('DEF', 3360),
		]


	def solve(self):
		return self._bidirectional_a_star()

	def _bidirectional_a_star(self):
		nodes_generated = 0

		self._read_heuristic_file()

		explored_forward = set()
		frontier_forward = []
		frontier_forward_dict = {}
		explored_backward = set()
		frontier_backward = []
		frontier_backward_dict = {}

		init_forward_heuristic_cost = self.init_state.get_forward_heuristic_cost(self._database, self._masking_tables)
		heappush(frontier_forward, (init_forward_heuristic_cost, init_forward_heuristic_cost, self.init_state, ''))
		frontier_forward_dict[self.init_state] = ''

		init_backward_heuristic_cost = 0
		for i in range(0, 16):
			if self._goal_state.layout[i] != '0':
				init_backward_heuristic_cost += self._goal_state.get_backward_heuristic_cost(self.init_state, i,
				                                                                             self._goal_state.layout[i])
		heappush(frontier_backward, (init_backward_heuristic_cost, init_backward_heuristic_cost, self._goal_state, ''))
		frontier_backward_dict[self._goal_state] = ''

		while True:  # It is given that problem is solvable
			cur_forward_estimated_cost, cur_forward_heuristic_cost, cur_forward_state, cur_forward_path = heappop(
				frontier_forward)
			if cur_forward_state in frontier_forward_dict:
				frontier_forward_dict.pop(cur_forward_state)

				# print(cur_forward_estimated_cost, cur_forward_estimated_cost - cur_forward_heuristic_cost, cur_forward_path)

				if cur_forward_state in frontier_backward_dict:
					maximin = max(cur_forward_estimated_cost, frontier_backward[0][0])
					if len(cur_forward_path) + len(frontier_backward_dict[cur_forward_state]) <= maximin:
						min_path_forward = list(cur_forward_path)
						min_path_backward = list(frontier_backward_dict[cur_forward_state])
						forward_direction_ref = {
							Puzzle.Moves.UP.value: 'Up',
							Puzzle.Moves.DOWN.value: 'Down',
							Puzzle.Moves.LEFT.value: 'Left',
							Puzzle.Moves.RIGHT.value: 'Right'
						}
						backward_direction_ref = {
							Puzzle.Moves.UP.value: 'Down',
							Puzzle.Moves.DOWN.value: 'Up',
							Puzzle.Moves.LEFT.value: 'Right',
							Puzzle.Moves.RIGHT.value: 'Left'
						}
						for i in range(0, len(min_path_forward)):
							min_path_forward[i] = forward_direction_ref[min_path_forward[i]]

						min_path = min_path_forward
						min_path.append(['-----'])

						for i in range(len(min_path_backward) - 1, -1, -1):
							min_path.append(backward_direction_ref[min_path_backward[i]])
						break

				possible_forward_next_states = cur_forward_state.get_possible_next_states()
				for direction, possible_forward_next_state in possible_forward_next_states.items():
					if possible_forward_next_state not in explored_forward:
						new_forward_heuristic_cost = possible_forward_next_state.get_forward_heuristic_cost(
							self._database,
							self._masking_tables)

						new_forward_estimated_cost = cur_forward_estimated_cost - cur_forward_heuristic_cost + 1 + new_forward_heuristic_cost

						heappush(frontier_forward, (
							new_forward_estimated_cost,
							new_forward_heuristic_cost,
							possible_forward_next_state,
							cur_forward_path + direction.value
						))
						if possible_forward_next_state in frontier_forward_dict:
							frontier_forward_dict[possible_forward_next_state] = min(
								frontier_forward_dict[possible_forward_next_state], cur_forward_path + direction.value,
								key=len)
						else:
							frontier_forward_dict[possible_forward_next_state] = cur_forward_path + direction.value

						nodes_generated += 1
				explored_forward.add(cur_forward_state)

			# !!!!!! Backward search !!!!!!

			cur_backward_estimated_cost, cur_backward_heuristic_cost, cur_backward_state, cur_backward_path = heappop(
				frontier_backward)
			if cur_backward_state in frontier_backward_dict:
				frontier_backward_dict.pop(cur_backward_state)

				# print(cur_backward_estimated_cost, cur_backward_estimated_cost - cur_backward_heuristic_cost, cur_backward_path)

				if cur_backward_state in frontier_forward_dict:
					maximin = max(cur_backward_estimated_cost, frontier_forward[0][0])
					if len(cur_backward_path) + len(frontier_forward_dict[cur_backward_state]) <= maximin:
						min_path_backward = list(cur_backward_path)
						min_path_forward = list(frontier_forward_dict[cur_backward_state])
						forward_direction_ref = {
							Puzzle.Moves.UP.value: 'Up',
							Puzzle.Moves.DOWN.value: 'Down',
							Puzzle.Moves.LEFT.value: 'Left',
							Puzzle.Moves.RIGHT.value: 'Right'
						}
						backward_direction_ref = {
							Puzzle.Moves.UP.value: 'Down',
							Puzzle.Moves.DOWN.value: 'Up',
							Puzzle.Moves.LEFT.value: 'Right',
							Puzzle.Moves.RIGHT.value: 'Left'
						}
						for i in range(0, len(min_path_forward)):
							min_path_forward[i] = forward_direction_ref[min_path_forward[i]]

						min_path = min_path_forward
						min_path.append(['-----'])

						for i in range(len(min_path_backward) - 1, -1, -1):
							min_path.append(backward_direction_ref[min_path_backward[i]])
						break

				possible_backward_next_states = cur_backward_state.get_possible_next_states()
				for direction, possible_backward_next_state in possible_backward_next_states.items():
					if possible_backward_next_state not in explored_backward:
						# new_backward_heuristic_cost = possible_backward_next_state.get_backward_heuristic_cost(self._database,
						#                                                                                     self._masking_tables)

						czl = cur_backward_state.zero
						pzl = possible_backward_next_state.zero
						new_backward_heuristic_cost = cur_backward_heuristic_cost - cur_backward_state.get_backward_heuristic_cost(
							self.init_state, pzl,
							cur_backward_state.layout[pzl]) + possible_backward_next_state.get_backward_heuristic_cost(
							self.init_state, czl, possible_backward_next_state.layout[czl])

						new_backward_estimated_cost = cur_backward_estimated_cost - cur_backward_heuristic_cost + 1 + new_backward_heuristic_cost

						heappush(frontier_backward, (
							new_backward_estimated_cost,
							new_backward_heuristic_cost,
							possible_backward_next_state,
							cur_backward_path + direction.value
						))
						if possible_backward_next_state in frontier_backward_dict:
							frontier_backward_dict[possible_backward_next_state] = min(
								frontier_backward_dict[possible_backward_next_state],
								cur_backward_path + direction.value,
								key=len)
						else:
							frontier_backward_dict[possible_backward_next_state] = cur_backward_path + direction.value

						nodes_generated += 1
				explored_backward.add(cur_backward_state)

		return min_path, nodes_generated


	def _read_heuristic_file(self):
		with open(r'2017B3A70285G_ARJUN.dat', 'rb') as hf:
			data = hf.read()

		start_size = 0
		for combination, size in self._heuristic_combinations:
			for j in range(0, size):
				data_loc = start_size + 3 * j
				blocks_locs = int.from_bytes(data[data_loc: data_loc + 2], byteorder='big', signed=False)
				cost = data[data_loc + 2]

				key = '****************'
				for block in combination[::-1]:
					block_loc = blocks_locs & 15
					blocks_locs >>= 4
					key = key[: block_loc] + block + key[block_loc + 1:]

				self._database[key] = cost

			start_size += size * 3


def FindMinimumPath(initialState, goalState):
	# minPath = []  # This list should contain the sequence of actions in the optimal solution
	# nodesGenerated = 0  # This variable should contain the number of nodes that were generated while finding the optimal solution

	puzzle = Puzzle(initialState, goalState)
	minPath, nodesGenerated = puzzle.solve()

	return minPath, nodesGenerated


### TODO: !!!!!!!!!!!!!! CHECK BEFORE SUBMISSION !!!!!!!!!!!!!!
# **************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
	# TODO: CHANGE BEFORE SUBMISSION
	with open("test_state55.txt", "r") as file:  # IMP: If you change the file name, then there will be an error when
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
	print('   Time taken : {0} s'.format(round(timeTaken, 4)))


if __name__ == '__main__':
	main()
