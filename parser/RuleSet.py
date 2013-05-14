from DateMatcher import *
from StringMatcher import *
from TimeMatcher import *
from RuleInstance import *
from Rule import *
import re

class RuleSet:
	ruleset = None
	def __init__(self, ruleset):
		self.ruleset = ruleset
	
	def tokenize(self, buf):
		tokens = re.findall(r"\w+|[^\w\s]", buf, re.UNICODE)
		return tokens

	def runRule(self, buf, index, r):
		curindex = index
		sm = StringMatcher()
		dm = DateMatcher()
		tm = TimeMatcher()
		ri = RuleInstance(r)
		if r.getType() == 'stringmatch':
			p = sm.seek_until_keys(buf[curindex:], r.getKeys(), r.getExpectedConfidence())
			if p[0] != -1: # Found something
				ri.addMatchedKeys(r.getType(), [p[1], p[2]])
				curindex += (p[0]+len(p[1]))
		elif r.getType() == 'datematch':
			p = dm.locate_date(buf[curindex:], r.getExpectedConfidence())
			if p[0] != -1:
				ri.addMatchedKeys(r.getType(), [p[1], p[2]])
				curindex += p[0]
		elif r.getType() == 'timematch':
			p = tm.locate_time(buf[curindex:], r.getExpectedConfidence())
			if p[0] != -1:
				print "Time offset: ",curindex," and ",p[0]," = ", curindex+p[0]
				ri.addMatchedKeys(r.getType(), [p[1], p[2]])
				curindex += p[0]

		return (curindex, ri)

	def runRules(self, buf, index, rules):
		curindex = index
		for r in rules:
			(curindex, ri) = self.runRule(buf, curindex, r)
			



	def run(self, ruletree, buf, curindex, ruleinstances):
		for rt in ruletree:
			print "Running "+rt['rule']+" index:",curindex
			r = self.ruleset[rt['rule']]
			(curindex, ri) = self.runRule(buf, curindex, r)
			ruleinstances.append(ri)
		
			# Check wether the value is within our confidence interval
			newrt = rt[ri.validate()]
			if newrt:
				(curindex, ruleinstances) = self.run([newrt], buf, curindex, ruleinstances)	

		return (curindex, ruleinstances)
