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
import itertools
import time
#import numpy as np
from math import ceil
## Using some simple functions from http://programminghistorian.org/lessons/counting-frequencies
import obo
## handling of non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)


#################################################################################################
#################################################################################################
## load data
#creators=[]
addys=[]
titles=[]
descriptions=[]
dates=[]

years=range(1992,1999)
NRecYear=[0]*(len(years))	

for x in range(len(years)):	
	fname ='arXiv-meta-{}.xml'.format(years[x])	
	## parse XML data
	data = minidom.parse(fname)		
	for rec in data.getElementsByTagName('record'):			
		NRecYear[x]+=1
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
	print ('Loading year: {}; Num. entries: {}'.format(years[x],NRecYear[x]))


## output some stuff to check	
#print('\n')		
#for i in range(len(titles)): print(titles[i]);	print(dates[i]); print(descriptions[i]); print('\n');


#################################################################################################
#################################################################################################
## yearly blocks
'''
print('\n')
NRec=sum(NRecYear)
NRecRunning=0
for x in range(len(years)):	
	fulltextYear=''	
	for i in range(NRecYear[x]):
		rec=i+NRecRunning				
		desc=descriptions[rec]
		title=titles[rec]
		text=desc+title
		fulltextYear=fulltextYear+text	
	NRecRunning=NRecRunning+NRecYear[x]

	

	desc_fullwordlist = obo.stripNonAlphaNum(fulltextYear)
	desc_wordlist = obo.removeStopwords(desc_fullwordlist,obo.stopwords)	
	desc_dictionary = obo.wordListToFreqDict(desc_wordlist)
	desc_sorteddict = obo.sortFreqDict(desc_dictionary)
	
	print ('Year: {}; Num. entries: {}'.format(years[x],NRecYear[x]))

	#x = itertools.islice(desc_sorteddict.items(), 0, 10)

	for s in desc_sorteddict[:30]: 	
		print(str(s))
	print('\n')
'''

#################################################################################################
#################################################################################################
## Quarterly blocks
print('\n')
NRec=sum(NRecYear)
top100=[]
NRecRunning=0
year0=1992
NRecQuarter=[0]*25*4
for x in range(len(years)):	
	fulltextQuarter=['']*4
	for i in range(NRecYear[x]):
		rec=i+NRecRunning				
		desc=descriptions[rec]
		
		title=titles[rec]
		text=title+desc

		date=datetime.strptime(dates[rec],'%Y-%m-%d')		
		Q=int(ceil(date.month/3)-1)
		ind = 4*(date.year-year0)+Q
		NRecQuarter[ind]+=1

		fulltextQuarter[Q]=fulltextQuarter[Q]+text		
		
	NRecRunning=NRecRunning+NRecYear[x]
	

	for q in range(4):
		desc_fullwordlist = obo.stripNonAlphaNum(fulltextQuarter[q])
		desc_wordlist = obo.removeStopwords(desc_fullwordlist,obo.stopwords)	
		desc_dictionary = obo.wordListToFreqDict(desc_wordlist)
		desc_sorteddict = obo.sortFreqDict(desc_dictionary)

		top100.append(desc_sorteddict[:300])
		'''
		print ('Year: {}; Quarter: Q{}; Num. entries: {}'.format(years[x],q+1,len(fulltextQuarter[q])))
		for s in desc_sorteddict[:40]: 	print(str(s))
		print('\n')
		'''

#with open('obj/'+ name + '.pkl', 'wb') as f:
	#pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

year0=1992
N=[0]*len(top100)
for q in range(len(top100)):
	year  = year0  + int(ceil((q+1.)/4)-1)
	print('Year: {}; Quarter: Q{}; Num. entries: {}').format(year, q%4+1, NRecQuarter[q])
	top100quarter=top100[q]
	for s in top100quarter[:10]: print(str(s))
	print('\n')

	dictQuarter=dict(top100quarter)
	invDict = {v: k for k, v in dictQuarter.items()}
	
	word='bose'.lower()
	
	if word in invDict: N[q] = invDict.get(word); 
	else: N[q]=0

print(N)
