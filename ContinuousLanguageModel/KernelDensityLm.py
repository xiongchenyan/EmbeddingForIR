'''
Created on my MAC May 27, 2015-3:51:44 PM
What I do:
I estimate kernel density for each document as its Language model
    in the continuous space
What's my input:
lTerms
What's my output:
a kde, can sample, can calculate pdf of a given term
@author: chenyanxiong
'''



import numpy as np

from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
import logging
import json
from ContinuousLanguageModel.ContinuousLm import ContinuousLmC

class KernelDensityLmC(ContinuousLmC):
            
            
    def Init(self):
        ContinuousLmC.Init(self)
        self.kde = KernelDensity()
        self.lBandWidth=np.logspace(-2, 0, 5)
        self.lX = []
        
    def Construct(self,lTerm,Word2VecModel):
        if [] == lTerm:
            return
        self.lX = [Word2VecModel[term] for term in lTerm if term in Word2VecModel]
        self.kde = self.CVForBestKde()
        logging.info('doc kde lm estimated')
        
        
    def CVForBestKde(self):
        params = {'bandwidth':self.lBandWidth}
#         logging.debug('cv bandwidth from [%s]',json.dumps(self.lBandWidth))
        grid = GridSearchCV(KernelDensity(), params)
        logging.debug('fitting on [%d] vector',len(self.lX))
        grid.fit(self.lX)
        logging.info('best bandwidth = [%f]',grid.best_estimator_.bandwidth)
        return grid.best_estimator_
    
    
    def pdf(self,x):
        return self.kde.score(x)
        


