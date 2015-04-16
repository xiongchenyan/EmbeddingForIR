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


'''
Apr 16 2015
Support loading gensim doc2vec format
load the model in LoadDocVec (but not store in hDocVec)
for each pair of qid and doc, fetch them before throw into generator
    pack gensim vector to VectorC() format as well
this will be rather memory consuming    

need do a docno-> internal id mapping for gensim first = =
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
from gensim.models.doc2vec  import *
import logging
class ExtractDocVecFeatureToSVMDataC(cxBaseC):
    def Init(self):
        cxBaseC.Init(self)
        self.hDocVec = {}
        self.DocVecModel = None
        self.hDocNoInternalId = {}
        self.DistanceType = "abs"
        self.QField = "topic"
        self.DocVecInName = ""
        self.OverWrite = False
        self.DocVecInType = 'text'
        self.DocNoInName = ""
    
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        self.DistanceType = self.conf.GetConf('distype', self.DistanceType)
        self.QField = self.conf.GetConf('qfield', self.QField)
        self.DocVecInName = self.conf.GetConf('docvecin')
        self.OverWrite = bool(int(self.conf.GetConf('overwrite',0)))
        self.DocVecInType = self.conf.GetConf('docvecintype', self.DocVecInType)
        self.DocNoInName = self.conf.GetConf('docnoinname')
    
    @staticmethod
    def ShowConf():
        cxBaseC.ShowConf()
        print "distype abs|raw|l2|cos\nqfield topic|desp\ndocvecin\noverwrite 0"
        print 'docvecintype text|gensim\ndocnoinname'
    
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
        
        if self.DocVecInType == 'text':
            self.LoadTextDocVec()
            
        if self.DocVecInType == 'gensim':
            self.LoadGensimDocVec()
            lLines = open(self.DocNoInName).read().splitlines()
            lInternalId = ['SENT_%s' %(i) for i in range(len(lLines))]
            self.hDocNoInternalId = dict(zip(lLines,lInternalId))
        
        return True
        
    def LoadGensimDocVec(self):
        logging.info('start load gensim doc vec [%s]',self.DocVecInName)
        self.DocVecModel = Doc2Vec.load(self.DocVecInName)
        logging.info('loaded')
        return True
        
        
            
    
    def LoadTextDocVec(self):
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
    
    
    
    def FetchDocVec(self,TargetNo,IsQid = False):
        
        if self.DocVecInType == 'text':
            if not TargetNo in self.hDocVec:
                return None
            return self.hDocVec[TargetNo]
        
        if self.DistanceType == 'gensim':
            if IsQid:
                TargetNo = 'TrecWebTrack_' + TargetNo + '_' + self.QField
            
            if not TargetNo in self.hDocNoInternalId:
                return None
            TargetNo = self.hDocNoInternalId[TargetNo]   #transfer to SENT_%d
            if not TargetNo in self.DocVecModel:
                return None
            VecArray = self.DocVecModel[TargetNo]
            return VectorC(list(VecArray))
            
        
        return None
    
    
    def ProcessOneInstance(self,LeToRData):
        Qid = LeToRData.qid
        DocNo = LeToRData.DocNo
        
        QVec = self.FetchDocVec(Qid, IsQid=True)
        if QVec == None:
            logging.warn('qid [%s] doc vec not found', Qid)
            return LeToRData
        DocVec = self.FetchDocVec(DocNo)
        if DocVec == None:
            logging.warn('doc [%s] doc vec not found',DocNo)
            return LeToRData
        
        FeatureVec = self.GenerateEmbeddingFeatureVector(QVec,DocVec)
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
        


if __name__ == '__main__':        
    import sys
    if 2 != len(sys.argv):
        ExtractDocVecFeatureToSVMDataC.ShowConf()
        print "in\nout"    
        sys.exit()
    
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
        
    conf = cxConfC(sys.argv[1])
    SVMInName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    
    Extractor = ExtractDocVecFeatureToSVMDataC(sys.argv[1])
    Extractor.Process(SVMInName, OutName)

    
        
        
        
        
        
        
        
        
        
        
    
    
                
        
        
        
        
        
        