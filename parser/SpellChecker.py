from pyaspell import *
import string

class SpellChecker:
	aspell = None
	def __init__(self, language):
		self.aspell = Aspell(("lang", language))
	
	def check(self, word):
		return self.aspell.check(word)

	def suggest(self, word):
		return self.aspell.suggest(word)

	def checkText(self, text):
		words = string.split(text, " ")
		for w in words:
			if len(w) < 2:
				continue

			if not self.check(w):
				sugg = self.suggest(w)
				print "Spell failed for word", w, "Suggestions:",repr(sugg)

	
