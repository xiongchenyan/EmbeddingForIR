'''
Created on Feb 22, 2015 1:44:30 PM
@author: cx

what I do:
sample doc with given sample rate
but keep all target documents
what's my input:
CW doc train data
SVMData of LeToR for target docno's
sample rate
what's my output:
a sampled document collection
'''


import sys
import random


def LoadTargetDocNo(SVMInName):
    hDocNo = {}
    for line in open(SVMInName):
        key = line.strip().split('#')[-1].strip()
        hDocNo[key] = 1
        
    return hDocNo


def KeepDocLine(line,hDocNo,SampleRate = 0.1):
    key = line.split()[0]
    if not 'clueweb' in key:
        return True
    
    if key in hDocNo:
        print key + ' in target set'
        return True
    
    if random.random() < SampleRate:
        return True
    return False


def Process(InName,OutName,SVMInName,SampleRate = 0.1):
    out = open(OutName,'w')
    hDocNo = LoadTargetDocNo(SVMInName)
    cnt = 0
    for line in open(InName):
        line = line.strip()
        if KeepDocLine(line, hDocNo, SampleRate):
            print >>out, line
            cnt += 1
            if 0 == (cnt % 1000):
                print "kept [%d] lines" %(cnt)
                
    out.close()
    print "finished [%d] line rest" %(cnt)
    
    
if 5 != len(sys.argv):
    print "In + out + svm in + sample rate"
    print "to sample with fixed target docno's"
    sys.exit()
    
SampleRate = float(sys.argv[4])
Process(sys.argv[1],sys.argv[2],sys.argv[3],SampleRate)


    
    
    
    