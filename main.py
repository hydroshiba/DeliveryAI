from core import Reader
from core import Agent

from search import BFS
from search import DFS
from search import UCS
from search import GBFS
from search import AStar

graph, agents = Reader.read('testcase/input.txt')
agent = Agent(agents[0].start, agents[0].end, agents[0].time)

print('Agent: ', agent.start, agent.end)
print('Optimize time: ', 'Yes' if agent.optimize_time else 'No')
print('Optimize fuel: ', 'Yes' if agent.optimize_fuel else 'No', '\n')

# =============================================================================

search = BFS()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')

# =============================================================================

search = DFS()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')

# =============================================================================

search = UCS()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')

# =============================================================================

search = GBFS()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')

# =============================================================================

search = AStar()
print('Search: ', search)

search.run(graph, agent)
path = search.path
expanded = search.expanded

print('Path distance: ', len(path) - 1)
print('Path:\n', ' '.join(str(p) for p in path), '\n')
print('Expanded:\n', ' '.join(str(e) for e in expanded), '\n')