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



import site

site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')

import numpy as np
from DensityEstimation.AdditiveKde import AdditiveKdeC
from sklearn.neighbors import KernelDensity
from sklearn.grid_search import GridSearchCV
import logging
import json
from ContinuousLanguageModel.ContinuousLm import ContinuousLmC


class KernelDensityLmC(ContinuousLmC):
            
            
    def Init(self):
        ContinuousLmC.Init(self)
        self.kde = KernelDensity()
        self.lBandWidth=np.logspace(-2, 0, 10)
        self.BandWidth = 0.1
        self.KernelType = 'kde'
        
        
    def SetPara(self, conf):
        ContinuousLmC.SetPara(self, conf)
        self.BandWidth = conf.GetConf('bandwidth',self.BandWidth)
        self.KernelType = conf.GetConf('kernel',self.KernelType)
        return True
    
    
    
        
    def Construct(self,lTerm,Word2VecModel):
        if [] == lTerm:
            return
        lX = np.array([Word2VecModel[term] for term in lTerm if term in Word2VecModel])
#         self.kde = self.CVForBestKde()
        self.FitKernel(lX)
        
        logging.debug('doc kde lm estimated')
    
    
    def FitKernel(self,lX):
        if self.KernelType == 'additivekde':
            self.kde = AdditiveKdeC()
            self.kde.Bandwidth = self.BandWidth
            self.kde.fit(lX)
            return
        self.kde = KernelDensity(kernel='gaussian',bandwidth=self.BandWidth).fit(lX)
        return
    
        
    def CVForBestKde(self):
        '''
        this is CV for each doc's best bandwidth
        It is better/more intuitive to CV for training query's ranking performance
        '''
        params = {'bandwidth':self.lBandWidth}
#         logging.debug('cv bandwidth from [%s]',json.dumps(self.lBandWidth))
        grid = GridSearchCV(KernelDensity(), params)
        logging.debug('fitting on [%d] vector',len(self.lX))
        grid.fit(self.lX)
        logging.info('best bandwidth = [%f]',grid.best_estimator_.bandwidth)
        return grid.best_estimator_
    
    def pdf(self,x):
        return np.exp(self.LogPdf(x))
    
    def LogPdf(self, x):
        return self.kde.score(x)
        


