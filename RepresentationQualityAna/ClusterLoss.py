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

import logging,json

def LoadSparseMtx(InName):
    lLines = open(InName).read().splitlines()
    
    lData = [line.split(',') for line in lLines]
    lData = [[int(item[0]) - 1,int(item[1]) - 1,float(item[2])] for item in lData]
    
    Mtx = np.array(lData)
    SmtxData = csc_matrix(Mtx[:,2],(Mtx[:,0],Mtx[:,1]))
    
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
    
    PosCenter /= float(PosCnt)
    NegCenter /= float(NegCnt)
    
    logging.info('q [%d] [%d] pos [%d] neg',LabelMtx[0,1],PosCenter,NegCenter)
    
    '''
    start calculate cluster loss
    '''        
    
    LossScore = 0
    for i in range(LabelMtx.shape[0]):
        ThisRow = ThisRepMtx.getrow(i)
        if LabelMtx[i,0] > 0:
            Diff = ThisRow - PosCenter
        else:
            Diff = ThisRow - NegCenter
        Diff = Diff.multiply(Diff)
        LossScore += Diff.sum()
        
    LossScore /= float(PosCnt + NegCnt)
    
    logging.info('q[%d] loss [%f]',LabelMtx[0,1],LossScore)
    return LossScore
    
            
    
            
    
    
    
    
    
    
    
    
    