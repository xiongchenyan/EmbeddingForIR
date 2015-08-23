'''
Created on Aug 23, 2015 3:44:45 PM
@author: cx

what I do:
    Just sum up the vectors
what's my input:

what's my output:


'''

import numpy as np
from scipy.spatial.distance import cosine

from ContinuousLanguageModel.ContinuousLm import ContinuousLmC
import logging
import sys



class SummationLmC(ContinuousLmC):
        
    def Init(self):
        #main parameters
        ContinuousLmC.Init(self)
        self.Mu = np.array()
        #parameters for smoothing
        
        
    def Construct(self,lTerm,Word2VecModel):
        '''
        calculate the mean and sigma of it
        lTerm must be cleaned
        '''
        lTerm = [term.lower() for term in lTerm]
        lVec = [Word2VecModel[term] for term in lTerm if term in Word2VecModel]
        mWord2Vec = np.matrix(lVec)
        self.Mu = np.array(np.mean(mWord2Vec,0))
       
        return True
    
            
        
        
    
    
    def pdf(self,x,SmoothMethod=None,PriorDis = None):
        CosDistance = cosine(x,self.Mu)
        return (2.0 - CosDistance) / 2.0
        
        
        

        
        
        
   