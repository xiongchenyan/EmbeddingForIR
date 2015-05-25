'''
Created on my MAC May 25, 2015-4:21:24 PM
What I do:
only keep those that is useful for given queries

vocabulary = {all that appear in q and retrieved doc}
What's my input:
query
index
cachedir
word2vec
What's my output:
word2vec filtered with only those in vocabulary
@author: chenyanxiong
'''

import site

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.Vector import VectorC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC


def MakeVocabulary(QInName,Searcher):
    sVoc = set()
    for line in open(QInName):
        qid,query = line.strip().split('\t')
        lQT = query.lower().split()
        sVoc.update(set(lQT))
        
        lDoc = Searcher.RunQuery(query)
        for doc in lDoc:
            lDT = doc.GetContent().lower().split()
            sVoc.update(set(lDT))
    return sVoc

def FilterWord2VecModel(InName,OutName,sVoc):
    '''
    need two traverse...
    '''
    cnt = 0
    LineCnt = 0
    for line in open(InName):
        LineCnt += 1
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
    print 'conf:\nqin\nword2vecin\nout'
    IndriSearchCenterC.ShowConf()
    sys.exit()
    
Searcher = IndriSearchCenterC(sys.argv[1])
conf = cxConfC(sys.argv[1])
QInName = conf.GetConf('qin')
OutName = conf.GetConf('out')
Word2VecIn = conf.GetConf('word2vecin')

sVoc = MakeVocabulary(QInName, Searcher)
FilterWord2VecModel(Word2VecIn, OutName, sVoc)
    

        
        
        
        