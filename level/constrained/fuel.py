# fuel.py
# =============================================================================
#  A modified A* search algorithm to find the shortest path while considering
#  both the time and fuel constraints.
# =============================================================================

from core import Heap
from core import Search

class FuelSearch(Search):
	def __init__(self):
		super().__init__()

	def augment_path(self):
		for i in range(len(self._path)):
			self._path[i] = self._path[i][0]

	class Node:
		def __init__(self, state, parent, cost, heuristic, time, fuel):
			self._state = state
			self._parent = parent
			self._cost = cost
			self._heuristic = heuristic
			self._time = time
			self._fuel = fuel

	def cost(self, graph, agent, cur, next):
		return 1

	def heuristic(self, graph, agent, cur):
		return graph.manhattan(cur, agent.end)

	def compare(self, u: Node, v: Node):
		u_sum = u._cost + u._heuristic
		v_sum = v._cost + v._heuristic

		if u_sum != v_sum: return u_sum < v_sum
		if u._time != v._time: return u._time < v._time
		if u._fuel != v._fuel: return u._fuel < v._fuel

		return u._state < v._state

	def run(self, graph, agent):
		if(not agent.optimize_time): raise ValueError('Agent does not have time constraint.')
		if(not agent.optimize_fuel): raise ValueError('Agent does not have fuel constraint.')

		visited = set()
		predecessor = dict()
		self._expanded = []

		frontier = Heap(self.compare)
		frontier.put(self.Node(
			(agent.start, agent.fuel),
			None,
			0,
			0,
			0,
			agent.fuel
		))

		while not frontier.empty():
			node = frontier.get()
			cur, parent, cost, time, fuel = node._state, node._parent, node._cost, node._time, node._fuel

			if cur in visited: continue
			if time > agent.time: continue
			if fuel < 0: continue

			visited.add(cur)
			self._expanded.append(cur)
			if predecessor.get(cur) is None: predecessor[cur] = parent

			# Late goal test
			if cur[0] == agent.end:
				self.trace(predecessor, cur)
				self.augment_path()
				return
			
			directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

			for dir in directions:
				next = (cur[0][0] + dir[0], cur[0][1] + dir[1])

				if next in visited: continue
				if not (0 <= next[0] < graph.height and 0 <= next[1] < graph.width): continue
				if graph.toll[next[0]][next[1]] == -1: continue
				
				new_cost = cost + self.cost(graph, agent, cur, next)
				new_heuristic = self.heuristic(graph, agent, next)
				new_time = time + graph.toll[next[0]][next[1]] + graph.fuel[next[0]][next[1]] + 1
				new_fuel = agent.fuel if bool(graph.fuel[next[0]][next[1]]) else fuel - 1

				frontier.put(self.Node(
					(next, new_fuel),
					cur,
					new_cost,
					new_heuristic,
					new_time,
					new_fuel
				))