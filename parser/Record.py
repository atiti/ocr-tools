class Record:
	title = ""
	time_org = ""
	time_new = ""
	duration = ""
	date_org = ""
	date_new = ""
	datetime = ""
	header = ""
	body = ""
	images = ""
	confidence = 0.0

	def __init__(self):
		pass

	def display(self):
		print "************************"
		print "Title:\t "+self.title
		print "Time orig:\t "+self.time_org
		print "Time new:\t "+self.time_new
		print "Duration:\t "+self.duration
		print "Date orig:\t "+self.date_org
		print "Date new:\t "+self.date_new
		print "DateTime:\t "+self.datetime
		print "Header:\t "+self.header
		print "Body:\t "+self.body
		print "Images:\t "+self.images
		print "Confidence:\t "+str(self.confidence)
		print "*************************"
