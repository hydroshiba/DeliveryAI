# dfs.py
# =============================================================================
#  The Depth-first search algorithm, a search algorithm that explores nodes
#  in depth first manner before moving on to the next branch.
# =============================================================================

from . import best
from search.best import Best

class DFS(Best):
	def __init__(self):
		super().__init__(best.EarlyTest)

	def cost(self, graph, agent, cur, next):
		return -1

	def heuristic(self, graph, agent, cur):
		return 0