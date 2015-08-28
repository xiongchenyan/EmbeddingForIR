'''
Created on Aug 28, 2015 5:25:52 PM
@author: cx

what I do:
     average the annotator's label of LP50
what's my input:
    LP50's label
what's my output:
    doc id,doc id, sim score (avg)

'''


import sys
import numpy as np

if 3 != len(sys.argv):
    print '2 para: LP 50 annotation data + output'
    print 'I average them'
    sys.exit()
    
    
lLines = open(sys.argv[1]).read().splitlines()[1:]

lData = [line.split(',')[1:4] for line in lLines]

hData = {}

for a,b,score in lData:
    l = [int(a),int(b)]
    l.sort()
    key = '%d,%d'%(l[0],l[1])
    score = float(score)
    if not key in hData:
        hData[key] = [score]
    else:
        hData[key].append(score)
        
    
    
out = open(sys.argv[2],'w')

for key,l in hData.items():
    print >>out, key + ',%f'%(np.mean(l))
    
out.close()
print 'finished'
    