'''
Created on Apr 3, 2015 7:34:52 PM
@author: cx

what I do:
    read the matrix format
        label input:
            col1: relevance label
            col -1: qid
        representation input:
            sparse input: doc id, f id, score     (always sparse)
    calculate the within cluster loss for each qid
        \sum_i \in C ||X_i - \mu_C||^2

what's my input:
    label mtx + representation mtx
what's my output:
    qid \t cluster loss score
    .
    .
    .
    mean \t cluster loss
'''


'''
try to use numpy and skilearn for this

numpy load sparse mtx,
and work on the sparse mtx
'''


from scipy.sparse import csc_matrix
import numpy as np

import logging,math

def LoadSparseMtx(InName):
    lLines = open(InName).read().splitlines()
    
    lData = [line.split(',') for line in lLines]
    lData = [[int(item[0]) - 1,int(item[1]) - 1,float(item[2])] for item in lData]
    
    Mtx = np.array(lData)
    logging.info('load full rep mtx shape %d-%d',Mtx.shape[0],Mtx.shape[1])
    SmtxData = csc_matrix((Mtx[:,2],(Mtx[:,0],Mtx[:,1])))
    
#     logging.info('start normalize SmtxData')
#     
#     for i in range(SmtxData.shape[0]):
#         L2Norm = float(math.sqrt(SmtxData.getrow(i).multiply(SmtxData.getrow(i)).sum()))
#         if 0 != L2Norm:
#             SmtxData[i,:] /= L2Norm 
            
    
            
    logging.info('normalized to unit length')
    return SmtxData


def LoadLabelMtx(InName):
    lLines = open(InName).read().splitlines()
    
    lData = [[int(col) for col in line.split(',')] for line in lLines]
    
    LabelMtx = np.array(lData)
    return LabelMtx


def ProcessOneQuery(LabelMtx,ThisRepMtx):
    '''
    LabelMtx is the labels of this query
    ThisRepMtx is corresponding doc mtx
    calculate the inner L2 distance
    '''
    
    '''
    get center for pos and neg (np.array's size? and how to for...)
    go through, and sum up the L2 distance with corresponding centers
    '''
    
    if LabelMtx.shape[0] != ThisRepMtx.shape[0]:
        logging.error('input label mtx and emd mtx shape not equal')
        return
    
    
    logging.info('start working on q [%d]',LabelMtx[0,1])
    PosCenter = csc_matrix(np.zeros(shape = ThisRepMtx.getrow(0).shape))
    NegCenter = csc_matrix(PosCenter)
    
    PosCnt = 0
    NegCnt = 0
    for i in range(LabelMtx.shape[0]):
        if LabelMtx[i,0] > 0:
            PosCenter += ThisRepMtx.getrow(i)
            PosCnt += 1
        else:
            NegCenter += ThisRepMtx.getrow(i)
            NegCnt += 1
    
    if PosCnt != 0:
        PosCenter /= float(PosCnt)
    if NegCnt != 0:
        NegCenter /= float(NegCnt)
    
    logging.info('q [%s] [%d] pos [%d] neg',LabelMtx[0,1],PosCnt,NegCnt)
    
    '''
    start calculate cluster loss
    '''        
    
    SameClassDis = 0
    DiffClassDis = 0
    for i in range(LabelMtx.shape[0]):
        ThisRow = ThisRepMtx.getrow(i)
        if LabelMtx[i,0] > 0:
            SameDiff = ThisRow - PosCenter
            DiffDiff = ThisRow  - NegCenter
        else:
            DiffDiff = ThisRow - PosCenter
            SameDiff = ThisRow  - NegCenter
        SameClassDis += math.sqrt(SameDiff.multiply(SameDiff).sum())
        DiffClassDis += math.sqrt(DiffDiff.multiply(DiffDiff).sum())
        
    LossScore = SameClassDis / DiffClassDis
    
    logging.info('q[%d] loss [%f]',LabelMtx[0,1],LossScore)
    return LossScore


def Process(LabelInName,EmbInName,OutName):
    logging.info('start loading label mtx from [%s]',LabelInName)
    LabelMtx = LoadLabelMtx(LabelInName)
    logging.info('start loading representation mtx from [%s]',EmbInName)
    EmdMtx = LoadSparseMtx(EmbInName)
    
    logging.info('data loaded')
    out = open(OutName,'w')
    st = 0
    ed = 0
    MeanScore = 0
    QCnt = 0
    for i in range(LabelMtx.shape[0]):
        qid = LabelMtx[i,1]
        LossScore = -1
        
        if i < LabelMtx.shape[0] - 1:
            if LabelMtx[i+1,1] == qid:
                continue
        
        ed = i + 1
        logging.info('q [%s] data [%d-%d)',qid,st,ed)
        LossScore = ProcessOneQuery(LabelMtx[st:ed,:], EmdMtx[st:ed,:])
        st = ed
        QCnt += 1
        print >>out, '%s\t%.20f' %(qid,LossScore)
        MeanScore += LossScore
        logging.info('qid [%s] processed [%f] cluster loss',qid,LossScore)
    
    MeanScore /= float(QCnt)
    
    print >>out, 'mean\t%.20f' %(MeanScore)
    out.close()
    logging.info('finished')
    
    
    
import sys

if 4 != len(sys.argv):
    print "label in name + emd in name + out name"
    sys.exit()
    
root = logging.getLogger()
root.setLevel(logging.DEBUG)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)


Process(sys.argv[1], sys.argv[2], sys.argv[3])
        
            
            
            
            
    
    
    
            
    
            
    
    
    
    
    
    
    
    
    