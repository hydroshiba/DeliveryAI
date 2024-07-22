# agent.py
# =============================================================================
#  A simple agent that has a start and end coordinates with time and fuel
#  constraints.
# =============================================================================

class Agent:
	def __init__(self, start: tuple, end: tuple, time: int, fuel: int):
		self._start = start
		self._end = end
		self._time = time
		self._fuel = fuel

	@property
	def start(self):
		return self._start

	@property
	def end(self):
		return self._end

	@property
	def time(self):
		return self._time

	@property
	def fuel(self):
		return self._fuel