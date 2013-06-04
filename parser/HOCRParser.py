from HTMLParser import HTMLParser

# Sample output:
#
# Start tag: span
# Attr: ('class', 'ocrx_word')
# Attr: ('id', 'word_252')
# Attr: ('title', 'bbox 2702 4628 2706 4634; x_wconf 26')
#


class Word:
	id = ""
	txt = ""
	box = ""
	confidence = 0
	def __init__(self):
		pass
	def __str__(self):
		r = "Word id: "+self.id
		r += "\nWord box: "+self.box
		r += "\nWord conf: "+str(self.confidence)
		r += "\nWord txt: "+self.txt
		r += "\n----------------------------\n"
		return r

""" Our custom HTML parser for HOCR files """
class MyHOCRParser(HTMLParser):
	current_word = None
	def __init__(self, hocr):
		HTMLParser.__init__(self)
		self.hocr = hocr

	def handle_starttag(self, tag, attr):
		if tag == "span":
			box = ""
			conf = ""
			wordid = ""
			word = None
			for a in attr:
				if len(a) > 1:
					if a[0] == 'class' and a[1] == 'ocrx_word':
						word = Word()
					elif a[0] == 'id':
						if word:
							word.id = a[1]
					elif a[0] == 'title':
						b = a[1].split(";")
						if word:
							word.box = b[0].replace("bbox ", "")
							word.confidence = int(b[1].replace("x_wconf", "").strip())	
			self.current_word = word
#		else:			
#			print "Start tag:",tag
#			for a in attr:
#				print "Attr:",a
	def handle_endtag(self, tag):
		#print "End tag:",tag
		if tag == "span":
			self.current_word = None
	def handle_data(self, data):
		if self.current_word:
			self.current_word.txt = data
			self.hocr.words.append(self.current_word)	
#		else:
#			print "Encountered data:",data

class HOCRParser:
	words = []
	def __init__(self):
		self.parser = MyHOCRParser(self)
	def run(self, data):
		self.words = []
		self.parser.feed(data)
		return self.words

