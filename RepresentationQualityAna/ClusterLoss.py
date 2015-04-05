'''
Created on Apr 3, 2015 7:34:52 PM
@author: cx

what I do:
    read the matrix format
        label input:
            col1: relevance label
            col -1: qid
        representation input:
            each line is a doc's features
            or sparse input: doc id, f id, score    
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
