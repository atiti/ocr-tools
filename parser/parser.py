#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, string, codecs
from StringMatcher import *
from RuleSet import *
from Rule import *
from RuleInstance import *
from SpellChecker import *
from DateParser import *
from Record import *
from XLSProcessor import *
from HOCRParser import *
from kitchen.text.converters import getwriter
from time import strftime
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)

xls = XLSProcessor('out.xls')
xls.save()
s = StringMatcher()

#  Could be something like this
#
#                             programtype
#                           >0.9 /    \  <0.9
#                            date    fail
#                      >0.7 /   \  <0.7
#                        time   fail
#                      / | |  \
#                             fail
#




ruleset = {'programtype': Rule('programtype', 'stringmatch', [u'NYHEDSMAGASINET', u'MORGENREDAKTIONEN', u'SØNDAGSAVISEN', u'TV-AVISEN', u'RADIOAVISEN', u'P2-MORGENMAGASINET', u'GO\' MORGEN P3'], 0.8),
	   'airdate': Rule('airdate', 'stringmatch', [u'Mandag', u'Tirsdag', u'Onsdag', u'Torsdag', u'Fredag', u'Lørdag', u'Søndag'], 0.7),
	   'date': Rule('date', 'datematch', [], 0.85),
	   'time': Rule('time', 'timematch', [], 0.75),
	  }

ruletree = [ {'rule': 'programtype', True: {'rule':'airdate', True: None, 
							      False:None}, 
				     False:None}, 
 	     {'rule': 'date', True: None, False: None},
	     {'rule': 'time', True: None, False: None} ]
	   #  {'rule': 'airdate', True: None, False: None} ] 


def format_block_text(t):
	newtxt = re.sub(r'(\w)\n(\w)', r'\1 \2', t, flags=re.UNICODE)  # Get rid of "ordinary" line wraps
	newtxt = re.sub(r'(\w)(-)\n(\w)', r'\1\3', newtxt, flags=re.UNICODE) # Get rid of line split wraps
	return newtxt

PREFIX=sys.argv[1]
files = os.listdir(PREFIX)
files.sort()

dateparse = DateParser()
spell = SpellChecker("da")
hocr = HOCRParser()

