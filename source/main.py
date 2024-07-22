from reader import Reader

graph, agents = Reader.read('testcase/input.txt')
print(graph.width, graph.height)
print('\n'.join(' '.join(str(cell) for cell in row) for row in graph.toll))
print()
print('\n'.join(' '.join(str(cell) for cell in row) for row in graph.fuel))
print()
for agent in agents:
	print(agent.start, agent.end, agent.time, agent.fuel)