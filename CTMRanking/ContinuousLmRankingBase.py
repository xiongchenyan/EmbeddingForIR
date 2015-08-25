'''
Created on my MAC Aug 24, 2015-9:48:06 PM
What I do:

What's my input:
    I am the base class to ranking and evaluate using continuous lm
What's my output:
    I provide API to be called by training and testing
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
import gensim

class ContinuousLmRankingBaseC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Evaluator = AdhocEvaC()
        self.Searcher = IndriSearchCenterC()
        self.Word2VecInName = ""
        self.Word2VecModel = None
        self.cLmName = "kde"
        self.LmClass = KernelDensityLmC
        
        
        #lm conf input
        self.ParaConf = cxConfC()
        
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Searcher.SetConf(ConfIn)
        self.Evaluator.SetConf(ConfIn)
        
        self.cLmName = self.conf.GetConf('lmname', self.cLmName)
        self.SetLmClass()
        
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
        print 'word2vecin'
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
        Lm.SetPara(self.ParaConf)
        Lm.Construct(lTerm,self.Word2VecModel)
        return Lm
    
    
    def FormPerQData(self,qid,query):
        lDoc = self.Searcher.RunQuery(query, qid)
        lLm = [self.FormLm(doc) for doc in lDoc]
        
        return lDoc,lLm
    
    def Process(self,QueryInName,ParaStr,OutName,WithRankingOut = False):
        '''
        evaluate cLmName on QueryInName's queries
        evaluation result output to OutName
        '''
        
        
        self.ParaConf.ParseParaStr(ParaStr)   #will be used to init lm model's parameter too
        
        BaseConfInName = self.ParaConf.GetConf('baseconf')
        self.SetConf(BaseConfInName)
        
        
        
        
        
        
        lQidQuery = [line.split('\t') for line in open(QueryInName).read().splitlines()]
        
        
        
        
        lEvaRes = []
        
        if WithRankingOut:
            RankOut = open(OutName + '_rank','w')
        
        logging.info('start evaluating...')
        for qid,query in lQidQuery:
            lDoc,lLm = self.FormPerQData(qid, query)
            EvaRes,lDocNo,lScore = self.ReRankAndEvaPerQ(qid, query, lDoc, lLm)
            lEvaRes.append(EvaRes)
            
            if WithRankingOut:
                for i in range(len(lDocNo)):
                    print >> RankOut, qid + ' Q0 ' + lDocNo[i] + ' %d %f %s'%(i+1,lScore[i],self.cLmName)
        
        if WithRankingOut:
            RankOut.close()
            
        MeanRes = AdhocMeasureC.AdhocMeasureMean(lEvaRes)
        lEvaRes.append(MeanRes)
        out = open(OutName,'w')
        
        if WithRankingOut:
            for QidQuery,EvaRes in zip(lQidQuery,lEvaRes):
                print >>out, QidQuery[0] + '\t' + EvaRes.dumps()
        else:
            print >>out, MeanRes.Err
        out.close()
        logging.info('evaluation res %s',MeanRes.dumps())
        
        return True
    
    
    def SetLmClass(self):
        '''
        select proper class name for cLmName
        '''
        
        if self.cLmName == 'gaussian':
            logging.info('use gaussian clm')
            self.LmClass = GaussianLmC
            return True
            
        if self.cLmName == 'kde':
            logging.info('use kde lm')
            self.LmClass =  KernelDensityLmC
            return True
        
        if self.cLmName == 'sum':
            logging.info('use raw sum')
            self.LmClass =  SummationLmC
            return True
        
        if self.cLmName == 'rand':
            logging.info('use rand')
            self.LmClass =  RandLmC
            return True
        
        raise NotImplementedError('please choose continuous language model from gaussian|kde')
    
    
