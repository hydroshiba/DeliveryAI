# bfs.py
# =============================================================================
#  The Breadth-first search algorithm, a search algorithm that explores all
#  nodes at the present depth first before moving on to next depth.
# =============================================================================

from . import best
from search.best import Best

class BFS(Best):
	def __init__(self):
		super().__init__(best.EarlyTest)

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return 0

	def compare(self, u, v):
		if u._cost != v._cost: return u._cost < v._cost
		return u._state < v._state