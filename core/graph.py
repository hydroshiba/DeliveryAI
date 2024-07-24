# graph.py
# =============================================================================
#  A graph class to represent the map with information of toll booths and fuel
#  stations stop time.
# =============================================================================

class Graph:
	def __init__(self, width: int, height: int):
		self._width = width
		self._height = height

		self._toll = [[0 for _ in range(width)] for _ in range(height)]
		self._fuel = [[0 for _ in range(width)] for _ in range(height)]

	def __init__(self, grid):
		self._width = len(grid[0])
		self._height = len(grid)

		self._toll = [
			[
				0 if item.startswith(('S', 'G', 'F')) else int(item)
				for item in grid[i]
			]
			for i in range(self._height)
		]

		self._fuel = [
			[
				int(item[1:]) if item.startswith('F') else 0
				for item in grid[i]
			]
			for i in range(self._height)
		]

	@property
	def width(self):
		return self._width
	
	@property
	def height(self):
		return self._height
	
	@property
	def toll(self):
		return self._toll
	
	@property
	def fuel(self):
		return self._fuel
	
	@staticmethod
	def manhattan(start: tuple, end: tuple):
		return abs(start[0] - end[0]) + abs(start[1] - end[1])
	
	@staticmethod
	def euclidean(start: tuple, end: tuple):
		return ((start[0] - end[0]) ** 2 + (start[1] - end[1]) ** 2) ** 0.5