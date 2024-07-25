# node.py
# =============================================================================
#  A simple node structure to represent the state of the agent. Allows search
#  algorithms to inherit and define custom comparison methods.
# =============================================================================

class Node():
	def __init__(self, state, parent, cost, heuristic, time = None, fuel = None):
		self._state = state
		self._parent = parent

		self._cost = cost
		self._heuristic = heuristic

		self._time = time
		self._fuel = fuel