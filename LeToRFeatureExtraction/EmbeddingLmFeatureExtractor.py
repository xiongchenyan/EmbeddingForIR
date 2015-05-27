'''
Created on my MAC May 27, 2015-4:08:38 PM
What I do:
I extract feature from embedding language model
Mostly for kde lm
Gaussian use almost same assumption as termpair distance
What's my input:
I am subclass of EmbeddingFeatureExtractorC
What's my output:

@author: chenyanxiong
'''

import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from cxBase.Vector import VectorC
import logging
import numpy as np

from EmbeddingFeatureExtractor import EmbeddingFeatureExtractorC
from ContinuousLanguageModel.KernelDensityLm import KernelDensityLmC

class EmbeddingLmFeatureExtractorC(EmbeddingFeatureExtractorC):
    def Init(self):
        EmbeddingFeatureExtractorC.Init(self)
        self.FeatureName = 'EmbLm'
        
        
    def Extract(self, qid, query, doc, Word2VecModel):
        EmbeddingFeatureExtractorC.Extract(self, qid, query, doc, Word2VecModel)
        
        '''
        not using fields at all. as the estimator can only work for longer content
        only using kde with default kernel (Gaussian) and CVed bandwidth per doc
        '''
        
        lQVec = [Word2VecModel(qterm) for qterm in  query.split() if qterm in Word2VecModel]
        lDVec = [Word2VecModel(term) for term in doc.GetContent().split() if term in Word2VecModel]
        
        hFeature = {}
        
        hFeature.update(self.KdeFeatures(lQVec,lDVec))
        
        return hFeature
    
    def KdeFeatures(self,lQVec,lDVec):
        '''
        the mean of p(q|kde-D)
        '''
        
        DocKdeLm = KernelDensityLmC(lDVec)
        
        FeatureName = self.FeatureName  + 'Kde'
        lScore = [DocKdeLm.pdf(QVec) for QVec in lQVec]
        score = np.mean(lScore)
        hFeature = {FeatureName:score}
        return hFeature
        
        
        
        
    


