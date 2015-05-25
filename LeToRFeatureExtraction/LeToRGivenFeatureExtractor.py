'''
Created on my MAC May 25, 2015-2:12:30 PM
What I do:
I just read the given features in conf file
What's my input:
I am the sub class of LeToRFeatureExtractorC
conf: existingsvmdata
What's my output:
hFeature={1:as loaded etc.}
@author: chenyanxiong
'''

import logging
from LeToRFeatureExtractor import LeToRFeatureExtractorC
from LeToR.LeToRDataBase import LeToRDataBaseC
class LeToRGivenFeatureExtractorC(LeToRFeatureExtractorC):
    
    def Init(self):
        LeToRFeatureExtractorC.Init(self)
        self.hQidDocFeature = {}  #stuff to preload
        self.ExistingSVMInName = ""
        
    def SetConf(self, ConfIn):
        LeToRFeatureExtractorC.SetConf(self, ConfIn)
        self.ExistingSVMInName = self.conf.GetConf('existingsvmdata')
    
    @staticmethod
    def ShowConf():
        LeToRFeatureExtractorC.ShowConf()    
        print 'existingsvmdata'
        
        
    def Prepare(self):
        LeToRFeatureExtractorC.Prepare(self)
        self.LoadExistingSVMData()
        
    def LoadExistingSVMData(self):
        lLines = open(self.ExistingSVMInName).read().splitlines()
        lLTRData = [LeToRDataBaseC(line) for line in lLines]
        for LTRData in lLTRData:
            key = LTRData.qid + ' ' + LTRData.DocNo
            self.hQidDocFeature[key] = dict(LTRData.hFeature)
        logging.info('existing svm feature loaded from [%s]',self.ExistingSVMInName)
        return True
    
    
    def Extract(self, qid, query, doc):
        LeToRFeatureExtractorC.Extract(self, qid, query, doc)
        hFeature = {}
        key = qid  + ' ' + doc.DocNo
        if not key in self.hQidDocFeature:
            logging.warn('[%s] feature not in predefined svm data [%s]',key,self.ExistingSVMInName)
            return {}
        hFeature = self.hQidDocFeature[key]
        return hFeature
        
        
        
        
        