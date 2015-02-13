'''
Created on Feb 13, 2015 4:23:03 PM
@author: cx

what I do:
Transfer the textual formated clueweb 09 cate B to docvec training format
what's my input:
ClueWeb with boiler pipe
what's my output:
each line for a document
docno word word (cleaned text)


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.TextBase import TextBaseC
import sys


def ProcessOneDoc(lLines):
    DocNo = ""
    text = ""
    TextFlag = False
    for line in lLines:
        if "<DOCNO>" == line[:7]:
            DocNo = line.replace('</DOCNO>','').replace('<DOCNO>')
            continue
        if '<TEXT>' == line[:6]:
            TextFlag = True
        if '</TEXT>' == line[:7]:
            TextFlag = False
        if TextFlag:
            text += line.strip()
    text = TextBaseC.RawClean(text)
    return DocNo+ ' ' + text



if 3 != len(sys.argv):
    print 'ClueWeb boiler pipe input + doc vec trainingd data out'
    sys.exit()
    
    
out = open(sys.argv[2],'w')

lLines = []
DocCnt = 0
for line in open(sys.argv[1]):
    if '</DOC>' == line[:6]:
        print >>out, ProcessOneDoc(lLines)
        DocCnt += 1
        if 0 == (DocCnt % 1000):
            print 'processed [%d] doc' %(DocCnt)        
        lLines = []
    lLines.append(line)
    
print 'finished [%d] doc total' %(DocCnt)
    
    

    