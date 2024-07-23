from core import Reader
from core import Agent
from search import Search

graph, agents = Reader.read('testcase/input.txt')
print(graph.width, graph.height)
print('\n'.join(' '.join(str(cell) for cell in row) for row in graph.toll))
print()
print('\n'.join(' '.join(str(cell) for cell in row) for row in graph.fuel))
print()

for agent in agents:
	print(agent.start, agent.end, agent.time, agent.fuel)

agent = Agent(agents[1].start, agents[1].end)
print(agents[0].time)

pred = {
	(1, 2): (1, 1),
	(3, 3): (1, 2),
	(6, 9): (3, 3),
	(5, 4): (6, 9),
	(2, 1): (5, 4),
	(7, 8): (2, 1)
}

print(Search().trace(pred, agent.start, agent.end))