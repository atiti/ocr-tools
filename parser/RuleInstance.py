class RuleInstance:
	rule = None
	matchedkeys = {}
	def __init__(self, rule):
		self.rule = rule
		self.matchedkeys = {}
	def addMatchedKeys(self, key, conf):
		self.matchedkeys[key] = conf
	def getMatchedKeys(self):
		return self.matchedkeys
	def getRule(self):
		return self.rule
	def validate(self):
		if len(self.matchedkeys.keys()) == 0:
			return False

		expconf = self.rule.getExpectedConfidence()

		#print self.matchedkeys

		for k,v in self.matchedkeys.iteritems():
			if v >= expconf:
				return True

		return False
	
