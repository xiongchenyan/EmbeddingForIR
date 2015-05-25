'''
Created on my MAC May 25, 2015-2:04:14 PM
What I do:
I am the base class to extract feature vector for a given qid, query, doc.
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
from IndriSearch.IndriDocBase import IndriDocBaseC
import logging
import numpy as np
import json



class LeToRFeatureExtractorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Prepared = False
        return
    
    def Prepare(self):
        self.Prepared = True
        return
    
    def Extract(self,qid,query,doc):
        if not self.Prepared:
            self.Prepare()
        hFeature = {}
        return hFeature
    
    