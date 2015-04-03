'''
Created on Apr 3, 2015 5:59:41 PM
@author: cx

what I do:
get the sparse mtx (csv format) for docs in SVMData
Row Id aligned with row in SVMData (start from 1)
what's my input:
SVMData + ClueWeb Boiler pipe + idf dict
what's my output:
sparse mtx of: doc-word-(tf*idf)
+ term->id mapping

'''

import pickle
import nltk
import logging,json
import math



stemmer = nltk.stem.PorterStemmer()

def ProcessOneDoc(DocId,lTerm,hCtf,hTermId):
    hIdScore = {}
    global stemmer
    for term in lTerm:
        term = stemmer.stem(term)
        if not term in hTermId:
            hTermId[term] = len(hTermId) + 1
        TermId = hTermId[term]
        
        ctf = 0.5
        if term in hCtf:
            ctf = hCtf[term]
        if ctf == 0:
            ctf = 0.5    
        score = math.log(1.0/ctf)
        if not TermId in hIdScore:
            hIdScore[TermId] = score
        else:
            hIdScore[TermId] += score
            
    lIdScore = hIdScore.items()
    lDocTermScore = ["%d\t%d\t%f" %(DocId,item[0],item[1]) for item in lIdScore]
    return lDocTermScore


def LoadDocFromSVMData(InName):
    '''
    one doc can have multiple id
    '''
    hDocNoToId = {}
    
    lLines = open(InName).read().splitlines()
    lDocNo = [item.split('#')[-1].strip() for item in lLines]
    
    for Id,DocNo in enumerate(lDocNo):
        Id += 1
        if not DocNo in hDocNoToId:
            hDocNoToId[DocNo] = [Id]
        else:
            hDocNoToId[DocNo].append(Id)
            
    return hDocNoToId


def Process(SVMInName,DocTextInName,CtfInName,OutPre):
    hTermId = {}
    
    hCtf = pickle.load(open(CtfInName))
    logging.info('ctf dict loaded')
    out = open(OutPre,'w')
    hDocNo = LoadDocFromSVMData(SVMInName)
    logging.info('doc no formed')
    for LineCnt,line in enumerate(open(DocTextInName)):
        line = line.strip()
        vCol = line.split()
        DocNo = vCol[0]
        lTerm = vCol[1:]
        
        if not DocNo in hDocNo:
            continue
        
        lDocId = hDocNo[DocNo]
        
        for DocId in lDocId:
            lDocTermScore = ProcessOneDoc(DocId, lTerm, hCtf, hTermId)
            print >> out, '\n'.join(lDocTermScore)
            
        if 0 == (LineCnt % 1000):
            logging.info('processed [%d] lines',LineCnt) 
            
            
    out.close()
    pickle.dump(hTermId,open(OutPre + '_termid','w'))
    logging.info('done')
    return True


import sys

logging.basicConfig(level=logging.INFO)

if 5 != len(sys.argv):
    print "4 para: svm in + doc text in + ctf in + out"
    sys.exit()
    
Process(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])








        
    
        
    
    
    
