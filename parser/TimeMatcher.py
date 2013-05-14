import string
from TemplateMatcher import *

SEEKING_OFFSET=200
TIME_FORMATS = [
                 [{'k':['Kl', 'kl', 'Kl ', 'kl '], 't':'p'}, {'k':['$$.$$-$$.$$', '$.$-$.$', '$$:$$-$$:$$', '$:$-$:$'], 't':'h.m-h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
                 [{'k':['\nKl.', '\nkl.'], 't':'p'}, {'k':['$$.$$-$$.$$', '$.$-$.$', '$$:$$-$$:$$', '$:$-$:$'], 't':'h.m-h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
                 [{'k':['Kl.', 'kl.', 'Kl. ', 'kl. '], 't':'p'}, {'k':['$$.$$-$$.$$', '$.$-$.$', '$$:$$-$$:$$', '$:$-$:$'], 't':'h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
 
		 [{'k':['Kl', 'kl', 'Kl ', 'kl '], 't':'p'}, {'k':['$:$', '$$:$', '$:$$', '$$:$$'], 't':'h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
		 [{'k':['\nKl.', '\nkl.'], 't':'p'}, {'k':['$$.$$', '$$.$', '$.$$', '$.$'], 't':'h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
		 [{'k':['Kl.', 'kl.', 'Kl. ', 'kl. '], 't':'p'}, {'k':['$.$', '$$.$', '$.$$', '$$.$$'], 't':'h.m'}, {'k':['.', ':', '\n'], 't':'p'}],
		 [{'k':['kl. $$.$$.'], 't':'p. h.m.'}],
		 [{'k':['kl. $.$$.'], 't':'p. h.m.'}],
		 [{'k':['kl. $.$.'], 't':'p. h.m.'}],
		 [{'k':['kl. $$.$.'], 't':'p. h.m.'}],
	       ]

class TimeMatcher:
	tm = None
	def __init__(self):
		global TIME_FORMATS, SEEKING_OFFSET
		self.tm = TemplateMatcher(TIME_FORMATS, SEEKING_OFFSET)
	def preprocess(self, str1):
		return str1
		#new = self.tm.preprocess(str1)
		#return new

	def locate_time(self, origstring, confidence):
		return self.tm.locate_template(origstring, confidence)	
