'''
arXiv-metadata-reOrder.py --- 25 June 2016
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
from xml.dom.minidom import Document
from itertools import chain # don't think I need chain anymore, delete
from datetime import datetime
import time
## throwing down some code I don't yet understand regarding non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#################################################################################################
#################################################################################################
## Records on local memory -- a list of tuples
myListofTuples=[]
## Run through raw data blocks
for block in range(1,5):
	fname ='arXiv-meta-block{}.xml'.format(block)
	#################################################################################################
	#################################################################################################
	## parse XML data
	data = minidom.parse(fname)	
	## pull out desired data from records, do some basic formatting
	creators=[]
	addys=[]
	titles=[]
	descriptions=[]
	dates=[]
	for rec in data.getElementsByTagName('record'):		
		## error checking if arXiv entry has been deleted
		hstatus = rec.getElementsByTagName("header")[0].getAttribute('status')
		if hstatus!='deleted':			
			t_creators=()
			for c in rec.getElementsByTagName("dc:creator"):			
				t_creators=t_creators+(c.firstChild.data,)
			rec_dates=[]
			for d in rec.getElementsByTagName("dc:date"):
				rec_dates.append(d.firstChild.data)		
			rec_ids=[]
			for i in rec.getElementsByTagName("dc:identifier"):
				rec_ids.append(i.firstChild.data)			
			
			#print(rec.getElementsByTagName("dc:title")[0].firstChild.data)			

			## append data from this record into a larger running array across all blocks
			creators.append(t_creators)
			addys.append(rec.getElementsByTagName("identifier")[0].firstChild.data)
			titles.append(rec.getElementsByTagName("dc:title")[0].firstChild.data)
			descriptions.append(rec.getElementsByTagName("dc:description")[0].firstChild.data)
			dates.append(rec_dates[0]) # take date first submitted as date.

		'''
		## output some stuff to check		
		print(titles)
		for c in rec_creators:
			print(c)
		print(dates)
		#for d in dates:
		#	print(d)
		print('\n')	
		'''
	
	#################################################################################################
	#################################################################################################
	for i in chain(range(0,len(dates))):
	#for i in chain(range(0,10)):		
		date    = datetime.strptime(dates[i],'%Y-%m-%d')				
		addy    = addys[i]
		creator = creators[i]
		title   = titles[i]
		desc    = descriptions[i]
		
		myListofTuples.append((date,addy,title,creator,desc))

#################################################################################################
#################################################################################################
sortedList=sorted(myListofTuples, key=lambda d: d[0])


#################################################################################################
#################################################################################################
previousYear=myListofTuples[0][0].year # first entry
f = open("arXiv-meta-{}.xml".format(previousYear), "w")
doc = Document()
ListRecords = doc.createElement('ListRecords')
doc.appendChild(ListRecords)

#################################################################################################
#################################################################################################
for rec in sortedList:
	'''
	print(rec[2])
	print(rec[0])
	print('\n')
	time.sleep(1)
	'''

	year = rec[0].year	
	if year != previousYear:
		## write previous data and close file
		f.write(doc.toxml(encoding='utf-8'))
		f.close()
		## start a new file
		previousYear=year # new previous entry
		f = open("arXiv-meta-{}.xml".format(year), "w")
		doc = Document()
		ListRecords = doc.createElement('ListRecords')
		doc.appendChild(ListRecords)
	
	#################################################################################################
	#################################################################################################
	
	record = doc.createElement('record')
	ListRecords.appendChild(record)

	header = doc.createElement('header')
	record.appendChild(header)
	identifier = doc.createElement('identifier')
	header.appendChild(identifier)
	identifierData = doc.createTextNode(rec[1])
	identifier.appendChild(identifierData)
	
	## metadata and children
	metadata = doc.createElement('metadata')
	record.appendChild(metadata)
	
	title = doc.createElement('title')
	metadata.appendChild(title)
	titleData =doc.createTextNode(rec[2])
	title.appendChild(titleData)
	
	description = doc.createElement('description')
	metadata.appendChild(description)	
	descriptionData =doc.createTextNode(rec[4])
	description.appendChild(descriptionData)
	
	date = doc.createElement('date')
	metadata.appendChild(date)	
	dateData =doc.createTextNode(rec[0].strftime('%Y-%m-%d'))
	date.appendChild(dateData)

	

#################################################################################################
#################################################################################################
f.write(doc.toxml(encoding='utf-8'))
f.close()
#print(len(s))