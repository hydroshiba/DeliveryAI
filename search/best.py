# best.py
# =============================================================================
#  The Best-first search algorithm, a general framework for specific searching
#  strageties. Search strategies are implemented by inheriting this class.
# =============================================================================

from abc import ABC, abstractmethod
from queue import PriorityQueue

from core import Node
from search import Search

# Goal test tags
class EarlyTest: pass
class LateTest: pass

class Best(Search, ABC):
	def __init__(self, tag):
		self._tag = tag
		pass

	@abstractmethod
	def cost(self, graph, agent, cur, next):
		pass

	@abstractmethod
	def heuristic(self, graph, agent, cur):
		pass

	def run(self, graph, agent):
		frontier = PriorityQueue()
		visited = set()
		predecessor = dict()
		self._expanded = []

		frontier.put(Node(agent.start, None, 0, 0))

		while not frontier.empty():
			node = frontier.get()
			cur, parent, cost, time, fuel = node._state, node._parent, node._cost, node._time, node._fuel
			
			if cur in visited: continue
			if agent.optimize_time and time > agent.time: continue
			if agent.optimize_fuel and fuel < 0: continue

			visited.add(cur)
			self._expanded.append(cur)
			predecessor[cur] = parent

			# Late goal test
			if self._tag == LateTest and cur == agent.end:
				self.trace(self, predecessor, agent.start, agent.end)
				return
			
			directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
			for dx, dy in directions:
				next = (cur[0] + dx, cur[1] + dy)

				if next in visited: continue
				if not (0 <= next[0] < graph.height and 0 <= next[1] < graph.width): continue
				if graph.toll[next[0]][next[1]] == -1: continue

				new_cost = cost + self.cost(graph, agent, cur, next)
				new_heuristic = self.heuristic(graph, agent, next)

				# Optimize time
				if agent.optimize_time:
					new_time = time + graph.toll[next[0]][next[1]] + self.cost(graph, agent, cur, next)
				else: new_time = 0

				# Optimize fuel
				if agent.optimize_fuel:
					new_fuel = agent.fuel if graph.fuel[next[0]][next[1]] > 0 else fuel - 1
					new_time += graph.fuel[next[0]][next[1]]
				else: new_fuel = 0

				# Early goal test
				if self._tag == EarlyTest:
					if agent.optimize_time and new_time > agent.time: continue
					if agent.optimize_fuel and new_fuel < 0: continue
					if next == agent.end:
						predecessor[next] = cur
						self.trace(self, predecessor, agent.start, agent.end)
						return

				frontier.put(Node(next, cur, new_cost, new_heuristic, new_time, new_fuel))