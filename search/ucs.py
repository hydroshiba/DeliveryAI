# ucs.py
# =============================================================================
#  The Uniform Cost Search algorithm, a search algorithm that explores nodes
#  with the lowest accumulated path cost, similar to Dijkstra's algorithm.
#
#  In this specific case which the graph is a grid, the cost moving from one
#  node to another is always 1, so this implementation behaves exactly like
#  BFS.
# =============================================================================

from . import best
from search.best import Best

class UCS(Best):
	def __init__(self):
		super().__init__(best.LateTest)

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return 0