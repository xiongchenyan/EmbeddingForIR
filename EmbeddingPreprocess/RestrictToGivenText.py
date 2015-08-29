'''
Created on Aug 28, 2015 8:28:39 PM
@author: cx

what I do:
    only keep given text's vocabulary
what's my input:
    textin
    word2vecin
    
what's my output:
    filtered word2vec model

'''


import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from cxBase.TextBase import TextBaseC


def MakeVocabulary(TextIn):
    print 'start making vocabulary'
    sVoc = set()
    for line in open(TextIn):
        lTerm = TextBaseC.RawClean(line.strip()).split()
        sVoc.update(set(lTerm))
        
    print "total [%d] target term" %(len(sVoc))
    return sVoc

def FilterWord2VecModel(InName,OutName,sVoc):
    '''
    need two traverse...
    '''
    cnt = 0
    LineCnt = 0
    
    for line in open(InName):
        LineCnt += 1
        if 0 == (LineCnt % 1000):
            print 'first round [%d] line' %(LineCnt)
        if 1 == LineCnt:
            continue
        word = line.split()[0]
        if word in sVoc:
            cnt += 1
    
    print 'first round done, [%d] term left' %(cnt)        
    out = open(OutName,'w')
    LineCnt = 0
    for line in open(InName):
        LineCnt += 1
        if 0 == (LineCnt % 1000):
            print 'second round [%s] line' %(LineCnt)
        if 1 == LineCnt:
            Dim = line.strip().split()[-1]
            print >>out, '%d\t%s' %(cnt,Dim)
            continue
        
        word = line.split()[0]
        if word in sVoc:
            print >>out, line.strip()
    print 'finished'
    out.close()
    
    
import sys

if 2 != len(sys.argv):
    print 'conf:\nin\nword2vecin\nout'
    sys.exit()
    
conf = cxConfC(sys.argv[1])
InName = conf.GetConf('in')
OutName = conf.GetConf('out')
Word2VecIn = conf.GetConf('word2vecin')

sVoc = MakeVocabulary(InName)
FilterWord2VecModel(Word2VecIn, OutName, sVoc)
    

        
        
        
        
