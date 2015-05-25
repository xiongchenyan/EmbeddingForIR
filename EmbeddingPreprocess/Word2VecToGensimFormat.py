'''
Created on my MAC May 25, 2015-4:42:07 PM
What I do:
move the lines together
</s>
vec

=>
</s> vec
What's my input:
word2vec in
What's my output:
word2vec out,but gensim format
@author: chenyanxiong
'''

import sys

if 3 != len(sys.argv):
    print "word2vec raw in + out\nwill change the format to gensim likes"
    sys.exit()
    

out = open(sys.argv[2],'w')

cnt = 0
LastLine = ""
for line in open(sys.argv[1]):
    cnt += 1
    line = line.strip()
    if cnt == 1:
        print >> out,line
        continue
    
    if 1 == (cnt % 2):
        print >>out, LastLine + ' ' + line
    LastLine = line
    if 0 == cnt % 1000:
        print "processed [%d] line" %(cnt)
out.close()
print "finished"
        