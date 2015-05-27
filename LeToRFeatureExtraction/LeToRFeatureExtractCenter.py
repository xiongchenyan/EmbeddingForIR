'''
Created on my MAC May 25, 2015-3:09:00 PM
What I do:
I configure and call all feature extraction classes to extract features
for a given q-doc pair

I also support pipe line run for a query
    retrieval
    + feature extraction
What's my input:
query
What's my output:
q-doc svm style output
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
import gensim
import logging
import numpy as np
import json
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from LeToRGivenFeatureExtractor import LeToRGivenFeatureExtractorC
from EmbeddingTermPairFeatureExtractor import EmbeddingTermPairFeatureExtractorC
from EmbeddingLmFeatureExtractor import EmbeddingLmFeatureExtractorC


from LeToR.LeToRDataBase import LeToRDataBaseC
from AdhocEva.AdhocQRel import AdhocQRelC


class LeToRFeatureExtractCenterC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Prepared = False
        
        self.Word2VecInName = ""
        self.Word2VecModel = None
        
        self.lFeatureGroup = []
        self.Searcher = IndriSearchCenterC()
        self.GivenFeatureExtractor = LeToRGivenFeatureExtractorC()
        self.EmbTermPairFeatureExtractor = EmbeddingTermPairFeatureExtractorC()
        self.EmbLmFeatureExtractor = EmbeddingLmFeatureExtractorC()
        self.QRelCenter = AdhocQRelC()
        self.QRelIn = ""
        
    
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.Word2VecInName = self.conf.GetConf('word2vecin')
        
        self.lFeatureGroup = self.conf.GetConf('featuregroup')
        
        self.QRelIn = self.conf.GetConf('qrel')
        self.QRelCenter.Load(self.QRelIn)
        if type(self.lFeatureGroup) != list:
            self.lFeatureGroup = [self.lFeatureGroup]
            
        self.Searcher.SetConf(ConfIn)
        
        if 'givenfeature' in self.lFeatureGroup:
            self.GivenFeatureExtractor.SetConf(ConfIn)
            
        if 'termpairemb' in self.lFeatureGroup:
            self.EmbTermPairFeatureExtractor.SetConf(ConfIn)
            
        if 'emblm' in self.lFeatureGroup:
            self.EmbLmFeatureExtractor.SetConf(ConfIn)
            
            
        return True
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print 'word2vecin\nfeaturegroup givenfeature|termpairemb\nqrel\nemblm'
        LeToRGivenFeatureExtractorC.ShowConf()
        EmbeddingTermPairFeatureExtractorC.ShowConf()
        EmbeddingLmFeatureExtractorC.ShowConf()
        IndriSearchCenterC.ShowConf()
        
    def Prepare(self):
        if self.Prepared:
            return
        
        
        
        logging.info('start load word2vec input')
        self.Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(self.Word2VecInName)
        logging.info('word2vec loaded')
        if 'givenfeature' in self.lFeatureGroup:
            self.GivenFeatureExtractor.Prepare()
        if 'termpairemb' in self.lFeatureGroup:
            self.EmbTermPairFeatureExtractor.Prepare()
        if 'emblm' in self.lFeatureGroup:
            self.EmbLmFeatureExtractor.Prepare()
        
        self.Prepared = True
        return
    
    def Process(self, qid,query,doc):
        '''
        extract all features here
        '''
        self.Prepare()
        
        
        hFeature = {}
        
        if 'givenfeature' in self.lFeatureGroup:
            hFeature.update(self.GivenFeatureExtractor.Extract(qid, query, doc))
            logging.debug('given feature extracted')
        
        if 'termpairemb' in self.lFeatureGroup:
            hFeature.update(self.EmbTermPairFeatureExtractor.Extract(qid, query, doc, self.Word2VecModel))
            logging.debug('termpairemb feature extracted')
            
        if 'emblm' in self.lFeatureGroup:
            hFeature.update(self.EmbLmFeatureExtractor.Extract(qid, query, doc, self.Word2VecModel))
            logging.debug('emblm feature extracted')
            
        return hFeature
    
    
    def PipeLineRun(self,QInName,OutName):
        '''
        will make a feature hash myself... It should be OK right?
        '''
        hFeatureName = {}
        self.Prepare()
        lLines = open(QInName).read().splitlines()
        lQidQuery = [line.split('\t') for line in lLines]
        out = open(OutName,'w')
        
        logging.info('start extracting for file [%s]',QInName)
        for qid,query in lQidQuery:
            lDoc = self.Searcher.RunQuery(query, qid)
            for doc in lDoc:
                hFeature = self.Process(qid, query, doc)
                LTRData = LeToRDataBaseC()
                LTRData.qid = qid
                LTRData.DocNo = doc.DocNo
                LTRData.hFeature = hFeature
                
                LTRData.score = self.QRelCenter.GetScore(qid, doc.DocNo)
                hFeatureName = LTRData.HashFeatureName(hFeatureName)
                print >>out,LTRData.dumps()
                
            logging.info('qid [%s] extracted',qid)
            
        out.close()
        
        NameOut = open(OutName + '_FeatureName','w')
        for name,Id in hFeatureName.items():
            print >>NameOut,'%d\t%s' %(Id,name)
        NameOut.close()
        logging.info('finished')
        return
    
    
if __name__ == '__main__':
    import sys
    if 2 != len(sys.argv):
        LeToRFeatureExtractCenterC.ShowConf()
        print "in\nout"    
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    
    Extractor = LeToRFeatureExtractCenterC(sys.argv[1])
    Extractor.PipeLineRun(QInName, OutName)
        
        
        
        
        
    
    
    
    
        
        
        
        
        
        
    
