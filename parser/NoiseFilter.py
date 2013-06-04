# -*- coding: utf-8 -*-

class NoiseFilter:
	def run(self, buff):
		b = buff.split("\n")
		for l in b:
			self.per_line_filter(l)

	""" Crude line-by-line noise filter """
	def per_line_filter(self, a):
		if len(a) == 0:
			return
		noisecnt = 0
		validcnt = 0
		for v in a:
			if (v == ' ' or v == '\n'):
				continue
			elif (v >= 'a' and v <= 'z') or (v >= '0' and v <= '9') or (v >= 'A' and v <='Z') or v == u'å' or v == u'ø' or v == u'æ':
				print v
				validcnt += 1
			else:
				noisecnt += 1



		validratio = float(validcnt)/len(a)
		noiseratio = float(noisecnt)/len(a)
		#if validratio < 0.65:
		print a,"\t|\t",validratio, noiseratio


	
