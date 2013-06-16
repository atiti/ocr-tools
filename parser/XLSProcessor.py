from Record import *
import xlwt 


XLS_TITLES = ['KANAL', 'TITEL', 'OCR', 'PARSING', 'TIME_ORG', 'TIME_NEW', 'DURATION', 'DATE_ORG', 'DATE_NEW', 'DATETIME', 'COLOPHON', 'DESCRIPTION', 'IMAGES']

class XLSProcessor:
	filename = ""
	workbook = None
	worksheet = None
	cur_row = 0
	cur_col = 0
	basic_style = None
	def __init__(self, filename):
		global XLS_TITLES
		self.filename = filename
		self.workbook = xlwt.Workbook(encoding='utf-8')
		self.worksheet = self.workbook.add_sheet("Parser")
			
		# Create bold font for spreadsheet
		style = xlwt.easyxf('font: bold 1;')

		# Create a standard font
		self.basic_style = xlwt.easyxf('align: wrap on;')	

		self.cur_row = 0
		self.cur_col = 0
		for i in range(0, len(XLS_TITLES)):
			self.worksheet.write(self.cur_row, i, XLS_TITLES[i], style)
		self.cur_row += 1

	def add_item(self, record):
		if (record.confidence < 80):
			badstyle = xlwt.easyxf('align: wrap on; pattern: pattern solid, pattern_fore_colour coral')
		elif record.time_valid == False or record.date_valid == False:
			badstyle = xlwt.easyxf('align: wrap on; pattern: pattern solid, pattern_fore_colour tan')
		else:
			badstyle = self.basic_style

		self.cur_col = 0
		self.worksheet.write(self.cur_row, self.cur_col, record.channel, badstyle) # Write the channel
		self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.title, badstyle) # Write the title
		self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.ocr_confidence, badstyle) 
		self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.confidence, badstyle)
                self.cur_col += 1		
		self.worksheet.write(self.cur_row, self.cur_col, record.time_org, badstyle) # Write the time_org
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.time_new, badstyle) # Write the time_new
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.duration, badstyle) # Write the duration
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.date_org, badstyle) # Write the date_org
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.date_new, badstyle) # Write the date_new
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.datetime, badstyle) # Write the datetime
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.header, badstyle) # Write the header
                self.cur_col += 1
	
		# FIXME: Cut off the rest of the text if it doesn't fit in the column!
		if len(record.body) > 32767:
			body = record.body[0:32766]
		else:
			body = record.body
		self.worksheet.write(self.cur_row, self.cur_col, body, badstyle) # Write the body
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.images, badstyle) # Write the images
		self.cur_row += 1

	def save(self):
		print "Saving as ",self.filename
		self.workbook.save(self.filename)
		
		
