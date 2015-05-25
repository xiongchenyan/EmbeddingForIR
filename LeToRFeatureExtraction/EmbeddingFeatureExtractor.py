'''
Created on my MAC May 25, 2015-1:59:43 PM
What I do:
I am the virtual class to define API and pre load stuff for letor feature extraction from embedding
What's my input:
q, doc, Word2VecModel
What's my output:
hFeature for this pair
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
from gensim.models.doc2vec  import *
import logging
import numpy as np
import json

from LeToRFeatureExtractor import LeToRFeatureExtractorC


class EmbeddingFeatureExtractorC(LeToRFeatureExtractorC):
    
    def Extract(self,qid,query,doc,Word2VecModel):
        '''
        Is this the right design pattern?
        '''
        LeToRFeatureExtractorC.Extract(self, qid, query, doc)
        hFeature = {}
        return hFeature

    def FetchQTermEmbedding(self,query,Word2VecModel):
        lVector = []
        lQTerm = query.lower().split()
        
        for qt in lQTerm:
            if not qt in Word2VecModel:
                continue
            lVector.append(VectorC(list(Word2VecModel[qt])))
        return lVector
    
    def FetchDocTermEmbedding(self,doc,Word2VecModel):
        lTerm = doc.GetContent().lower().split()
        lVector = [VectorC(list(Word2VecModel[term])) for term in lTerm if term in Word2VecModel]
        return lVector
    
        