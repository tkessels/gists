import math
x=1
notfound=1
while notfound:
	silber=math.pow(x,2)
	ungerade=math.floor(silber/16.)%2
	rest=silber%16
#	print str(silber) + " " + str(ungerade)
	if ungerade == 1 and rest>1 and rest<9:
		print "rest passt"
		print x
		print silber
		print rest
		print 16-rest
		notfound=0
	x+=1

