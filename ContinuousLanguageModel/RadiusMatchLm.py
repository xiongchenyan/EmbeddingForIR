'''
Created on Aug 28, 2015 3:04:40 PM
@author: cx

what I do:
    p(x|D) = 1/n * (# of points within r radius of x)
    
    It is very like query expansion using r-ball around q term
    
what's my input:
    I am a subclass of ContinuousLmC

what's my output:


'''

import site

site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

import numpy as np
import logging
import json
from ContinuousLanguageModel.ContinuousLm import ContinuousLmC
import scipy

class RadiusMatchLmC(ContinuousLmC):
            
            
    def Init(self):
        ContinuousLmC.Init(self)
        self.MinCos = 0.7
        self.lX = []
        self.n = 0
        self.d = 0
        
        
    def SetPara(self, conf):
        self.MinCos = conf.GetConf('mincos',self.MinCos)
        return True
    
    
    
        
    def Construct(self,lTerm,Word2VecModel):
        if [] == lTerm:
            return
        lX = np.array([Word2VecModel[term] for term in lTerm if term in Word2VecModel])
#         self.kde = self.CVForBestKde()
        self.lX = lX
        self.n,self.d = self.lX.shape        
        logging.debug('doc kde lm estimated')
    
    
    
    def pdf(self,x):
        x=x.reshape(1,self.d)
        m = self.lX - np.ones([self.n,1]).dot(x)
        NeighborCnt = 0
        for i in range(self.n):
            cos = 1 - scipy.spatial.distance.cosine(self.lX[i,:],x)
            if cos >= self.MinCos:
                NeighborCnt += 1
        
        return NeighborCnt / float(self.n)
    
    def LogPdf(self, x):
        p = max(np.exp(-20),self.pdf(x))
        return np.log(p)
