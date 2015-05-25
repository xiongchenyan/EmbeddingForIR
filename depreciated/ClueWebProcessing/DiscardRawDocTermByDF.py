'''
Created on Feb 19, 2015 7:02:22 PM
@author: cx

what I do:
discard < 5 df
what's my input:
clueweb boiler pipe + doc id in beginning
what's my output:
tf < 5 terms (except doc no) discarded

'''

import sys


def CoundDF(InName):
    hTerm = {}
    for line in open(InName):
        vCol = line.strip().split()
        if len(vCol) < 2:
            continue
        for term in vCol[1:]:
            if not term in hTerm:
                hTerm[term] = 1
            else:
                hTerm[term] += 1
    return hTerm


def Discard(InName,OutName,hTerm):
    out = open(OutName,'w')
    for line in open(InName):
        vCol = line.strip().split()
        if len(vCol) < 2:
            continue
        l = [vCol[0]]
        for col in vCol[1:]:
            if hTerm[col] < 5:
                continue
            l.append(col)
        print >>out,' '.join(l)
    out.close()
    
    
hTerm = CoundDF(sys.argv[1])
print "df get"
Discard(sys.argv[1], sys.argv[2], hTerm)
print "done"
