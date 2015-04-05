'''
Created on Apr 5, 2015 2:03:07 PM
@author: cx

what I do:
I get an SVM LeToR data
and output:
    label,qid mtx
    feature mtx (sparse format)
    
DocId assigned by line no
add zero to empty features (don't have to as output is sparse format)

if has feature st and ed col input
    will modify the col number as (dim - st + 1)
    
what's my input:
SVM data
col st + col ed (if need)
what's my output:

a label,qid file
a sparse featue mtx file

'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')


from MLBase.SVMData import SVMDataC
import logging

def ProcessOneLine(SVMLine,LineNo, st,ed):
    data = SVMDataC(SVMLine)
    
    LabelLine = "%d,%s" %(data.Label, data.qid)
    
    lFeature = data.hFeature.items()
    
    lFeature.sort(key=lambda item:item[0])
    print "original [%d] feature" %(len(lFeature))
    lFRes = ['%s,%s,%s' %(LineNo,item[0] - st + 1,item[1]) for item in lFeature if (item[0] >= st) &(item[0] < ed)]
    print "get [%d] feature in [%d-%d)" %(len(lFRes),st,ed)
    return LabelLine,lFRes


def ReadForMinAndMax(SVMDataInName):
    st = 1 #assume st is always 1
    ed = -1
    
    for line in open(SVMDataInName):
        data = SVMDataC(line.strip())
        lDim = data.hFeature.keys()
        ed = max(ed, max(lDim))
        
    return st,ed


def Process(SVMDataInName,OutName,st = 1, ed = -1):
    if ed == -1:
        st,ed = ReadForMinAndMax(SVMDataInName)
    
    print "feature target [%d-%d)" %(st,ed)    
    LabelOut = open(OutName + "_label","w")
    FOut = open(OutName + '_feature','w')
    for LineNo,line in enumerate(open(SVMDataInName)):
        line = line.strip()
        
        LabelLine,lFResLine = ProcessOneLine(line, LineNo + 1, st, ed)
        
        print >>LabelOut, LabelLine
        print >>FOut, '\n'.join(lFResLine)
        
        if 0 == (LineNo % 100):
            print "processed [%d] lines" %(LineNo)
        
    LabelOut.close()
    FOut.close()
    
    print 'finished'
    
    
import sys

if 3 > len(sys.argv):
    print "svm in + out pre + col st(opt) + col (ed) opt"
    sys.exit()
    
    
st = 1
ed = -1

if len(sys.argv) >= 5:
    st = int(sys.argv[3])
    ed = int(sys.argv[4])

Process(sys.argv[1],sys.argv[2],st,ed)
        
    
    
    