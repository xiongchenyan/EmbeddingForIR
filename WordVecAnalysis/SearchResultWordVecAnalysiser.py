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
import gensim
import numpy as np
import pickle
from scipy.stats import pearsonr

class SearchResultWordVecAnalysiserC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.QIn = ""
        self.OutDir = ""
        self.Word2VecInName = ""
        self.Word2VecModel = None
        self.Searcher = IndriSearchCenterC()
        self.BinNumber = 100
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Searcher.SetConf(ConfIn)
        
        self.Word2VecInName = self.conf.GetConf('word2vecin')
        self.LoadWord2Vec()
        self.QIn = self.conf.GetConf('in')
        self.OutDir = self.conf.GetConf('outdir')
        self.BinNumber = self.conf.GetConf('binnumber', self.BinNumber)
        
    def LoadWord2Vec(self):
        logging.info('start load word2vec input')
        self.Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(self.Word2VecInName)
        logging.info('word2vec loaded')     
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'word2vecin\nin\noutdir\nbinnumber'
        IndriSearchCenterC.ShowConf()
        
        
    def LoadDocWordVec(self):
        
        lDoc = []
        lQidQuery = [line.split('\t') for line in open(self.QIn).read().splitlines()]
        
        for qid,query in lQidQuery:
            lDoc.extend(self.Searcher.RunQuery(query, qid))
        
        lTerm = []
        for doc in lDoc:
            lTerm.extend(doc.GetContent().split())
            
        lX = np.array([self.Word2VecModel[term] for term in lTerm if term in self.Word2VecModel])
        
        logging.info('target doc word vec get')
        return lX
    
    
    def BinData(self,lX,OutName):
        '''
        bin all lX's dim
        [[mu,sigma, bins]]
        '''
        logging.info('binning data')
        lBinData = []
        dim = lX.shape[1]
        for i in range(dim):
            x = lX[:,i]
            logging.info('binning dim [%d]',i)
            mu = np.mean(x)
            sigma = np.var(x)
            hist,bins = np.histogram(x,bins=self.BinNumber)
            lBinData.append([mu,sigma,hist, bins])
        
        out = open(OutName,'w')
        
        pickle.dump(lBinData,out)
        out.close()
        logging.info('data binned to [%s]',OutName)
        return
    
    def CalcPersonCorrelation(self,lX,OutName):
        
        n,d = lX.shape
        mPValue = np.zeros([d,d])
        mPearson = np.zeros([d,d])
        
        for i in range(d):
            for j in range(i+1,d):
                per,p = pearsonr(lX[:,i],lX[:,j])
                mPValue[i,j] = p
                mPValue[j,i] = p
                mPearson[i,j] = per
                mPearson[j,i] = per
                if p < 0.05:
                    logging.info('[%d-%d] correlated p=%f',i,j,p)
        
        out = open(OutName + '_pearson','w')
        pickle.dump(mPearson,out)
#         print >>out, np.array2string(mPearson)
        out.close()
        
        out = open(OutName + '_pvalue','w')
        pickle.dump(mPValue,out)
#         print >>out, np.array2string(mPValue)
        out.close()
        
        logging.info('pearson corr calculated and dumped')
        
        return True
        
    def CalcCovarianceMtx(self,lX,OutName):
        logging.info('start calculating covariance matrix')
        CovMtx = np.cov(lX.T)
        out = open(OutName,'w')
        pickle.dump(CovMtx,out)
        out.close()
        logging.info('covariance dumped to [%s]',OutName)
        
        
            
    
    def Process(self):
        
        lX = self.LoadDocWordVec()
    
#         self.BinData(lX, self.OutDir + '/MarginalDist')
        
        
        self.CalcCovarianceMtx(lX, self.OutDir + '/CovarianceMtx')
        self.CalcPersonCorrelation(lX,self.OutDir + '/PersonCorrelationMtx')
        
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
    
        
        
        