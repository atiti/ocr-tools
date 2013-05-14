import string

class TemplateMatcher:
	seek_offset = 0
	def __init__(self, templates, seek_offset):
		self.formats = templates
		self.seek_offset = seek_offset
	def preprocess(self, str1):
		#new = str1.replace("l", "1") # Replace misdetected 'l' as 1 : l987 => 1987
		new = str1.replace("o", "0")  # Replace misdetected 0 : o2.O2 => 02.02
		new = new.replace("O", "0")  # o2.O2 => o2.02
		new = new.replace("]", "7")  # Replace ] with 7 : 198] => 1987
		return new

	def compare_cs(self, str1, str2, exact):
		confidence = 0
		smallen = len(str2) if len(str1) > len(str2) else len(str1)
		match = 0
		for i in range(0,smallen):
			if exact:
				if str1[i] == str2[i]:
					match += 1
			else:
				if str1[i] == '$' and str2[i] >= '0' and str2[i] <= '9':
					match += 1
				elif str1[i] == '#' and ((str2[i] >= 'a' and str2[i] <= 'z') or (str2[i] >= 'A' and str2[i] <= 'Z')):
					match += 1
				elif str1[i] == str2[i]:
					match += 1
		if smallen == 0:
			return 0
		confidence = float(match) / float(smallen)
		#print str1,"=>",str2,confidence
		return confidence

	def compare_ncs(self, str1, str2, exact):
		return self.compare_cs(str1.lower(), str2.lower(), exact)

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
			conf = self.compare_ncs(origstring[i:], tomatch, 0)
			if conf >= confidence and conf >= found[2]:
				found = (startindex,tomatch, conf)
			startindex += 1
		return found

	def seek_until_keys(self, origstring, tomatch, confidence):
		global SEEKING_OFFSET
		startindex = 0
		stopiter = self.longest_key(tomatch)+SEEKING_OFFSET
		found = (-1, "", 0)
		toindex = len(origstring)+SEEKING_OFFSET
		for i in range(0, toindex):
			for m in tomatch:
				conf = self.compare_ncs(origstring[i:], m, 0)
				print origstring[i:stopiter], "=>", m
				if conf >= confidence and conf >= found[2]:
					found = (startindex, m, conf)
			if i > stopiter:
				break;
			startindex += 1
		return found

	def get_max_confidence(self, strarray, tomatch):
		maxconf = 0
		maxconfword = ""
		maxmatchword = ""
		tomatch = self.preprocess(tomatch)
		for s in strarray:
			conf = self.compare_ncs(s, tomatch, 0)
			#print s,"=>",tomatch[0:len(s)],"   |",conf
			if conf > maxconf:
				maxconf = conf
				maxmatchword = tomatch[0:len(s)]
				maxconfword = s
		return (maxconf, maxmatchword, maxconfword)

	def locate_template(self, origstring, confidence):
		bestmatch = 0
		found = (-1, [], 0)
		startindex = 0
		stopiter = self.seek_offset
		toindex = len(origstring)+self.seek_offset
		for i in range(0, toindex):
			for df in self.formats:
				totalmatch = 0
				maxconf = 0
				cdf = []
				curindex = startindex
				for k in df:
					v = k["k"]
					(conf, matchw, confw) = self.get_max_confidence(v, origstring[curindex:curindex+20])
					#print confw, "=>",origstring[curindex:curindex+20], "   |",conf
					totalmatch += (conf*len(confw))
					maxconf += len(confw)
					#if conf >= confidence:
					cdf.append([matchw, conf, k["t"]])
					curindex += len(confw)+1

				if totalmatch > bestmatch:
					totconf = float(totalmatch)/float(maxconf)
					print "New mest match:",totalmatch,"/",maxconf,"\t",str(round(totconf*100, 2))+"%"
					print repr(cdf)
					bestmatch = totalmatch
					found = (startindex, cdf, totconf)
			if i > stopiter:
				break;
			startindex += 1
		return found
