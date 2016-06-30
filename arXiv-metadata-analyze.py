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

import time
import pickle
from math import ceil
import matplotlib.pyplot as plt
import numpy as np
## handling of non-ascii characters in the database
# http://chase-seibert.github.io/blog/2014/01/12/python-unicode-console-output.html
import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)
print('\n')


#################################################################################################
#################################################################################################
## Pickle?
NRecQuarter = pickle.load( open( "obj/NRecQuarter.pkl", "rb" ) )
topWords = pickle.load( open( "obj/topWords5k.pkl", "rb" ) )

#################################################################################################
#################################################################################################
## Word counting
year0=1992
print ('Tracking occurance of a particular word...')
N=[0]*len(topWords)
for q in range(len(topWords)):
	year  = year0  + int(ceil((q+1.)/4)-1)
	print('Year: {}; Quarter: Q{}; Num. entries: {}').format(year, q%4+1, NRecQuarter[q])
	topWordsquarter=topWords[q]
	#for s in topWordsquarter[-10:-1]: print(str(s))	

	# topWordsquarter is a list of tuples [(key, value)..]
	# need to reverse, then build dictionary
	topWordsquarterReversed=[]
	for t in topWordsquarter:
		topWordsquarterReversed.append(tuple(reversed(t)))	
	invDict=dict(topWordsquarterReversed)
		
	#word='lattice'.lower()		
	#if word in invDict: N[q] = invDict.get(word); 
	#else: N[q]=0
	wordList=['bose','einstein','condensate']
	wordList=['synthetic','magnetic','field']
	wordList=['bose','hubbard']
	wordList=['degenerate','fermi','gas']
	wordList=['feshbach','resonance']
	wordList=['trapped', 'ions']
	wordList=['single','site','microscope']
	wordList=['anderson','localization']
	wordList=['bloch','oscillation']
	wordList=['phase','transition']
	wordList=['kibble','zurek']
	wordList=['electromagnetically','induced']
	wordList=['vortex','lattice']
	for word in wordList:
		if word.lower() in invDict: N[q] += invDict.get(word);
		else:
			N[q] = 0
			break;

quarters=np.arange(len(N))
years=quarters/4.+1992
NRecQuarter[NRecQuarter==0]=0.1

plt.subplot(211)
plt.plot(years,N)
plt.plot(years,NRecQuarter)
plt.title('Search: {}'.format(word))
plt.subplot(212)
plt.plot(years,np.asarray(N)/np.asarray(NRecQuarter))
plt.show()