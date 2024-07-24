# node.py
# =============================================================================
#  A simple node structure to represent the state of the agent.
# =============================================================================

class Node:
	def __init__(self, state, parent, cost, heuristic, time = 0, fuel = 0):
		self._state = state
		self._parent = parent

		self._cost = cost
		self._heuristic = heuristic

		self._time = time
		self._fuel = fuel

	def __lt__(self, other):
		return self._cost + self._heuristic < other._cost + other._heuristic