# time.py
# =============================================================================
#  A modified A* search algorithm to find the shortest path while considering
#  the time constraint.
# =============================================================================

from core import Heap
from core import Search

class TimeSearch(Search):
	def __init__(self):
		super().__init__()

	class Node:
		def __init__(self, state, parent, cost, heuristic, time):
			self._state = state
			self._parent = parent
			self._cost = cost
			self._heuristic = heuristic
			self._time = time

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return graph.manhattan(cur, agent.end)

	def compare(self, u: Node, v: Node):
		u_sum = u._cost + u._heuristic
		v_sum = v._cost + v._heuristic

		if u_sum != v_sum: return u_sum < v_sum
		if u._time != None and u._time != v._time: return u._time < v._time
		return u._state < v._state

	def run(self, graph, agent):
		if(not agent.optimize_time): raise ValueError('Agent does not have time constraint.')

		visited = set()
		predecessor = dict()
		self._expanded = []

		frontier = Heap(self.compare)
		frontier.put(self.Node(agent.start, None, 0, 0, 0))

		while not frontier.empty():
			node = frontier.get()
			cur, parent, cost, time = node._state, node._parent, node._cost, node._time

			if cur in visited: continue
			if time > agent.time: continue

			visited.add(cur)
			self._expanded.append(cur)
			if predecessor.get(cur) is None: predecessor[cur] = parent

			# Late goal test
			if cur == agent.end:
				self.trace(predecessor, agent.start, agent.end)
				return
			
			directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

			for dir in directions:
				next = (cur[0] + dir[0], cur[1] + dir[1])

				if next in visited: continue
				if not (0 <= next[0] < graph.height and 0 <= next[1] < graph.width): continue
				if graph.toll[next[0]][next[1]] == -1: continue
				
				new_cost = cost + self.cost(graph, agent, cur, next)
				new_heuristic = self.heuristic(graph, agent, next)
				new_time = time + max(graph.toll[next[0]][next[1]], 1)

				frontier.put(self.Node(next, cur, new_cost, new_heuristic, new_time))