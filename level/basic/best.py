# best.py
# =============================================================================
#  The Best-first search algorithm, a general framework for specific searching
#  strageties. Search strategies are implemented by inheriting this class.
# =============================================================================

from abc import ABC, abstractmethod
from core import Heap
from core import Search

# Goal test tags
class EarlyTest: pass
class LateTest: pass

class Best(Search, ABC):
	def __init__(self, tag):
		super().__init__()
		self._tag = tag

	class Node:
		def __init__(self, state, parent, cost, heuristic):
			self._state = state
			self._parent = parent
			self._cost = cost
			self._heuristic = heuristic

	@abstractmethod
	def cost(self, graph, agent, cur, next):
		pass

	@abstractmethod
	def heuristic(self, graph, agent, cur):
		pass

	@abstractmethod
	def compare(self, u: Node, v: Node):
		pass

	def run(self, graph, agent):
		visited = set()
		predecessor = dict()
		self._expanded = []

		frontier = Heap(self.compare)
		frontier.put(self.Node(agent.start, None, 0, 0))

		while not frontier.empty():
			node = frontier.get()
			cur, parent, cost = node._state, node._parent, node._cost
			if cur in visited: continue

			visited.add(cur)
			self._expanded.append(cur)
			if predecessor.get(cur) is None: predecessor[cur] = parent

			# Late goal test
			if self._tag == LateTest and cur == agent.end:
				self.trace(predecessor, cur)
				return
			
			directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

			for dir in directions:
				next = (cur[0] + dir[0], cur[1] + dir[1])

				if next in visited: continue
				if not (0 <= next[0] < graph.height and 0 <= next[1] < graph.width): continue
				if graph.toll[next[0]][next[1]] == -1: continue

				# Early goal test
				if self._tag == EarlyTest and next == agent.end:
					predecessor[next] = cur
					self.trace(predecessor, cur)
					return
				
				new_cost = cost + self.cost(graph, agent, cur, next)
				new_heuristic = self.heuristic(graph, agent, next)
				frontier.put(self.Node(next, cur, new_cost, new_heuristic))