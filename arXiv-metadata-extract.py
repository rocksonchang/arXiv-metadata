import urllib
import time
from xml.dom import minidom

## http request to OA server 
url = 'http://export.arxiv.org/oai2?verb=ListRecords&set=physics:quant-ph&metadataPrefix=oai_dc'
rawData = urllib.urlopen(url).read()
print(type(rawData))
indStart=rawData.find('<record>')
indEnd=rawData.find('<resumptionToken')
indToken1=rawData[indEnd:].find('>')
indToken2=rawData[indToken1:].find('<')
rawData[indToken1:indToken2]

cutData=rawData[indStart+7:indEnd]

'''
fname='arXiv-meta{}.xml'

f=open(fname,'w')
f.write(rawdata)
f.close()

## parse XML data
data = minidom.parse('xmltest.xml')
token = data.getElementsByTagName("resumptionToken")[0]
titles = data.getElementsByTagName("dc:title")
print(token.firstChild.data)
for i in range(0,10):
	print titles[i].firstChild.data


## wait 20 seconds and send next request
#time.sleep(22)
url = 'http://export.arxiv.org/oai2?verb=ListRecords&resumptionToken={}'.format(token.firstChild.data)
rawdata = urllib.urlopen(url).read()

f=open('xmltest.xml','a')
f.write(rawdata)
f.close()

data = minidom.parse('xmltest.xml')
token = data.getElementsByTagName("resumptionToken")[0]
titles = data.getElementsByTagName("dc:title")
print(token.firstChild.data)
for i in range(0,10):
	print titles[i].firstChild.data
'''