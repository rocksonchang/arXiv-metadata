'''
arXiv-metadata-reOrder.py (beta) --- 25 June 2016
-------------------------------------------------
This script has been coded for Python3.

The metadata consists of the following entries:
	dc:title
	dc:creator (authors)
	dc:subject (keywords)
	dc:description (abstract)
	dc:date (date of submission)
	dc:identifier (final publishing locations)

'''


from xml.dom import minidom
from itertools import chain
from datetime import datetime
import numpy as np

## blocks of data based on metadata update date
#fname = 'arXiv-meta-block1.xml'; # from 2007-01-01 to 2009-12-31
#fname = 'arXiv-meta-block2.xml'; # from 2010-01-01 to 2012-12-31
#fname = 'arXiv-meta-block3.xml'; # from 2013-01-01 to 2015-12-31
#fname = 'arXiv-meta-block4.xml'; # from 2016-01-01 to 2018-12-31 

for block in range(4,5):
	fname ='arXiv-meta-block{}.xml'.format(block)
	## parse XML data and test some outputs
	data = minidom.parse(fname)
	## pull out data
	titles       = data.getElementsByTagName("dc:title")
	creators     = data.getElementsByTagName("dc:creator")
	descriptions = data.getElementsByTagName("dc:description")	
	dates        = data.getElementsByTagName("dc:date")
	ids          = data.getElementsByTagName("dc:identifier")
	
	print(len(titles))
	print(len(dates))
	print(len(ids))
	dateList=[]
	titleList=[]
	descList=[]
	#for i in chain(range(0,len(dates))):
	for i in chain(range(0,100)):
		#print titles[i].firstChild.data
		#print dates[i].firstChild.data
		date  = datetime.strptime(dates[i].firstChild.data,'%Y-%m-%d')				
		title = titles[i].firstChild.data
		desc  = descriptions[i].firstChild.data
		
		dateList.append(date)
		titleList.append(title)
		descList.append(desc)

	keys = range(0,len(dates))	
	#dateDict = dict(list(zip(dateList,keys)))
	dateDict = dict(list(zip(dateList,titleList)))
	s=sorted(dateDict.keys())
	for key in s:
		print(key, dateDict[key])

