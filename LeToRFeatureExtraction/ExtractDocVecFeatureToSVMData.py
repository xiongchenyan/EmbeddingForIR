'''
Created on Feb 21, 2015 1:36:21 PM
@author: cx

what I do:
Add doc vec feature to SVM data
Things it configure:
    which query part to use? topic|desp
    what distance to use? raw|abs|l2
what's my input:
SVMData
TargetEmbeddings (query is marked as TrecWebTrack-id)

what's my output:
a new SVM data, with features


'''


import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/GoogleAPI')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
site.addsitedir('/bos/usr0/cx/PyCode/cxMachineLearning')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from word2vec.WordVecBase import Word2VecC,Word2VecReaderC
from cxBase.Vector import VectorC
from LeToR.LeToRDataBase import LeToRDataBaseC

class ExtractDocVecFeatureToSVMDataC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.hDocVec = {}
        self.DistanceType = "abs"
        self.QField = "topic"
        self.DocVecInName = ""
        self.OverWrite = False
    
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DistanceType = self.conf.GetConf('distype', self.DistanceType)
        self.QField = self.conf.GetConf('qfield', self.QField)
        self.DocVecInName = self.conf.GetConf('docvecin')
        self.OverWrite = bool(int(self.conf.GetConf('overwrite',0)))
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "distype abs|raw|l2|cos\nqfield topic|desp\ndocvecin\noverwrite 0"
    
    def SegQIdField(self,QName):
        vCol = QName.split('_')
        qid,field = "",""
        if len(vCol) < 2:
            return qid,field
        if len(vCol) > 3:
            return qid,field
            
        Id = vCol[1]
        if len(vCol) == 2:
            field = 'topic'
        else:
            field = 'desp'
        return Id,field
        
        
    def LoadDocVec(self):
        Reader = Word2VecReaderC()
        Reader.open(self.DocVecInName)
        for wordvec in Reader:
            if 'TrecWebTrack' in wordvec.word:
                Qid,field = self.SegQIdField(wordvec.word)
                if field != self.QField:
                    continue
                self.hDocVec[Qid] = wordvec
            else:
                self.hDocVec[wordvec.word] = wordvec
        print 'docvec loaded, total [%d]' %(len(self.hDocVec))
        return True
    
    
    def GenerateEmbeddingFeatureVector(self,QVec,DocVec):
        ResVec = Word2VecC()
        if self.OverWrite:
            StFeatureDim = 1
        else:
            StFeatureDim = self.StFeatureDim
        if self.DistanceType == 'abs':
            ResVec = abs(QVec - DocVec)
        if self.DistanceType == 'raw':
            ResVec = QVec - DocVec
        if self.DistanceType == 'l2':
            ResVec = Word2VecC.PointWiseL2(QVec, DocVec)
            
        if self.DistanceType == 'cos':
            score = Word2VecC.cosine(QVec, DocVec)
            ResVec.hDim[0] = score
            
        FeatureVec = VectorC()
        for key,value in ResVec.hDim.items():
            NewKey = key + StFeatureDim
            FeatureVec.hDim[NewKey] = value
        return FeatureVec
    
    def ReadSVMForMaxFeatureDim(self,SVMInName):
        self.StFeatureDim = 0
        for line in open(SVMInName):
            LeToRData = LeToRDataBaseC(line.strip())
            self.StFeatureDim = max(self.StFeatureDim,max(LeToRData.hFeature.keys()))
        self.StFeatureDim += 1
        print "new feature start from [%d]" %(self.StFeatureDim)
    
    def ProcessOneInstance(self,LeToRData):
        Qid = LeToRData.qid
        DocNo = LeToRData.DocNo
        if (not Qid in self.hDocVec) :
            #do nothing
            print 'Qid[%s] doc vec not found' %(Qid)
            return LeToRData
        if (not DocNo in self.hDocVec):
            print 'Doc[%s] doc vec not found' %(DocNo)
            return LeToRData
        
        FeatureVec = self.GenerateEmbeddingFeatureVector(self.hDocVec[Qid], self.hDocVec[DocNo])
        if self.OverWrite:
            LeToRData.hFeature = FeatureVec.hDim
        else:
            LeToRData.hFeature.update(FeatureVec.hDim)
        
        return LeToRData
    
    def Process(self,SVMInName,OutName):
        self.LoadDocVec()
        self.ReadSVMForMaxFeatureDim(SVMInName)
        
        out = open(OutName,'w')
        for line in open(SVMInName):
            LeToRData = LeToRDataBaseC(line.strip())
            LeToRData = self.ProcessOneInstance(LeToRData)
            print >> out,LeToRData.dumps()
        out.close()
        print "finished"
        
        
import sys
if 2 != len(sys.argv):
    ExtractDocVecFeatureToSVMDataC.ShowConf()
    print "in\nout"    
    sys.exit()
    
conf = cxConfC(sys.argv[1])
SVMInName = conf.GetConf('in')
OutName = conf.GetConf('out')

Extractor = ExtractDocVecFeatureToSVMDataC(sys.argv[1])
Extractor.Process(SVMInName, OutName)

    
        
        
        
        
        
        
        
        
        
        
    
    
                
        
        
        
        
        
        