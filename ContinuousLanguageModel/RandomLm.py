'''
Created on Aug 23, 2015 4:19:55 PM
@author: cx

what I do:
    return random score
what's my input:

what's my output:


'''


import numpy as np

from ContinuousLanguageModel.ContinuousLm import ContinuousLmC



class RandLmC(ContinuousLmC):
        
    def Init(self):
        #main parameters
        ContinuousLmC.Init(self)
        #parameters for smoothing
        
        
    def Construct(self,lTerm,Word2VecModel):
        '''
        calculate the mean and sigma of it
        lTerm must be cleaned
        '''
        return True
    
            
        
        
    
    
    def pdf(self,x,SmoothMethod=None,PriorDis = None):
        return np.random.rand()
        
        
        

        
