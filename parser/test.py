#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys, string, codecs
from StringMatcher import *
from RuleSet import *
from Rule import *
from RuleInstance import *
from SpellChecker import *
from kitchen.text.converters import getwriter
UTF8Writer = getwriter('utf8')
sys.stdout = UTF8Writer(sys.stdout)


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




ruleset = {'programtype': Rule('stringmatch', [u'NYHEDSMAGASINET', u'MORGENREDAKTIONEN', u'SØNDAGSAVISEN', u'TV-AVISEN', u'RADIOAVISEN', u'P2-MORGENMAGASINET', u'GO\' MORGEN P3'], 0.8),
	   'airdate': Rule('stringmatch', [u'Mandag', u'Tirsdag', u'Onsdag', u'Torsdag', u'Fredag', u'Lørdag', u'Søndag'], 0.7),
	   'date': Rule('datematch', [], 0.85),
	   'time': Rule('timematch', [], 0.7),
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

spell = SpellChecker("da")

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
        for r in ruleinstances:
                m = r.getMatchedKeys()
		print r.getRule().getType(),":",m
		if len(m.keys()) < 1:
			has_empty = 1
	
	if has_empty:
		backside = 0
		fnum = f.split("_")
		if len(fnum) > 1:
			fnum = int(fnum[1].replace(".txt", ""))
			if fnum % 2 == 0:
				backside = 1

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

print num_files," files,",num_matched,"matched,",round((float(num_matched)/float(num_files))*100, 2),"% coverage"
