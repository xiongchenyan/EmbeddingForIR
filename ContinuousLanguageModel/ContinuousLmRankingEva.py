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
from ContinuousLanguageModel.GaussianLm import GaussianLmC
from ContinuousLanguageModel.KernelDensityLm import KernelDensityLmC

site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')
from cxBase.Conf import cxConfC
from cxBase.base import cxBaseC
from AdhocEva.AdhocEva import AdhocEvaC
from AdhocEva.AdhocMeasure import AdhocMeasureC
from IndriSearch.IndriSearchCenter import IndriSearchCenterC

class ContinuousLmRankingEvaluatorC(cxBaseC):
    
    def Init(self):
        cxBaseC.Init(self)
        self.Evaluator = AdhocEvaC()
        self.Searcher = IndriSearchCenterC()
        
        
    def SetConf(self, ConfIn):
        cxBaseC.SetConf(self, ConfIn)
        
        self.Evaluator.SetConf(ConfIn)
        
    @classmethod
    def ShowConf(cls):
        cxBaseC.ShowConf()
        print    cls.__name__
        
        IndriSearchCenterC.ShowConf()
        AdhocEvaC.ShowConf()
        
    def EvaluatePerQ(self,qid,query,lDoc,lLm):
        
        lReRankDocNo = self.FormNewRank(query,lDoc,lLm)
        EvaRes = self.Evaluator.EvaluatePerQ(qid, query, lReRankDocNo)
        logging.info('[%s][%s] result [%s]',qid,query,EvaRes.dumps())
        return EvaRes
    
    def FormNewRank(self,query,lDoc,lLm):
        
        lScore = [lm.InferenceQuery(query) for lm in lLm]
        lDocScore = zip(lDoc,lScore)
        lDocScore.sort(key=lambda item: item[1], reverse = True)
        lDocNo = [item[0].DocNo for item in lDocScore]
        return lDocNo
    
    
    def FormLm(self,doc,cLmClass):
        lTerm = doc.GetContent().split()
        return cLmClass(lTerm)
    
    
    def FormPerQData(self,qid,query,cLmClass):
        lDoc = self.Searcher.RunQuery(query, qid)
        lLm = [self.FormLm(doc, cLmClass) for doc in lDoc]
        
        return lDoc,lLm
    
    def PipeEva(self,QueryInName,OutName,cLmName):
        '''
        evaluate cLmName on QueryInName's queries
        evaluation result output to OutName
        '''
        
        lQidQuery = [line.split('\t') for line in open(QueryInName).read().splitlines()]
        
        cLmClass = self.SelectcLmClass(cLmName)
        
        lEvaRes = []
        
        logging.info('start evaluating...')
        for qid,query in lQidQuery:
            lDoc,lLm = self.FormPerQData(qid, query, cLmClass)
            EvaRes = self.EvaluatePerQ(qid, query, lDoc, lLm)
            lEvaRes.append(EvaRes)
            
        lEvaRes.append(AdhocMeasureC.AdhocMeasureMean(lEvaRes))
        lQid = [item[0] for item in lQidQuery] + ['mean']
        
        out = open(OutName,'w')
        
        for qid,EvaRes in zip(lQid,lEvaRes):
            print >>out, qid + '\t' + EvaRes.dumps()
            
        out.close()
        logging.info('evaluation res %s',lEvaRes[-1].dumps())
        
        return True
    
    
    def SelectcLmClass(self,cLmName):
        '''
        select proper class name for cLmName
        '''
        
        if cLmName == 'gaussian':
            logging.info('use gaussian clm')
            return GaussianLmC
            
        if cLmName == 'kde':
            logging.info('use kde lm')
            return KernelDensityLmC
        
        raise NotImplementedError('please choose continuous language model from gaussian|kde')
    
    
    
if __name__=='__main__':
    import sys
    if 2 != len(sys.argv):
        ContinuousLmRankingEvaluatorC.ShowConf()
        print 'in\nout\nlmname gaussian|kde'
        sys.exit()
        
    root = logging.getLogger()
    root.setLevel(logging.INFO)
    
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    root.addHandler(ch)
    
    
    Evaluator = ContinuousLmRankingEvaluatorC(sys.argv[1])
    
    conf = cxConfC(sys.argv[1])
    QInName = conf.GetConf('in')
    OutName = conf.GetConf('out')
    cLmName = conf.GetConf('lmname')
    
    Evaluator.PipeEva(QInName, OutName, cLmName)
        
        
        
    

    

    
    
    
    
        
