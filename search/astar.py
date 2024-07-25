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
	
	def compare(self, u, v):
		u_sum = u._cost + u._heuristic
		v_sum = v._cost + v._heuristic

		if u_sum != v_sum: return u_sum < v_sum
		if u._time != None and u._time != v._time: return u._time < v._time
		if u._fuel != None and u._fuel != v._fuel: return u._fuel > v._fuel

		return u._state < v._state