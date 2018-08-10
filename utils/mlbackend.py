import pickle
import sklearn
import numpy as np

# ML model wrapper functions go here.
class MLBackend():

	def __init__(self, addr):
		self.model = pickle.load(open(addr, 'r'))

	def predict(self, inp):
		return self.model.predict(inp)[0]
	
	def proba_score(self, inp):
		return self.model.predict_proba(inp)[0][1]