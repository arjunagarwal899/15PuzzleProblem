#!/usr/bin/env python3
import time
from heapq import *  # See heapq_test.py file to learn how to use. Visit : https://docs.python.org/3/library/heapq.html

from enum import Enum   # Imported built-in "enum.Enum" class for declaring enumerations

### Don't use fancy libraries. Evaluators won't install fancy libraries. You may use Numpy and Scipy if needed.
### Send an email to the instructor if you want to use more libraries.


# ********************************************************************

# Main class which will allow creating objects for the 15 Puzzle Problem
class Puzzle:
	encoding = 'utf-8'  # Encoding used for string<->bytes conversion

	# An enumeration for storing the possible moves that can be made in the 15 Puzzle Problem
	class Moves(Enum):
		UP = 'Up'
		DOWN = 'Down'
		LEFT = 'Left'
		RIGHT = 'Right'

	# Nested class representing the path taken from the initial state to the current state. Derived from list
	class Path(list):
		def __lt__(self, other): return False  # Overrides the "less than" operator as paths cannot be compared

	# Nested class to store the state of the puzzle and provide possible next states, heuristic cost etc.
	class State:
		def __init__(self, layout, zero_location=None):
			"""Stores state layout as a bytearray and the location of the blank space in the layout"""
			self.layout = layout
			if isinstance(layout, list):
				self.layout = bytearray(b''.join(bytes(a, encoding=Puzzle.encoding) for a in sum(layout, [])))

			if zero_location is None: zero_location = self.layout.find(b'0')
			self.zero = zero_location

		def __lt__(self, other):  # Overrides the "less than" operator as states cannot be compared
			return False

		def __eq__(self, other):  # States are equal if their layout is the same
			return self.layout == other.layout

		def __hash__(self):  # To hash a state. Used in sets amd dicts.
			return hash(self.layout.hex())  # Hashed on the basis of the hex value of the layout

		def __str__(self):  # Utility function. Prints the layout of the state
			return str(bytes(self.layout))


		def get_possible_next_states(self):  # Returns all the states which can be reached from this particular
			#  state along with the direction as a dict
			possible_next_states = {}

			if self.zero < 12:
				possible_next_states[Puzzle.Moves.DOWN] = self._move_down()
			if self.zero > 3:
				possible_next_states[Puzzle.Moves.UP] = self._move_up()
			if self.zero % 4 != 3:
				possible_next_states[Puzzle.Moves.RIGHT] = self._move_right()
			if self.zero % 4 != 0:
				possible_next_states[Puzzle.Moves.LEFT] = self._move_left()

			return possible_next_states

		def get_heuristic_cost(self, database, masking_tables):
			# Returns the heuristic cost from the current state to the goal state using the database and masking tables
			heuristic_cost = 0

			for masking_table in masking_tables:
				masked_state_layout = self.layout.translate(masking_table)      # Mask the current state
				heuristic_cost += database[masked_state_layout.hex()]           # Values can be ADDED

			return heuristic_cost


		def _move_down(self):  # Returns the next state on performing the move 'Up'
			new_layout = self.layout.copy()
			z = self.zero

			new_layout[z], new_layout[z + 4] = new_layout[z + 4], new_layout[z]

			return Puzzle.State(new_layout, z + 4)

		def _move_up(self):  # Returns the next state on performing the move 'Down'
			new_layout = self.layout.copy()
			z = self.zero

			new_layout[z - 4], new_layout[z] = new_layout[z], new_layout[z - 4]

			return Puzzle.State(new_layout, z - 4)

		def _move_right(self):  # Returns the next state on performing the move 'Left'
			new_layout = self.layout.copy()
			z = self.zero

			new_layout[z], new_layout[z + 1] = new_layout[z + 1], new_layout[z]

			return Puzzle.State(new_layout, z + 1)

		def _move_left(self):  # Returns the next state on performing the move 'Right'
			new_layout = self.layout.copy()
			z = self.zero

			new_layout[z - 1], new_layout[z] = new_layout[z], new_layout[z - 1]

			return Puzzle.State(new_layout, z - 1)


	def __init__(self, problem, goal_state):  # Initialize the puzzle with the start state and goal state
		# !! Input is assumed to be correctly formatted in a 2 dimensional array with 4 rows and 4 columns !!
		self.init_state = Puzzle.State(problem)
		self._goal_state = Puzzle.State(goal_state)

		self._database = {}  # dict used for storing the pattern databases
		self._masking_tables = [  # masking tables corresponding to the pattern databases
			b''.maketrans(b'045689ABCDEF', b'************'),        # 01234567890ABCDEF -> *123***7********
			b''.maketrans(b'01235679ABEF', b'************'),        # 01234567890ABCDEF -> ****4***8***CD**
			b''.maketrans(b'0123478BCDEF', b'************'),        # 01234567890ABCDEF -> *****56**9A*****
			b''.maketrans(b'0123456789ACD', b'*************'),      # 01234567890ABCDEF -> ***********B**EF
		]

		self._pattern_database_keys = [                 # The combinations of tiles and number of elements related to
			(bytearray(b'7321************'), 43680),    #  each pattern database
			(bytearray(b'DC84************'), 43680),    # Four additive disjoint pattern databases have been used
			(bytearray(b'A965************'), 43680),    #  amounting to a total of 134400 bytes
			(bytearray(b'FEB*************'), 3360),     # Databases chosen such that they can be accommodated within
		]  # supplementary file size limitations

	def solve(self):  # Function to solve the puzzle. Perform A* search with pattern databases heuristics
		nodes_generated = 0
		min_path = Puzzle.Path()

		self._read_heuristic_file()  # Read the pattern databases from the .dat file

		explored = set()  # Hash set to store the states which have already been explored
		frontier = []  # Heap to store the states which are in the frontier along with
		# related information

		# Push initial state to frontier with dummy costs
		# Format of frontier elements:
		# 	Tuple containing 4 elements:
		# 	1) Total estimated cost i.e. f(n) = g(n) + h(n)
		#   2) Current heuristic cost i.e. h(n)
		#   3) Pointer to current state
		#   4) Pointer to current Path
		# This way priority is determined in the order f(n), h(n). Since states and paths cannot be compared, they
		#  were overridden
		heappush(frontier, (0, 0, self.init_state, Puzzle.Path()))

		while True:  # It is given that problem is solvable

			# Pop element from frontier and check if it has been visited before
			cur_estimated_cost, cur_heuristic_cost, cur_state, cur_path = heappop(frontier)
			if cur_state in explored:  # Ignore node if it has already been visited
				continue

			# Uncomment following line for debugging purposes: prints "f(n)    g(n)    h(n)    Path_compact"
			# print(cur_estimated_cost, cur_estimated_cost - cur_heuristic_cost, cur_heuristic_cost, ''.join([a[0] for a in cur_path]))

			# Exit loop if solution is found
			if cur_state == self._goal_state:
				min_path = cur_path
				break

			# Get the next states possible from current state
			possible_next_states = cur_state.get_possible_next_states()

			while possible_next_states:
				# Pops random item before Python 3.7. Pops last item added from Python 3.7 onwards.
				direction, possible_next_state = possible_next_states.popitem()

				# Add next state to frontier only if it hasn't been explored already
				if possible_next_state not in explored:
					# Calculate the heuristic cost for the next state
					new_heuristic_cost = possible_next_state.get_heuristic_cost(self._database, self._masking_tables)

					# Calculate the total cost for the next state
					new_estimated_cost = cur_estimated_cost - cur_heuristic_cost + 1 + new_heuristic_cost

					# Push new node to the frontier
					heappush(frontier, (
						new_estimated_cost,
						new_heuristic_cost,
						possible_next_state,
						Puzzle.Path(cur_path + [direction.value])
					))

					# Increment count of nodes generated by 1 for each node added to the frontier
					nodes_generated += 1

			# Add current state to the explored set
			explored.add(cur_state)

		return min_path, nodes_generated


	def _read_heuristic_file(self):
		"""
			Read the supplementary file and save it in the _databases variable
			Format of supplementary file:
				Each byte corresponds to the cost of a partidular pattern.
				The costs are stored in lexicographical order of the states
				i.e. (heuristic cost related to ************1237)(heuristic cost related to ************1273)
					(heuristic cost related to ************1327) and so on...
				Order of patterns is 1237, 48CD, 569A, BEF

			Space required:
				For combinations 1237, 48CD and 569A each:  1 bytes * (16! / 12!) entries = 40320 bytes
				For combination BEF:                        1 bytes + (16! / 13!) entries = 3360 bytes
				Therefore total space required: 3 * 40320 + 3360 = 134400 bytes ~ 132KB
		"""

		def next_permutation(cur):  # Function to generate next permutation of state in lexicographical order
			i = len(cur) - 1
			while i > 0:
				if cur[i] <= cur[i - 1]:
					i -= 1
				else:
					break
			i -= 1

			if i == -1: return cur[::-1]

			j = len(cur) - 1
			while j >= i:
				if cur[j] > cur[i]:
					break
				else:
					j -= 1

			cur[i], cur[j] = cur[j], cur[i]

			x, y = i + 1, i - len(cur)
			cur[x:] = cur[:y:-1]

			return cur

		with open(r'2017B3A70285G_ARJUN.dat', 'rb') as hf:
			data = hf.read()

		start_size = 0
		for pattern_database_key, size in self._pattern_database_keys:
			key = pattern_database_key
			for j in range(0, size):
				key = next_permutation(key)
				cost = data[start_size + j]

				self._database[key.hex()] = cost

			start_size += size


def FindMinimumPath(initialState, goalState):
	# minPath = []  # This list should contain the sequence of actions in the optimal solution
	# nodesGenerated = 0  # This variable should contain the number of nodes that were generated while finding the optimal solution

	puzzle = Puzzle(initialState, goalState)
	minPath, nodesGenerated = puzzle.solve()

	return minPath, nodesGenerated


# **************   DO NOT CHANGE ANY CODE BELOW THIS LINE *****************************


def ReadInitialState():
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
	print('   Time taken : {0} s'.format(round(timeTaken, 4)))


if __name__ == '__main__':
	main()
