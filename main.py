from core import Reader
from core import Agent

from level.basic import BFS
from level.basic import DFS
from level.basic import UCS
from level.basic import GBFS
from level.basic import AStar

from level.constrained import TimeSearch
from level.constrained import FuelSearch

graph, agents = Reader.read('testcase/input.txt')
agent = agents[0]

print('Agent: ', agent.start, agent.end)
print('Optimize time: ', 'Yes' if agent.optimize_time else 'No')
print('Optimize fuel: ', 'Yes' if agent.optimize_fuel else 'No', '\n')

# =============================================================================

search = FuelSearch()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')