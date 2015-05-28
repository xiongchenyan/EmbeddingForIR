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
from sklearn.decomposition import PCA
from EmbeddingFeatureExtractor import EmbeddingFeatureExtractorC
from ContinuousLanguageModel.KernelDensityLm import KernelDensityLmC
import random

class EmbeddingLmFeatureExtractorC(EmbeddingFeatureExtractorC):
    def Init(self):
        EmbeddingFeatureExtractorC.Init(self)
        self.FeatureName = 'EmbLm'
        self.PCADim = 0
        self.MaxDocLen = 5000
    
    def SetConf(self, ConfIn):
        EmbeddingFeatureExtractorC.SetConf(self, ConfIn)
        self.PCADim = int(self.conf.GetConf('pcadim', self.PCADim))    
        
    def Extract(self, qid, query, doc, Word2VecModel):
        EmbeddingFeatureExtractorC.Extract(self, qid, query, doc, Word2VecModel)
        
        '''
        not using fields at all. as the estimator can only work for longer content
        only using kde with default kernel (Gaussian) and CVed bandwidth per doc
        '''
        
        lQTerm = query.split()
        lDocTerm = doc.GetContent().split()
        
        if len(lDocTerm) > self.MaxDocLen:
            logging.warn('doc too long [%s][%d], sample [%d] term',doc.DocNo,len(lDocTerm), self.MaxDocLen)
            random.shuffle(lDocTerm)
            lDocTerm = lDocTerm[:self.MaxDocLen]
        
        
        lQVec = [Word2VecModel[qterm] for qterm in  lQTerm if qterm in Word2VecModel]
        lDVec = [Word2VecModel[term] for term in lDocTerm if term in Word2VecModel]
        
        if [] == lQVec:
            logging.warn('[%s][%s] has no word2vec',qid,query)
            return {}
        if [] == lDVec:
            logging.warn('[%s][%s] has no word2vec',qid,doc.DocNo)
            return {}
        
        if 0 != self.PCADim:
            lQVec,lDVec = self.PCAVec(lQVec,lDVec)
        
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
    
    def PCAVec(self,lQVec,lDVec):
        lVec = lQVec + lDVec
        pca = PCA(n_components=self.PCADim, whiten=False)
        lPCAVec = pca.fit_transform(lVec)
        lPCAQVec = lPCAVec[:len(lQVec)]
        lPCADVec = lPCAVec[len(lQVec):]
        logging.debug('qvec and doc word2vec pca to [%d] dim',self.PCADim)
        return lPCAQVec,lPCADVec
        
        
        
        
    


