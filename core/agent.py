# agent.py
# =============================================================================
#  A simple agent that has a start and end coordinates with time and fuel
#  constraints.
# =============================================================================

class Agent:
	def __init__(self, start: tuple, end: tuple, time = None, fuel = None):
		self._start = start
		self._end = end
		self._optimize_time = False
		self._optimize_fuel = False

		if time is not None:
			self._optimize_time = True
			self._time = time

		if fuel is not None:
			self._optimize_fuel = True
			self._fuel = fuel

	@property
	def start(self):
		return self._start

	@property
	def end(self):
		return self._end
	
	@property
	def optimize_time(self):
		return self._optimize_time
	
	@property
	def optimize_fuel(self):
		return self._optimize_fuel

	@property
	def time(self):
		if not self.optimize_time:
			raise AttributeError('Agent does not have time constraint.')
		return self._time

	@property
	def fuel(self):
		if not self.optimize_fuel:
			raise AttributeError('Agent does not have fuel constraint.')
		return self._fuel