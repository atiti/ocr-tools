from Record import *
import xlwt 


XLS_TITLES = ['TITEL', 'CONFIDENCE', 'TIME_ORG', 'TIME_NEW', 'DURATION', 'DATE_ORG', 'DATE_NEW', 'DATETIME', 'COLOPHON', 'DESCRIPTION', 'IMAGES']

class XLSProcessor:
	filename = ""
	workbook = None
	worksheet = None
	cur_row = 0
	cur_col = 0
	def __init__(self, filename):
		global XLS_TITLES
		self.filename = filename
		self.workbook = xlwt.Workbook(encoding='utf-8')
		self.worksheet = self.workbook.add_sheet("Parser")
			
		# Create bold font for spreadsheet
		font = xlwt.Font() 
		font.name = 'Arial'
		font.bold = True
		font.underline = True
		font.italic = False
		style = xlwt.XFStyle()
		style.font = font

		self.cur_row = 0
		self.cur_col = 0
		for i in range(0, len(XLS_TITLES)):
			self.worksheet.write(self.cur_row, i, XLS_TITLES[i], style)
		self.cur_row += 1

	def add_item(self, record):
		self.cur_col = 0
		self.worksheet.write(self.cur_row, self.cur_col, record.title) # Write the title
		self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.confidence) # Write the confidence
                self.cur_col += 1		
		self.worksheet.write(self.cur_row, self.cur_col, record.time_org) # Write the time_org
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.time_new) # Write the time_new
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.duration) # Write the duration
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.date_org) # Write the date_org
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.date_new) # Write the date_new
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.datetime) # Write the datetime
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.header) # Write the header
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.body) # Write the body
                self.cur_col += 1
		self.worksheet.write(self.cur_row, self.cur_col, record.images) # Write the images
		self.cur_row += 1

	def save(self):
		print "Saving as ",self.filename
		self.workbook.save(self.filename)
		
		
