'''
Created on Aug 28, 2015 1:40:55 PM
@author: cx

what I do:

what's my input:

what's my output:


'''
"""
Demo of the histogram (hist) function with a few features.

In addition to the basic histogram, this demo shows a few optional features:

    * Setting the number of data bins
    * The ``normed`` flag, which normalizes bin heights so that the integral of
      the histogram is 1. The resulting histogram is a probability density.
    * Setting the face color of the bars
    * Setting the opacity (alpha value).

"""
import numpy as np
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt
import pickle
import logging


def ReadAndPlot(self,BinInName,OutPre):
    lBinData = pickle.load(open(BinInName))
    
    dim = 0
    for mu,sigma,hist,bins in lBinData:
#         y = mlab.normpdf(bins, mu, sigma)
        center = (bins[:-1] + bins[1:]) / 2
        plt.bar(center,hist,align='center',width=0.7 * (bins[1] - bins[0]))
#         plt.plot(bins, y, 'r--')
        plt.xlabel('embedding value dim %d',dim)
        plt.ylabel('Probability')
        plt.title(r'Histogram of Dim %d: $\mu=%f$, $\sigma=%f$',dim,mu,sigma)
        
        # Tweak spacing to prevent clipping of ylabel
        plt.subplots_adjust(left=0.15)   
        OutName = OutPre + '_%d'%(dim)
        plt.savefig(OutName,format='pdf',dpi=1000)
        logging.info('dim [%d] saved [%s]',OutName)
        dim += 1
        
    logging.info('plotted')
    return True


    
import sys
if 3 != len(sys.argv):
    print 'bin data in + out dir'
    sys.exit()
    
root = logging.getLogger()
root.setLevel(logging.INFO)

ch = logging.StreamHandler(sys.stdout)
#     ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
root.addHandler(ch)

ReadAndPlot(sys.argv[1], sys.argv[2])