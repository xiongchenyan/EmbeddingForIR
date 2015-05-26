'''
Created on my MAC May 25, 2015-2:33:30 PM
What I do:
Extract features from term pairwise similarity
to enumerate:
    doc fields (predefined in conf)
    max, min, mean between all q-d field's terms
    cosine | L2 distance
do:
    for each field:
        for each similarity method:
            formulate the pairwise similarity matrix
            max,min,mean of them as features
    
What's my input:

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

from EmbeddingFeatureExtractor import EmbeddingFeatureExtractorC

class EmbeddingTermPairFeatureExtractorC(EmbeddingFeatureExtractorC):
    def Init(self):
        EmbeddingFeatureExtractorC.Init(self)
        self.lDocField = ['title','inlink','body']
        self.lSimMetric = ['cosine','l2']
        self.lMergeMetric = ['max','min','mean']
        self.FeatureName = 'EmbTermPair'
        
    def SetConf(self, ConfIn):
        EmbeddingFeatureExtractorC.SetConf(self, ConfIn)
        self.lDocField = self.conf.GetConf('docfield', self.lDocField)
        if type(self.lDocField) != list:
            self.lDocField = [self.lDocField]
        
        self.lSimMetric = self.conf.GetConf('simmetric', self.lSimMetric)
        if type(self.lSimMetric) != list:
            self.lSimMetric = [self.lSimMetric]
        
        self.lMergeMetric = self.conf.GetConf('mergemetric', self.lMergeMetric)
        if type(self.lMergeMetric) != list:
            self.lMergeMetric = [self.lMergeMetric]
            

    @staticmethod
    def ShowConf():
        EmbeddingFeatureExtractorC.ShowConf()
        print 'docfield\nsimmetric\nmergemetric'
        
        
    def Extract(self, qid, query, doc, Word2VecModel):
        EmbeddingFeatureExtractorC.Extract(self, qid, query, doc, Word2VecModel)
        hFeature = {}
        lQVec = self.FetchQTermEmbedding(query, Word2VecModel)
        if len(lQVec) != len(query.strip()):
            logging.warn('query [%s] only [%d/%d] found in word2vec',query,len(lQVec),len(query.strip()))
        
        for field in self.lDocField:
            lTerm = doc.GetField(field).lower().split()
            lDVec = [VectorC(list(Word2VecModel[term])) for term in lTerm if term in Word2VecModel]
            if len(lDVec) != len(lTerm):
                logging.warn('doc [%s][%s] only [%d/%d] found in word2vec',doc.DocNo,field,len(lDVec),len(lTerm))
            for SimMetric in self.lSimMetric:
                for MergeMetric in self.lMergeMetric:
                    score = self.CalcPairWiseSim(lQVec,lDVec,SimMetric,MergeMetric)
                    FeatureName = self.FeatureName + field + SimMetric + MergeMetric
                    hFeature[FeatureName] = score
        
        return hFeature
    
    
    def CalcPairWiseSim(self,lQVec,lDVec,SimMetric,MergeMetric):
        
        score = -1
        cnt = 0
        for QVec in lQVec:
            for DVec in lDVec:
                ThisScore = VectorC.Similarity(QVec, DVec, SimMetric)
                cnt += 1
                if -1 == score:
                    score = ThisScore
                    continue
                if MergeMetric == 'min':
                    score = min(score,ThisScore)
                if MergeMetric == 'max':
                    score = max(score,ThisScore)
                if MergeMetric == 'mean':
                    score += ThisScore
        if MergeMetric == 'mean':
            score /= float(cnt)
        return score
                    
                
                
        
        
                
                
             
        
        
        
        
        
        
        
