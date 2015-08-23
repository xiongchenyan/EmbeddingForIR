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

from ContinuousLanguageModel.ContinuousLm import ContinuousLmC
import logging
import sys

class GaussianLmC(ContinuousLmC):
        
    def Init(self):
        #main parameters
        ContinuousLmC.Init(self)
        self.Mu = None
        self.Sigma = None
        self.Inv = None
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
    
    def SequentialConstructWithTermWeights(self,lTerm,Word2VecModel,lWeights):
        lTerm = [term.lower() for term in lTerm]
        
        '''
        get mean first
        '''
        Sum = None
        
        lInUse = [item for item in zip(lTerm,lWeights) if item[0] in Word2VecModel]
        lInUseTerm = [item[0] for item in lInUse]
        lInUseWeight = [item[1] for item in lInUse]
        WTotal = sum(lInUseWeight)
        if 0 == WTotal:
            return
        for term in lInUseTerm:
            vec = Word2VecModel[term]
            if Sum == None:
                Sum = vec
                continue
            Sum += vec
        
        self.Mu = Sum / float(WTotal)
        
        logging.info('sequential gaussian lm contruction for [%f] totol weight mean done', WTotal)
        
        CovSum = None
        for term in lInUseTerm:
            vec = Word2VecModel[term]
            Diff = np.matrix(vec - self.Mu)
            ThisCov = Diff.T * Diff
            
            if CovSum == None:
                CovSum = ThisCov
                continue
            CovSum += ThisCov
            
        self.Sigma = CovSum / float(WTotal)
        self.Inv = np.linalg.inv(self.Sigma)
        logging.info('sequential gaussian lm contruction for [%f] totol weight Sigma done', WTotal)
        return True
        
            
            
        
        
    
    
    def pdf(self,x,SmoothMethod=None,PriorDis = None):
        
        if SmoothMethod == None:
            if len(self.Mu) == 0:
                return 0
            model = multivariate_normal(mean=self.Mu,cov=self.Sigma)
            return model.pdf(x) 
        
#         if SmoothMethod == 'mixture':
#             return self.MixtureSmoothPdf(x,PriorDis)
#         
#         if SmoothMethod == 'prior':
#             return self.PriorSmoothPdf(x,PriorDis)
        
        logging.ERROR('smooth method unknow [%s]',SmoothMethod)
        sys.exit()
        
      
      
    '''
      depreciated
      TBD: fix wrong calling of method of multivariate_normal
    '''  
#     def MixtureSmoothPdf(self,x,PriorDis):
#         
#         return self.MixtureLambda * multivariate_normal(x,mean=PriorDis.Mu,cov = PriorDis.Sigma) \
#             + (1-self.MixtureLambda) * multivariate_normal(x,mean=self.Mu,cov=self.Sigma)
#             
#     def PriorSmoothPdf(self,x,PriorDis):
#         SigmaPos = np.linalg.inv(PriorDis.Inv + self.PriorN * self.Inv)
#         MuPos = SigmaPos *  (PriorDis.Inv * (np.matrix(PriorDis.Mu).T) + self.PriorN * self.Inv * (np.matrix(self.Mu).T))
#         
#         return multivariate_normal(x,mean=MuPos,cov=SigmaPos)
        
        
        
            
        
        
         

