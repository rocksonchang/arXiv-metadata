"""
arXiv-metadata-extract.py (beta) --- 25 June 2016
This script has been coded for Python3.
This script downloads metadata from the arXiv.  For the moment it's set to pull data from physics:quant-ph. The arXiv participates in the Open Archives Initiative (OAI; http://www.openarchives.org/).  Requests can be made to the URL http://export.arxiv.org/oai2, returning metadata in XML format.

The metadata consists of the following entries:
	dc:title
	dc:creater (authors)
	dc:subject (keywords)
	dc:description (abstract)
	dc:date (date of submission)
	dc:identifier (final publishing locations)

Each article entry is referred to as a <Record>, and the entire list is within the structure of <ListRecords>.
They restrict queries to 1k records.  As of 25 June 2016 there were around 80k total records dating back to 1992 (average of 3k records per year over 25 years).  Each 1k block of XML data occupies about 1.7MB.  A resumptionToken allows us to pick up the query where we left off.  When the token return is empty, we've reached the end of our query.
OAI2 allows to specify the date range of entries, but note that this is the date of the metadata update, not the article submission date.  The entire metadata set was updated in 1 April 2007.  I've decided to break up the XML data into 3 year blocks -- block1: 2007-2009, block2: 2010-2012, block3: 2013-2015, block4: 2016
"""

import urllib
import time
from itertools import chain
from xml.dom import minidom

## initial http request to OA server 
url = 'http://export.arxiv.org/oai2?verb=ListRecords&set=physics:quant-ph&metadataPrefix=oai_dc&from=2007-01-01&until=2009-12-31'
## setup XML file
fname = 'arXiv-meta-block1.xml'
token = 'dummy'
f=open(fname,'w')
f.write('<ListRecords>\n')
## start pulling in data, 1000 entries at a time.  
i=0
while token != '':
	i+=1
	print('Exectuing HTTP query {}'.format(i))
	rawData = urllib.urlopen(url).read()

	## find indicies to extract token and chop data
	indStart=rawData.find('<record>')
	indEnd=rawData.find('<resumptionToken')
	indToken1=rawData.find('>',indEnd)
	indToken2=rawData.find('<',indToken1)	

	## write to file
	f.write(rawData[indStart:indEnd])
	## find resumption token
	token=rawData[indToken1+1:indToken2]
	print('\tResumption token = {}'.format(token))
	url = 'http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={}'.format(token)	
	## wait 20 seconds to keep OAI2 happy
	time.sleep(20)

## write XML footer and close file
f.write('</ListRecords>\n')
f.close()

'''
## parse XML data and test some outputs
data = minidom.parse(fname)
titles = data.getElementsByTagName("dc:title")
for i in chain(range(0,10), range(1000,1010)):
	print titles[i].firstChild.data
'''