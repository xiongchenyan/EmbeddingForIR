'''
Created on my MAC Aug 24, 2015-10:10:57 PM
What I do:

What's my input:
    I am the testing class of CTM
What's my output:
    to be called by CrossValidation
@author: chenyanxiong
'''



import site
import logging


site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')
site.addsitedir('/bos/usr0/cx/PyCode/EmbeddingForIR')

import sys

from CTMRanking.ContinuousLmRankingBase import ContinuousLmRankingBaseC

if 5 != len(sys.argv):
    print '4para: training input + testing input + parastr (cxConfFormat) + eva out'
    print 'para: name=value,xxx=xxx,etc'
    sys.exit()
    
    
root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

LmRanker = ContinuousLmRankingBaseC()
LmRanker.Process(sys.argv[2], sys.argv[3], sys.argv[4], WithRankingOut=True)

    
    


