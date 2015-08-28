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
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt

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
    

        
    
    
    def PlotOneDim(self,x,OutPre,dim):
        mu = np.mean(x)
        sigma = np.var(x)
        n, bins, patches = plt.hist(x, self.BinNumber, facecolor='blue', alpha=0.5)
        # add a 'best fit' line
        y = mlab.normpdf(bins, mu, sigma)
        plt.plot(bins, y, 'r--')
        plt.xlabel('embedding value dim %d',dim)
        plt.ylabel('Probability')
        plt.title(r'Histogram of Dim %d: $\mu=%f$, $\sigma=%f$',dim,mu,sigma)
        
        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)   
        OutName = OutPre + '_%d'%(dim)
        plt.savefig(OutName,format='pdf',dpi=1000)
        logging.info('dim [%d] saved [%s]',OutName)
        
        return True
    
    
    def Process(self,lX,OutPre):
        
        for dim in range(lX.shape[1]):
            x = lX[:,dim]
            self.PlotOneDim(x, OutPre, dim)
        logging.info('plotted to %s_',OutPre)
        
        return True
        
        
    
        
    
    


