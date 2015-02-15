'''
Created on Feb 13, 2015 5:07:34 PM
@author: cx

what I do:
I made 
    query id(desp, subtopic-id) word word
data from trec web track query topics 
what's my input:
query original xml topics from trec
what's my output:
    qid|qid-desp|qid-st-id  word word
for each line

'''
import site
site.addsitedir('/bos/usr0/cx/PyCode/cxPyLib')

from cxBase.TextBase import TextBaseC
import xml.etree.ElementTree as ET
import sys


def ParseOneQueryNode(QueryNode):
    '''
    tbd:
        get query id, query, desp and sub topic + st id
    '''
    Qid = QueryNode.attrib['number']
    Query = ""
    lSt = []
    Desp = ""
    for subnode in QueryNode:
        if subnode.tag == 'query':
            Query = TextBaseC.RawClean(subnode.text.strip())
        if subnode.tag =='description':
            Desp = TextBaseC.RawClean(subnode.text.strip())
        if subnode.tag == 'subtopic':
            lSt.append(TextBaseC.RawClean(subnode.text.strip()))
    lLines = []
    lLines.append(Qid + ' ' + Query)
    lLines.append(Qid + '_desp' + ' ' + Desp)
    for i in range(len(lSt)):
        lLines.append(Qid + '_st_%d' %(i) + ' ' + lSt[i])
    return lLines

if 3 != len(sys.argv):
    print 'xml query in + output'
    sys.exit()
    
tree = ET.parse(sys.argv[1])
root = tree.getroot()

out = open(sys.argv[2],'w')
for QueryNode in root:
    lLines = ParseOneQueryNode(QueryNode)
    print >> out,'\n'.join(lLines)
    
out.close()


