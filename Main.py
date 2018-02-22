import wfdb
import numpy as np
from FeatureExtraction import FeatureExtraction

fe = FeatureExtraction()
NON_BEAT_ANN = [ '[', '!', ']', 'x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', '+', 's', 'T', '*', 'D', '='
    ,'"', '@']



fe.extract_features('sample/100')
#wfdb.plot_wfdb(record, annotation=annotation)


'''
# CODE TO CLEAN SIGNAL FROM NON BEAT ANNOTATIONS
new_sample = []
new_symbol= []

j = 0

for j in range(len(samples)):
    if(symbols[j] not in NON_BEAT_ANN):
        new_sample.append(samples[j])
        new_symbol.append(symbols[j])

new_sample = np.asarray(new_sample)
new_symbol = np.asarray(new_symbol)'''

