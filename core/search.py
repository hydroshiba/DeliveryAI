# base.py
# =============================================================================
#  A generic search class to be inherited by other search algorithms.
# =============================================================================

from abc import ABC, abstractmethod

class Search(ABC):
	def __init__(self):
		self._path = []
		self._expanded = []

	@property
	def path(self):
		return self._path
	
	@property
	def expanded(self):
		return self._expanded

	@abstractmethod
	def run(self, graph, agent):
		pass

	def trace(self, predecessor: dict, end):
		self._path = []

		while end != None:
			self._path.append(end)
			end = predecessor[end]

		self._path.reverse()