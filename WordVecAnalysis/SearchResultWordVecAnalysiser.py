'''
Created on Aug 28, 2015 11:33:17 AM
@author: cx

what I do:
    i analysis the word2vec in search result pages
what's my input:
    query
    word2vec
    search used data
what's my output:
    marginal dist figure plots

'''


import site
import logging


site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from IndriSearch.IndriDocBase import IndriDocBaseC
from MarginalDistAnalysiser import MarginalDistAnalysiserC
import gensim
import numpy as np


class SearchResultWordVecAnalysiserC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.MarginalAna = MarginalDistAnalysiserC()
        self.QIn = ""
        self.OutDir = ""
        self.Word2VecInName = ""
        self.Word2VecModel = None
        self.Searcher = IndriSearchCenterC()
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.MarginalAna.SetConf(ConfIn)
        self.Searcher.SetConf(ConfIn)
        
        self.Word2VecInName = self.conf.GetConf('word2vecin')
        self.LoadWord2Vec()
        self.QIn = self.conf.GetConf('in')
        self.OutDir = self.conf.GetConf('outdir')
        
    def LoadWord2Vec(self):
        logging.info('start load word2vec input')
        self.Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(self.Word2VecInName)
        logging.info('word2vec loaded')     
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'word2vecin\nin\noutdir'
        IndriSearchCenterC.ShowConf()
        MarginalDistAnalysiserC.ShowConf()
        
        
    def LoadDocWordVec(self):
        
        lDoc = []
        lQidQuery = [line.split('\t') for line in open(self.QIn).read().splitlines()]
        
        for qid,query in lQidQuery:
            lDoc.extend(self.Searcher.RunQuery(query, qid))
        
        lTerm = []
        for doc in lDoc:
            lTerm.extend(doc.GetContent().split())
            
        lX = [self.Word2VecModel[term] for term in lTerm if term in self.Word2VecModel]
        
        logging.info('add doc word vec get')
        return lX
    
    
    def Process(self):
        
        lX = self.LoadDocWordVec()
    
        self.MarginalAna.Process(lX, self.OutDir + '/MarginalDist')
        
        logging.info('[%s] search result word vec analysis finished',self.QIn)
        
        return True
    
    
if __name__=='__main__':
    import sys
    if 2 != len(sys.argv):
        SearchResultWordVecAnalysiserC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    Analysisor = SearchResultWordVecAnalysiserC(sys.argv[1])
    Analysisor.Process()
    
        
        
        