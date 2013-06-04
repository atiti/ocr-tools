import HOCRParser

fd = open("/tmp/out.html", "r")
buff = fd.read()
fd.close()

h = HOCRParser.HOCRParser()
words = h.run(buff)

totalconf = 0
wcount = 0
for w in words:
	if len(w.txt) > 1:
		totalconf += w.confidence
		wcount += 1


print round(float(totalconf)/wcount, 2)
