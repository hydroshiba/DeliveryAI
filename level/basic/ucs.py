# ucs.py
# =============================================================================
#  The Uniform Cost search algorithm, a search algorithm that explores nodes
#  with the lowest accumulated path cost, similar to Dijkstra's algorithm.
#
#  In this specific case which the graph is a grid, the cost moving from one
#  node to another is always 1, so this implementation behaves almost exactly
#  like BFS except the late goal test strategy is used instead.
# =============================================================================

from . import best
from . import Best

class UCS(Best):
	def __init__(self):
		super().__init__(best.LateTest)

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return 0
	
	def compare(self, u, v):
		if u._cost != v._cost: return u._cost < v._cost
		return u._state < v._state