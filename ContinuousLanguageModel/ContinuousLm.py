'''
Created on my MAC Jul 28, 2015-9:15:00 PM
What I do:
    I am the base class for continuous language model (with word embedding)
What's my input:
    I form language model (continuous version) with given set of terms,
        and word embedding model
What's my output:

@author: chenyanxiong
'''
from cxBase.Conf import cxConfC
import math


class ContinuousLmC(object):
    def __init__(self,lTerm = [],Word2VecModel = None):
        self.Init()
        if ([] != lTerm):
            self.Construct(lTerm,Word2VecModel)
            
            
    def Init(self):
        self.MinLogPdf = -20
        
        
    def Construct(self,lData,Word2VecModel):
        raise NotImplementedError('clm construct func not implemented')
        
    
    
    def pdf(self,x):
        raise NotImplementedError('clm pdf func not implemented')
    
    
    def LogPdf(self,x):
        return max(self.MinLogPdf,math.log(self.pdf(x)))
    
    def InferenceQuery(self,query,Word2VecModel):
        lQTerm = query.split()
        if [] == lQTerm:
            return self.MinLogPdf
        lQX = [Word2VecModel[term] for term in lQTerm if term in Word2VecModel]
        return self.InferenceQVec(lQX)
    
    def InferenceQVec(self,lQX):
        if [] == lQX:
            return self.MinLogPdf
        score = sum([self.LogPdf(x) for x in lQX]) / float(len(lQX))
        
        return score