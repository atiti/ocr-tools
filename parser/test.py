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
from kitchen.text.converters import getwriter
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

PREFIX=sys.argv[1]
files = os.listdir(PREFIX)
files.sort()

dateparse = DateParser()
spell = SpellChecker("da")


records = []
num_files = 0
num_matched = 0
# Loop though the files
for f in files:
	# Read in the file
	fd = codecs.open(PREFIX+f, "r", "utf-8")
	buff = fd.read()
	fd.close()

	print "========================================================================================"
	print f, type(buff)

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
				# New parsed string
				#newrecord.date_new = str(date[0])+"/"+str(date[1])+"/"+str(date[2])
				newrecord.date_new = "%02d/%02d/%d" % (date[0], date[1], date[2])
                        elif r.getRule().getType() == "timematch":
                        	timerange = dateparse.parseTime(array)
                		# Concatenate to get the original string
				newrecord.time_org = ""
				for v in array[0]:
					newrecord.time_org += v[0]+" "
				newrecord.time_org = newrecord.time_org.replace("\n", "")
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

		except:
			traceback.print_exc()

		

		print r.getRule().getName(),":",r.getRule().getType(),":",m
		
		# Calculating total confidence
		confidence_sum += array[len(array)-1]
		confidence_cnt += 1

	# Total record confidence calculation
	total_confidence = round((float(confidence_sum)/float(confidence_cnt))*100, 2)
	newrecord.confidence = total_confidence
	print "Total confidence: "+str(total_confidence)+"%"

	# Fill out date time
	# TODO: Some sort of datatype here?
	newrecord.datetime = newrecord.date_new+" "+newrecord.time_new

	# Calculate page index
	backside = 0
	fnum = f.split("_") # Split up the filename into parts
	if len(fnum) > 1:
		fnum = int(fnum[1].replace(".txt", "")) # Strip the .txt at the end and cast to integer
		if fnum % 2 == 0:
			backside = 1
			

#	newrecord.display()	
	if not backside:
		newrecord.images += f 
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
		newrecord.body += buff	
		newrecord.images += ", "+f
		newrecord.display()
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
