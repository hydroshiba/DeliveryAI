# reader.py
# =============================================================================
#  A reader class to generate a grid and its agents from a given input file.
# =============================================================================

from .agent import Agent
from .graph import Graph

class Reader:
	@staticmethod
	def read(path: str):
		with open(path, 'r') as f:
			width, height, time, fuel = map(int, f.readline().split())
			grid = [f.readline().split() for _ in range(height)]

			graph = Graph(grid)
			coordinates = dict()
			agents = []
			
			for i in range(height):
				for j in range(width):
					element = grid[i][j]
					if element.startswith('S'):
						coordinates[int(element[1:]) if len(element) > 1 else 0] = [(i, j)]
					else: continue

			for i in range(height):
				for j in range(width):
					element = grid[i][j]
					if element.startswith('G'):
						coordinates[int(element[1:]) if len(element) > 1 else 0].append((i, j))

			for key in sorted(coordinates.keys()):
				agents.append(Agent(
					coordinates[key][0],
					coordinates[key][1],
					time,
					fuel
				))

			return graph, agents