records = []
num_files = 0
num_matched = 0
# Loop though the files
for f in files:
	if f.find(".txt") < 0:
		continue
	# Read in the TXT file
	fd = codecs.open(PREFIX+f, "r", "utf-8")
	buff = fd.read()
	fd.close()

	# Read in the HOCR file
	has_hocr = True
	hbuff = ""
	try:
		fd = codecs.open(PREFIX+f.replace(".txt", ".html"), "r", "utf-8")
		if not fd:
			has_hocr = False
		else:
			hbuff = fd.read()
			fd.close()
	except:
		has_ocr = False
		ocr_conf = 0
	print "========================================================================================"
	print f, type(buff)

	# Calculate the OCR confidence
	if has_hocr:
		ocr_words = hocr.run(hbuff)
		totalconf = 0
		numwords = 0
		for w in ocr_words:
			if len(w.txt) < 2:
				continue
			totalconf += w.confidence
			numwords += 1
		if numwords > 0:
			ocr_conf = round(float(totalconf)/numwords, 2)
	else:
		ocr_conf = 0

        # Check if the page is empty!
        if len(buff) < 10:
                print "Empty page:",f
		print ""
		
                continue

        # Spell checker?
        #print f
        #spell.checkText(buff)

        # Analysis
        rs = RuleSet(ruleset)
        curindex = 0
        ruleinstances = []
        (curindex, ruleinstances) = rs.run(ruletree, buff, curindex, ruleinstances)

	print "----------------------------------------------------------------------------------------"
	print "Results:"
	print ""

        matched = 1
	has_empty = 0
	confidence_sum = 0
	confidence_cnt = 0
        newrecord = Record()

	header_start_pos = 0
	header_end_pos = 0
	body_start_pos = 0
	body_end_pos = 0
	for r in ruleinstances:
                m = r.getMatchedKeys()
		if len(m.keys()) < 1:
			has_empty = 1
			continue

		array = m[r.getRule().getType()]
                date = [0,0,0]
                timerange = [0,0,0,0]

                # Parse values
                try:
			if r.getRule().getName() == "programtype":
				newrecord.title = array[0]	
                	elif r.getRule().getType() == "datematch":
                        	date = dateparse.parseDate(array)
				# Concatenate to get the original string
				newrecord.date_org = ""
				for v in array[0]:
					newrecord.date_org += v[0]+" "
				newrecord.date_org = newrecord.date_org.replace("\n", "")
				#newrecord.date_new = str(date[0])+"/"+str(date[1])+"/"+str(date[2])
			
				# Validate the dates	
				if (date[0] <= 0 or date[0] > 31):
					newrecord.date_valid = False
				if (date[1] <= 0 or date[1] > 12):
					newrecord.date_valid = False
				if (date[2] <= 1920 or date[2] > int(strftime("%Y"))):
					newrecord.date_valid = False				

				# New parsed string
				newrecord.date_new = "%02d/%02d/%d" % (date[0], date[1], date[2])
				
				# Header starts right after the date!
				header_start_pos = array[3]-1 # Index to the end of the string
 
                        elif r.getRule().getType() == "timematch":
                        	timerange = dateparse.parseTime(array)
                		# Concatenate to get the original string
				newrecord.time_org = ""
				for v in array[0]:
					newrecord.time_org += v[0]+" "
				newrecord.time_org = newrecord.time_org.replace("\n", "")
				# Validate the time
				if (timerange[0] > 24 or timerange[0] < 0):
					newrecord.time_valid = False
				if (timerange[1] > 59 or timerange[1] < 0):
					newrecord.time_valid = False
				if (timerange[2] > 24 or timerange[2] < 0):
					newrecord.time_valid = False
				if (timerange[3] > 59 or timerange[3] < 0):
					newrecord.time_valid = False

				# New parsed string
				newrecord.time_new = "%02d.%02d.00" % (timerange[0], timerange[1])

				if timerange[2] != 0 or timerange[3] != 0:
					if timerange[2] < timerange[0]: # Check whether we lapse over to another day
						timerange[2] += 24 # Append 24 hours to our second range
					# Calculate the new duration
					duration = (timerange[2] - timerange[0])*60 + (timerange[3]-timerange[1])
					# Duration in minutes to hour and minutes
					duration_h = duration / 60
					duration_m = duration % 60
					newrecord.duration = "%02d.%02d.00" % (duration_h, duration_m)
				
				# Header stops right before the time.
				header_end_pos = array[2]
				# Body starts right after the time
				body_start_pos = array[3]-1
				
		except:
			traceback.print_exc()

		

		print r.getRule().getName(),":",r.getRule().getType(),":",m
		
		# Calculating total confidence
		confidence_sum += array[1]
		confidence_cnt += 1

	# Total record confidence calculation
	total_confidence = round((float(confidence_sum)/float(confidence_cnt))*100, 2)
	newrecord.confidence = total_confidence
	newrecord.ocr_confidence = ocr_conf
	print "Total confidence: "+str(total_confidence)+"%"
	print "Total OCR confidence: "+str(ocr_conf)+"%"	

	# Fill out date time
	# TODO: Some sort of datatype here?
	newrecord.datetime = newrecord.date_new+" "+newrecord.time_new

	# Calculate page index
	backside = 0
	fnum = f.split("_") # Split up the filename into parts
	if len(fnum) < 2:
		fnum = f.split(" - ")
	
	if len(fnum) > 1:
		fnum = int(fnum[len(fnum)-1].replace(".txt", "")) # Strip the .txt at the end and cast to integer
		if fnum % 2 == 0:
			backside = 1

	if not backside:
		# Fill out the header from the front page
		# The header is between the date stamp and the time stamp usually
		newrecord.header = buff[header_start_pos:header_end_pos].strip('\n')		
		# Fill out the body:
		# The body is the text after the timestamp
		if body_end_pos == 0:
			body_end_pos = len(buff)
		newrecord.body = format_block_text(buff[body_start_pos:body_end_pos].strip('\n'))

		newrecord.images += f.replace(".txt", "") # Append pages and remove extension

		# Validate field values in a record
		if not newrecord.validate():
			newrecord.confidence = 0

		print newrecord.display()
		records.append(newrecord)
	# If it's the backside then append the text to the previous' body, and add the side file
	else:
		# Check if we could use something from the backside to make our metadata more correct
		oldrecord = records[len(records)-1]
		if oldrecord.date_new == "00/00/0":
			oldrecord.date_new = newrecord.date_new
			oldrecord.datetime = newrecord.datetime
		if oldrecord.time_new == "00.00.00":
			oldrecord.time_new = newrecord.time_new
			oldrecord.datetime = newrecord.datetime	

		# Clean up the temporary record for the backside
		del newrecord
		newrecord = oldrecord
		newrecord.body += format_block_text(buff)
		newrecord.images += ", "+f.replace(".txt", "")   # Append pages and remove extension
		print newrecord.display()
	# Check if the record is complete!
	if has_empty:
		if not backside:
			matched = 0
			print "FAILED",f
       	        	print "----------------------------------------------------------------------------------------"
       	        	print buff
                	print "----------------------------------------------------------------------------------------"
		else:
			print "Backside for",f
		
	print "END"

	print ""	
	if matched:
		num_matched +=1
	num_files += 1


for r in records:
	xls.add_item(r)

xls.save()

print num_files," files,",num_matched,"matched,",round((float(num_matched)/float(num_files))*100, 2),"% coverage"
