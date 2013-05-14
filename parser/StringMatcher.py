import string
import pprint

SEEKING_OFFSET=150

class StringMatcher:
	def __init__(self):
		pass
	def compare_cs(self, str1, str2):
		confidence = 0
		smallen = len(str2) if len(str1) > len(str2) else len(str1)
		match = 0
		for i in range(0,smallen):
			if str1[i] == str2[i]:
				match += 1

		if smallen == 0:
			return 0
		confidence = float(match) / float(smallen)
		return confidence

	def compare_ncs(self, str1, str2):
		return self.compare_cs(str1.lower(), str2.lower())

	def longest_key(self, keys):
		l = 0
		for k in keys:
			if len(k) > l:
				l = len(k)
		return l

	# Seek until the word is found...
	def seek_until_key(self, origstring, tomatch, confidence):
		startindex = 0
		found = (-1, "", 0)
		for i in range(0, len(origstring)):
			conf = self.compare_ncs(origstring[i:], tomatch)
			if conf >= confidence and conf >= found[2]:
				found = (startindex,tomatch, conf)
			startindex += 1
		return found

	def seek_until_keys(self, origstring, tomatch, confidence):
		global SEEKING_OFFSET
		DEBUG_BUFFER = u""
		startindex = 0
		stopiter = self.longest_key(tomatch)+SEEKING_OFFSET
		found = (-1, "", 0)
		toindex = len(origstring)+SEEKING_OFFSET
		for i in range(0, toindex):
			for m in tomatch:
				conf = self.compare_ncs(origstring[i:], m)
				DEBUG_BUFFER += origstring[i:stopiter]+" => "+m+"\n"
				if conf >= confidence and conf >= found[2]:
					found = (startindex, m, conf)
			if i > stopiter:
				break;
			startindex += 1
		#if found[0] == -1:
		#	print DEBUG_BUFFER
		return found
