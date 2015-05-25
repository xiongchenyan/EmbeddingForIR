'''
Created on Feb 21, 2015 1:25:02 PM
@author: cx

what I do:
I fetch the useful embeddings from trained doc vectors
what's my input:
SVMData (contains doc no)
what's my output:
Q's vector + Doc's vector (in one file)


'''


import sys

def ReadTargetDocNo(SVMInName):
    hDocNo = {}
    for line in open(SVMInName):
        line = line.strip()
        DocNo = line.split('#')[-1]
        DocNo = DocNo.strip()
        hDocNo[DocNo] = 1
    return hDocNo


def Process(InName,OutName,hDocNo):
    out = open(OutName,'w')
    cnt = 0
    for line in open(InName):
        line = line.strip()
        key = line.split()[0]
        cnt += 1
        if 0 == (cnt % 1000):
            print "process [%d] lines"  %(cnt)
        if 'TrecWebTrack' == key[:12]:
            print >> out, line
            continue
        if key in hDocNo:
            print >>out, line
    
    out.close()
    
    
    
if 4 != len(sys.argv):
    print "SVMDataIn + DocVecIn + out"
    sys.exit()
    
    
hDocNo = ReadTargetDocNo(sys.argv[1])

Process(sys.argv[2], sys.argv[3], hDocNo)

print "finished"
            
        
        
