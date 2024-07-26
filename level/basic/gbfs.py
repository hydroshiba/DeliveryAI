# gbfs.py
# =============================================================================
#  The Greedy Best-first search algorithm, a search algorithm that explores
#  nodes with the lowest heuristic value first.
# =============================================================================

from . import best
from . import Best

class GBFS(Best):
	def __init__(self):
		super().__init__(best.EarlyTest)

	def cost(self, graph, agent, cur, next):
		return 0

	def heuristic(self, graph, agent, cur):
		return graph.manhattan(cur, agent.end)
	
	def compare(self, u, v):
		return u._heuristic < v._heuristic