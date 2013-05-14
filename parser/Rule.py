class Rule:
	rtype = ""
	rkeys = []
	rconfidence = 0.0
	def __init__(self, rtype, rkeys, expectedconfidence):
		self.rtype = rtype
		self.rkeys = rkeys
		self.rconfidence = expectedconfidence

	def getType(self):
		return self.rtype
	def getKeys(self):
		return self.rkeys
	def getExpectedConfidence(self):
		return self.rconfidence
