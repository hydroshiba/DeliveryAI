from core import Reader
from core import Agent

from search import BFS
from search import DFS
from search import GBFS

graph, agents = Reader.read('testcase/input.txt')
agent = Agent(agents[0].start, agents[0].end)
print('Agent: ', agent.start, agent.end, '\n')

search = BFS()
print('Search: ', search, '\n')

search.run(graph, agent)
path = search.path
expanded = search.expanded

print(path, '\n')
print(expanded, '\n')

# =============================================================================

search = DFS()
print('Search: ', search, '\n')

search.run(graph, agent)
path = search.path
expanded = search.expanded

print(path, '\n')
print(expanded, '\n')

# =============================================================================

search = GBFS()
print('Search: ', search, '\n')

search.run(graph, agent)
path = search.path
expanded = search.expanded

print(path, '\n')
print(expanded, '\n')