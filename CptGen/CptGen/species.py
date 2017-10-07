import numpy as np

class SpeciesCpt:
	__metaclass__ = ABCMeta

	@abstractmethod
	def score():
		pass

	@abstractmethod
	def next_move():
		pass

class FirstSpecies(SpeciesCpt):

	def __init__(self, cf):
		self.cf = cf
		self.cpt = [None for i in cf]
		
	@staticmethod
	def score(cpt):

