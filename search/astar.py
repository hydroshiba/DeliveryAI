# astar.py
# =============================================================================
#  The A* search algorithm, a search algorithm that prioritizing nodes with
#  the sum of its accumulated path cost and its heuristic value.
# =============================================================================

from . import best
from search.best import Best

class AStar(Best):
	def __init__(self):
		super().__init__(best.LateTest)

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return graph.manhattan(cur, agent.end)