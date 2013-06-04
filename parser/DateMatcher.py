import string
from TemplateMatcher import *

SEEKING_OFFSET=15
# The following describes the possible date formats to match
# This should be rather generic to all the documents
# The template matching algorithm finds the template match with the highest confidence
MONTHS = ['januar', 'februar', 'marts', 'april', 'maj', 'juni', 'juli', 'august', 'september', 'october', 'november', 'december']
DATE_FORMATS = [ [{'k':['den'], 't':'p'}, {'k':['$.', '$$.'], 't':'d'}, {'k':MONTHS, 't':'m'}, {'k':['$$$$'],'t':'y'}],	# den 2. januar 1997
		 [{'k':['d.'], 't':'p'}, {'k':map(lambda c:'$$.'+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}],	# d. 3.januar 1997
		 [{'k':map(lambda c:'$. '+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}], # 3.januar 1997
		 [{'k':map(lambda c:'$$. '+c, MONTHS), 't':'d.m'}, {'k':['$$$$'],'t':'y'}], # 20. januar 1987
		 [{'k':['den $$.$$.$$', 'den $.$$.$$', 'den $$.$.$$', 'den $.$.$$'], 't':'p d.m.y'}],  # den 1.2.87
		 [{'k':['$$.$$.$$', '$.$$.$$', '$$.$.$$', '$.$.$$'], 't':'d.m.y'}], # 1.2.97
		 [{'k':map(lambda c:'$$.'+c, MONTHS), 't':'d.m'}, {'k':['$$$$'], 't':'y'}],			# 9.januar 1987
	       ]

class DateMatcher:
	tm = None
	# Initialize a new template matcher
	def __init__(self):
		global DATE_FORMATS, SEEKING_OFFSET
		self.tm = TemplateMatcher(DATE_FORMATS, SEEKING_OFFSET)
	# Preprocess our input buffer for common mistakes
	def preprocess(self, str1):
		new = str1.replace("l9", "19") # l991 => 1991
		#new = self.tm.preprocess(str1)
		return new

	# Run the template matcher
	def locate_date(self, origstring, confidence):
		return self.tm.locate_template(origstring, confidence)	
