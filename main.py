from core import Reader
from core import Agent

from search import BFS

graph, agents = Reader.read('testcase/input.txt')
agent = Agent(agents[0].start, agents[0].end)
search = BFS()

search.search(graph, agent)
path = search.path
expanded = search.expanded

print(agent.start, agent.end, '\n')
print(path, '\n')
print(expanded, '\n')