from datetime import datetime, date, time
import re
import traceback

MONTHS = ['januar', 'februar', 'marts', 'april', 'maj', 'juni', 'juli', 'august', 'september', 'october', 'november', 'december']

class DateParser:
	def __init__(self):
		pass

	# Preprocess string
	def preprocess(self, txt):
		txt = txt.replace("l", "1") # Replace l => 1  For example: l997
		txt = txt.replace("q", "0") # Replace Q => 0  For example: Kl. 1Q.QQ
		return txt

	# Filter out only digits
	def getDigits(self, txt):
		return re.sub(r'[^\d]', '', txt)

	# Return the month number
	def getMonth(self, txt):
		global MONTHS
		d = self.getDigits(txt)
		if len(d) == 0:
			txt = txt.lower().strip()
			cnt = 1
			for m in MONTHS:
				if m == txt:
					break
				cnt += 1
			return cnt
		else:
			return len(d)

	def getDayMonth(self, txt):
		txt = txt.lower().strip() # Lower case the string
		s = txt.split(".")
		# We have a dot in the string
		if len(s) <= 1:
			s = txt.split(" ")

		if len(s) > 1:
			daystr = s[0]
			monthstr = s[1]
			month = self.getMonth(monthstr)
			try:
				day = int(self.getDigits(self.preprocess(daystr)))
				if month > 12 or day > 31:
					return [0,0]
			except:
				traceback.print_exc()
				return [0,0]
			return [day,month]	
		
		return [0,0] 
		
	def getDayMonthYear(self, txt):
		txt = txt.lower().strip()
		s = txt.split(".")
		if len(s) < 3:
			return [0,0,0]

		daystr = s[0]
		monthstr = s[1]
		yearstr = s[2]
	
		try:
			day = int(self.getDigits(self.preprocess(daystr)))
			month = self.getMonth(monthstr)
			year = int(self.getDigits(self.preprocess(yearstr)))
			return [day, month, year]
		except:
			return [0,0,0]

		return [0,0,0]

	def getHourMinute(self, txt):
		txt = txt.lower().strip().replace(":", ".") # Let's make ' 00:00 ' => '00.00' 
		s = txt.split(".")
		# Invalid time format
		if len(s) < 2:
			return [0,0]

		try:
			hour = int(self.getDigits(self.preprocess(s[0])))
			minute = int(self.getDigits(self.preprocess(s[1])))
			return [hour, minute]
		except:
			traceback.print_exc()

		return [0, 0]

	def getHourMinuteRange(self, txt):
		txt = txt.lower().strip()
		s = txt.split("-")
		# Invalid time range format
		if len(s) < 2:
			return [0,0,0,0]
		
		try:
			[hour, minute] = self.getHourMinute(s[0])
			[hour2, minute2] = self.getHourMinute(s[1])
			return [hour, minute, hour2, minute2]
		except:
			traceback.print_exc()
	
		return [0,0,0,0]			

	# Parse the date based on the extracted templates
	def parseDate(self, d1):
		day = 0
		month = 0
		year = 0		
		d = d1[0]
		for a in d:
			# template
			template = a[2]
			# Confidence
			confidence = a[1]
			# Value
			value = a[0]

			if template == 'd':  # Day
				day = int(self.getDigits(value))
				#print value, self.getDigits(value)		
			elif template == 'm':  # Month
				month = self.getMonth(value)
				#print value, self.getMonth(value)
			elif template == 'y':  # Year
				year = int(self.getDigits(value))
				#print value, self.getDigits(value)
			elif template == 'd.m': # Day and month
				[day, month] = self.getDayMonth(value)
				#print "Day month: ",day,month
			elif template == 'd.m.y': # Day month year
				[day, month, year] = self.getDayMonthYear(value)
				#print "Day month year:", value
			elif template == 'p d.m.y': # Prefix day month year
				print "Prefix day month year:", value

		return [day, month, year]

	# Parse time or timerange based on extracted templates
	def parseTime(self, t1):
		hour = 0
		mins = 0
		hour2 = 0
		mins2 = 0
		t = t1[0]
		for a in t:
			# template
			template = a[2]
			# confidence
			confidence = a[1]
			# value
			value = a[0]
			if template == 'h.m':
				[ hour, mins ] = self.getHourMinute(value)
			elif template == 'p h.m' or template == 'p. h.m.':  # Example: [[[u'Kl. 09:00.', 0.9, 'p. h.m.']]
				s = value.split(" ")
				if len(s) > 1:
					[ hour, mins ] = self.getHourMinute(s[1])
			elif template == 'h.m-h.m':
				[ hour, mins, hour2, mins2 ] = self.getHourMinuteRange(value)
		return [hour, mins, hour2, mins2]
