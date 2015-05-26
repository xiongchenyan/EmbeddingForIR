'''
Created on my MAC May 26, 2015-4:27:06 PM
What I do:
I build Gaussian Language Model for given text and word2vec
I can do:
    construct (namely calculate the mu and sigma)
    pdf (Gaussian pdf)
    pdf with smooth (prior and mixture) with given hyper paramter (smoothing weights)
    
What's my input:

What's my output:

@author: chenyanxiong
'''

import numpy as np
from scipy.stats import multivariate_normal

import logging
import sys
class GaussianLmC(object):
    def __init__(self,lTerm = [],Word2VecModel = None):
        self.Init()
        if ([] != lTerm) & (None != Word2VecModel):
            self.Construct(lTerm, Word2VecModel)
        
    def Init(self):
        #main parameters
        self.Mu = np.array()
        self.Sigma = np.matrix()
        self.Inv = np.matrix()
        #parameters for smoothing
        self.PriorN = 1
        self.MixtureLambda = 0.5
        
        
    def Construct(self,lTerm,Word2VecModel):
        '''
        calculate the mean and sigma of it
        lTerm must be cleaned
        '''
        lTerm = [term.lower() for term in lTerm]
        lVec = [Word2VecModel[term] for term in lTerm if term in Word2VecModel]
        mWord2Vec = np.matrix(lVec)
        self.Mu = np.array(np.mean(mWord2Vec,0))
        self.Sigma = np.cov(mWord2Vec.T)
        self.Inv = np.linalg.inv(self.Sigma)
        logging.debug('gaussian lm constructed')
        return True
    
    def pdf(self,x,SmoothMethod=None,PriorDis = None):
        
        if SmoothMethod == None:
            if len(self.Mu) == 0:
                return 0
            
            return multivariate_normal(x,mean=self.Mu,cov=self.Sigma)
        
        if SmoothMethod == 'mixture':
            return self.MixtureSmoothPdf(x,PriorDis)
        
        if SmoothMethod == 'prior':
            return self.PriorSmoothPdf(x,PriorDis)
        
        logging.ERROR('smooth method unknow [%s]',SmoothMethod)
        sys.exit()
        
        
    def MixtureSmoothPdf(self,x,PriorDis):
        
        return self.MixtureLambda * multivariate_normal(x,mean=PriorDis.Mu,cov = PriorDis.Sigma) \
            + (1-self.MixtureLambda) * multivariate_normal(x,mean=self.Mu,cov=self.Sigma)
            
    def PriorSmoothPdf(self,x,PriorDis):
        SigmaPos = np.linalg.inv(PriorDis.Inv + self.PriorN * self.Inv)
        MuPos = SigmaPos *  (PriorDis.Inv * (np.matrix(PriorDis.Mu).T) + self.PriorN * self.Inv * (np.matrix(self.Mu).T))
        
        return multivariate_normal(x,mean=MuPos,cov=SigmaPos)
        
        
        
            
        
        
         
