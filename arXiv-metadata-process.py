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
#!/usr/bin/python3.5

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
import pickle
## handling of non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
print('\n')

#################################################################################################
#################################################################################################
## load data
print ('Loading XML data...')
#creators=[]
addys=[]
titles=[]
descriptions=[]
dates=[]

years=range(2004,2005)
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
print('\n')

#################################################################################################
#################################################################################################
## Quarterly blocks
print ('Extracting text, identifying most frequently used words each quarter...')
NRec=sum(NRecYear)
topWords=[]
NRecRunning=0
year0=years[0]
NRecQuarter=[0]*len(years)*4

for x in range(len(years)):	
	fulltextQuarter=['']*4
	for i in range(NRecYear[x]):
		rec=i+NRecRunning						
		desc=descriptions[rec]
		
		title=titles[rec]
		text=title+desc

		date=datetime.strptime(dates[rec],'%Y-%m-%d')		
		Q=int(ceil(date.month/3.)-1)
		ind = 4*(date.year-year0)+Q
		NRecQuarter[ind]+=1

		fulltextQuarter[Q]=fulltextQuarter[Q]+text		
		
	NRecRunning=NRecRunning+NRecYear[x]
	

	for q in range(4):
		desc_fullwordlist = obo.stripNonAlphaNum(fulltextQuarter[q])
		desc_wordlist = obo.removeStopwords(desc_fullwordlist,obo.stopwords)	
		desc_dictionary = obo.wordListToFreqDict(desc_wordlist)
		desc_sorteddict = obo.sortFreqDict(desc_dictionary)

		topWords.append(desc_sorteddict[:300])
		
		print ('Year: {}; Quarter: Q{}; Num. entries: {}'.format(years[x],q+1,NRecQuarter[4*(date.year-year0)+q]))				
		#for s in desc_sorteddict[:10]: 	print(str(s))
		#print('\n')
print('\n')
	
#################################################################################################
#################################################################################################
## Pickle?
with open('obj/'+ 'topWords' + '.pkl', 'wb') as f:
	pickle.dump(topWords, f, pickle.HIGHEST_PROTOCOL)

#################################################################################################
#################################################################################################
## Word counting
print ('Tracking occurance of a particular word...')
N=[0]*len(topWords)
for q in range(len(topWords)):
	year  = year0  + int(ceil((q+1.)/4)-1)
	print('Year: {}; Quarter: Q{}; Num. entries: {}').format(year, q%4+1, NRecQuarter[q])
	topWordsquarter=topWords[q]
	for s in topWordsquarter[:10]: print(str(s))	

	# topWordsquarter is a list of tuples [(key, value)..]
	# need to reverse, then build dictionary
	topWordsquarterReversed=[]
	for t in topWordsquarter:
		topWordsquarterReversed.append(tuple(reversed(t)))	
	invDict=dict(topWordsquarterReversed)
		
	word='mechanics'.lower()
	if word in invDict: N[q] = invDict.get(word); 
	else: N[q]=0
	
	print('\n')	

print(N)