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

class KernelDensityLmC(object):
    def __init__(self,lData = [],Word2VecModel = None):
        self.Init()
        if ([] != lData):
            self.Construct(lData,Word2VecModel)
            
            
    def Init(self):
        self.kde = KernelDensity()
        self.lBandWidth=np.logspace(-10, 10, 20)
        self.lX = []
        
    def Construct(self,lData,Word2VecModel=None):
        if [] == lData:
            continue
        if type(lData) == str:
            self.lX = [Word2VecModel[term] for term in lData if term in Word2VecModel]
        else:  #then it should be vectors already
            self.lX = lData
        self.kde = self.CVForBestKde()
        logging.info('doc kde lm estimated')
        
        
    def CVForBestKde(self):
        params = {'bandwidth':self.lBandWidth}
        grid = GridSearchCV(KernelDensity(), params)
        grid.fit(self.lX)
        logging.info('best bandwidth = [%f]',grid.best_estimator_.bandwidth)
        return grid.best_estimator_
    
    
    def pdf(self,x):
        return self.kde.score(x)
        


