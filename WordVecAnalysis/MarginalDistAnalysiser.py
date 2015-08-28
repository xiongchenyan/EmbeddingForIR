'''
Created on Aug 28, 2015 10:50:49 AM
@author: cx

what I do:
    Analysis the marginal distributions of given corpus's word vectors
what's my input:
    word2vec model
    lTerm
what's my output:
    per dimension's hist plot

'''

import site
import logging



site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from cxBase.base import cxBaseC
from cxBase.Conf import cxConfC

import numpy as np
import pickle
class MarginalDistAnalysiserC(cxBaseC):
        
    def Init(self):
        cxBaseC.Init(self)
        self.BinNumber = 100
        return
    
    def SetConf(self,ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.BinNumber = self.conf.getint('binnumber',self.BinNumber)
        return True
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'binnumber'
    

        
    
    
   

    
    def BinData(self,lX,OutName):
        '''
        bin all lX's dim
        [[mu,sigma, bins]]
        '''
        lBinData = []
        for x in lX:
            mu = np.mean(x)
            sigma = np.var(x)
            hist,bins = np.histogram(x,bins=self.BinNumber)
            lBinData.append([mu,sigma,hist, bins])
        
        out = open(OutName,'w')
        
        pickle.dump(lBinData,out)
        out.close()
        logging.info('data binned to [%s]',OutName)
        
    
    

        
    
        
    
    


