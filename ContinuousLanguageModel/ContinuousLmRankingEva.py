'''
Created on my MAC Jul 28, 2015-9:08:06 PM
What I do:
    I evaluate the  ranking performance of continuous Lm
What's my input:
    qid,query, lDoc, and lDoc's lm
    qrel
What's my output:
    eva res of this query
    
Also support pipeline run, and with configuration
@author: chenyanxiong
'''



import site
import logging


site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC
from ContinuousLanguageModel.GaussianLm import GaussianLmC
from ContinuousLanguageModel.KernelDensityLm import KernelDensityLmC
from ContinuousLanguageModel.SummationLm import SummationLmC
from ContinuousLanguageModel.RandomLm import RandLmC
from ContinuousLanguageModel.RadiusMatchLm import RadiusMatchLmC
import gensim
import numpy as np

class ContinuousLmRankingEvaluatorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Evaluator = AdhocEvaC()
        self.Searcher = IndriSearchCenterC()
        self.Word2VecInName = ""
        self.Word2VecModel = None
        self.lLmName = []
        self.LmClass = None
        self.lOutName = []
        self.QueryInName = ""
        
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Searcher.SetConf(ConfIn)
        self.Evaluator.SetConf(ConfIn)
        
        self.lLmName = self.conf.GetConf('lmname', self.lLmName)
        
        self.QueryInName = self.conf.GetConf('in')
        self.lOutName = self.conf.GetConf('out', self.lOutName)
        
        self.Word2VecInName = self.conf.GetConf('word2vecin',self.Word2VecInName)
        self.LoadWord2Vec()
        
        
    def LoadWord2Vec(self):
        logging.info('start load word2vec input')
        self.Word2VecModel = gensim.models.Word2Vec.load_word2vec_format(self.Word2VecInName)
        logging.info('word2vec loaded')
        
        
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        print    cls.__name__
        print 'word2vecin\nkernel\nlmname\nbandwidth\nin\nout'
        IndriSearchCenterC.ShowConf()
        AdhocEvaC.ShowConf()
        
    def ReRankAndEvaPerQ(self,qid,query,lDoc,lLm):
        
        lReRankDocNo,lScore = self.FormNewRank(query,lDoc,lLm)
        EvaRes = self.Evaluator.EvaluatePerQ(qid, query, lReRankDocNo)
        logging.info('[%s][%s] result [%s]',qid,query,EvaRes.dumps())
        return EvaRes,lReRankDocNo,lScore
    
    def FormNewRank(self,query,lDoc,lLm):
        
        lQTerm = query.split()
        if [] == lQTerm:
            return self.MinLogPdf
        lQX = [self.Word2VecModel[term] for term in lQTerm if term in self.Word2VecModel]
        
        lScore = [lm.InferenceQVec(lQX) for lm in lLm]
        lDocScore = zip(lDoc,lScore)
        lDocScore.sort(key=lambda item: item[1], reverse = True)
        lDocNo = [item[0].DocNo for item in lDocScore]
        lScore = [item[1] for item in lDocScore]
        return lDocNo,lScore
    
    
    def FormLm(self,doc):
        lTerm = doc.GetContent().split()
        Lm = self.LmClass()
        Lm.SetPara(self.conf)
        Lm.Construct(lTerm,self.Word2VecModel)
        return Lm
    
    
    def FormPerQData(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        lLm = [self.FormLm(doc) for doc in lDoc]
        
        return lDoc,lLm
    
   
    
    
    def SetLmClass(self,cLmName):
        '''
        select proper class name for cLmName
        '''
        
        if cLmName == 'gaussian':
            logging.info('use gaussian clm')
            self.LmClass = GaussianLmC
            return True
            
        if cLmName == 'kde':
            logging.info('use kde lm')
            self.LmClass =  KernelDensityLmC
            return True
        
        if cLmName == 'sum':
            logging.info('use raw sum')
            self.LmClass =  SummationLmC
            return True
        
        if cLmName == 'rand':
            logging.info('use rand')
            self.LmClass =  RandLmC
            return True
        
        if cLmName == 'radius':
            logging.info('us radius')
            self.LmClass = RadiusMatchLmC
        
        raise NotImplementedError('please choose continuous language model from gaussian|kde')
    
    
    def Process(self):
        
        for OutName,cLmName in zip(self.lOutName,self.lLmName):
            self.RunForOneLm(self.QueryInName, OutName, cLmName)

    
    def RunForOneLm(self,QueryInName,OutName,cLmName):
        '''
        evaluate cLmName on QueryInName's queries
        evaluation result output to OutName
        '''
        
        lQidQuery = [line.split('\t') for line in open(QueryInName).read().splitlines()]
        
        self.SetLmClass(cLmName)
        
        lEvaRes = []
        
        RankOut = open(OutName + '_rank','w')
        
        logging.info('start evaluating...')
        for qid,query in lQidQuery:
            lDoc,lLm = self.FormPerQData(qid, query)
            EvaRes,lDocNo,lScore = self.ReRankAndEvaPerQ(qid, query, lDoc, lLm)
            lEvaRes.append(EvaRes)
            
            for i in range(len(lDocNo)):
                print >> RankOut, qid + ' Q0 ' + lDocNo[i] + ' %d %f %s'%(i+1,lScore[i],cLmName)
        
        RankOut.close()
            
        lEvaRes.append(AdhocMeasureC.AdhocMeasureMean(lEvaRes))
        lQid = [item[0] for item in lQidQuery] + ['mean']
        
        out = open(OutName,'w')
        
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('evaluation res %s',lEvaRes[-1].dumps())
        
        return True
  
    
    
if __name__=='__main__':
    import sys
    if 2 != len(sys.argv):
        ContinuousLmRankingEvaluatorC.ShowConf()
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    
    Evaluator = ContinuousLmRankingEvaluatorC(sys.argv[1])
    Evaluator.Process()
        
    

    
    
    
    
        
