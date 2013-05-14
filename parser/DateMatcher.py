import string
from TemplateMatcher import *

SEEKING_OFFSET=15
MONTHS = ['januar', 'februar', 'marts', 'april', 'maj', 'juni', 'juli', 'august', 'september', 'october', 'november', 'december']
DATE_FORMATS = [ [{'k':['den'], 't':'p'}, {'k':['$.', '$$.'], 't':'d'}, {'k':MONTHS, 't':'m'}, {'k':['$$$$'],'t':'y'}],	# den 2. januar 1997
		 [{'k':['d.'], 't':'p'}, {'k':map(lambda c:'$$.'+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}],	# d. 3.januar 1997
		 [{'k':map(lambda c:'$. '+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}], # 3.januar 1997
		 [{'k':map(lambda c:'$$. '+c, MONTHS), 't':'d.m'}, {'k':['$$$$'],'t':'y'}], # 20. januar 1987
		 [{'k':['den $$.$$.$$', 'den $.$$.$$', 'den $$.$.$$', 'den $.$.$$'], 't':'p d.m.y'}],  # den 1.2.87
		 [{'k':['$$.$$.$$', '$.$$.$$', '$$.$.$$', '$.$.$$'], 't':'d.m.y'}], # 1.2.97
		 [{'k':map(lambda c:'$$.'+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}],			# 9.januar 1987
	       ]

class Date:
	year = 0
	month = 0
	day = 0

class DateMatcher:
	tm = None
	def __init__(self):
		global DATE_FORMATS, SEEKING_OFFSET
		self.tm = TemplateMatcher(DATE_FORMATS, SEEKING_OFFSET)
	def preprocess(self, str1):
		return str1
		#new = self.tm.preprocess(str1)
		#return new

	def locate_date(self, origstring, confidence):
		return self.tm.locate_template(origstring, confidence)	
