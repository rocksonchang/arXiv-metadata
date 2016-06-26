'''
arXiv-metadata-process.py --- 26 June 2016
-------------------------------------------------
This script has been coded for Python3.

The metadata consists of the following entries:
	dc:title
	dc:creator (authors)
	dc:subject (keywords)
	dc:description (abstract)
	dc:date (date of submission)
	dc:identifier (final publishing locations)

## blocks of data based on metadata update date
#fname = 'arXiv-meta-block1.xml'; # from 2007-01-01 to 2009-12-31
#fname = 'arXiv-meta-block2.xml'; # from 2010-01-01 to 2012-12-31
#fname = 'arXiv-meta-block3.xml'; # from 2013-01-01 to 2015-12-31
#fname = 'arXiv-meta-block4.xml'; # from 2016-01-01 to 2018-12-31 

'''

#################################################################################################
#################################################################################################
from xml.dom import minidom
#from xml.dom.minidom import Document
from itertools import chain
from datetime import datetime
import time
## throwing down some code I don't yet understand regarding non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#creators=[]
addys=[]
titles=[]
descriptions=[]
dates=[]
for year in range(1992,2017):
	fname ='arXiv-meta-{}.xml'.format(year)	
	## parse XML data
	data = minidom.parse(fname)		
	NEntries=0		
	for rec in data.getElementsByTagName('record'):			
		NEntries+=1
		## extract data
		#t_creators=()
		#for c in rec.getElementsByTagName("dc:creator"):			
		#t_creators=t_creators+(c.firstChild.data,)
		rec_dates=[]
		for d in rec.getElementsByTagName("date"):
			rec_dates.append(d.firstChild.data)		
		rec_ids=[]
		for i in rec.getElementsByTagName("identifier"):
			rec_ids.append(i.firstChild.data)			
			
		#print(rec.getElementsByTagName("dc:title")[0].firstChild.data)			

		## append data from this record into a larger running array across all blocks
		#creators.append(t_creators)
		addys.append(rec.getElementsByTagName("identifier")[0].firstChild.data)
		titles.append(rec.getElementsByTagName("title")[0].firstChild.data)
		descriptions.append(rec.getElementsByTagName("description")[0].firstChild.data)
		dates.append(rec_dates[0]) # take date first submitted as date.
	print ('Loading year: {}; Num. entries: {}'.format(year,NEntries))
'''
## output some stuff to check	
print('\n')		
for i in range(len(titles)):
	print(titles[i])
	print(dates[i])
	print(descriptions[i])
	print('\n')	
'''