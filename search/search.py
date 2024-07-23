# search.py
# =============================================================================
#  A generic search class to be inherited by other search algorithms.
# =============================================================================

from abc import ABC, abstractmethod

class Search(ABC):
	# @abstractmethod
	# def search(self, graph, agent):
	# 	pass

	@staticmethod
	def trace(predecessor : dict, start : tuple, end : tuple):
		path = []

		while end != start:
			if predecessor.get(end) is None:
				return []

			path.append(end)
			end = predecessor[end]

		path.append(start)
		path.reverse()
		return path