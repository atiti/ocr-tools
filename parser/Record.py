""" Record is a datatype to store the extarcted information about the different parameters for one specific program """
class Record:
	channel = ""
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
	ocr_confidence = 0.0
	date_valid = True
	time_valid = True

	def __init__(self):
		pass

	""" Try to validate all the fields, if some missing, set the confidence to 0 """
	def validate(self):
		if len(self.title) < 1:
			return False
		if len(self.time_org) < 1:
			return False
		if len(self.time_new) < 1:
			return False
		if len(self.date_org) < 1:
			return False
		if len(self.date_new) < 1:
			return False
		if len(self.header) < 1:
			return False
		if len(self.body) < 1:
			return False
		if len(self.images) < 1:
			return False
		
		return True		

	""" Overwrite toString() to display the object in a nice way """
	def __str__(self):
		return self.display()

	def display(self):
		""" Display the Record in a user-friendly way """
		outstr = "************************\n"
		outstr += "Title:\t "+self.title+"\n"
		outstr += "Time orig:\t "+self.time_org+"\n"
		outstr += "Time new:\t "+self.time_new+"\n"
		outstr += "Duration:\t "+self.duration+"\n"
		outstr += "Date orig:\t "+self.date_org+"\n"
		outstr += "Date new:\t "+self.date_new+"\n"
		outstr += "DateTime:\t "+self.datetime+"\n"
		outstr += "Header:\t "+self.header+"\n"
		outstr += "Body:\t "+self.body+"\n"
		outstr += "Images:\t "+self.images+"\n"
		outstr += "Confidence:\t "+str(self.confidence)+"\n"
		outstr += "OCR Confidence:\t "+str(self.ocr_confidence)+"\n"
		outstr += "*************************\n"
		return outstr
