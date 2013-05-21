class Rule:
	rname = ""
	rtype = ""
	rkeys = []
	rconfidence = 0.0
	def __init__(self, rname, rtype, rkeys, expectedconfidence):
		self.rname = rname
		self.rtype = rtype
		self.rkeys = rkeys
		self.rconfidence = expectedconfidence
	def getName(self):
		return self.rname
	def getType(self):
		return self.rtype
	def getKeys(self):
		return self.rkeys
	def getExpectedConfidence(self):
		return self.rconfidence
