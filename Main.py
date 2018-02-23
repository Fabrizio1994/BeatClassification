import wfdb
import numpy as np
from FeatureExtraction import FeatureExtraction

fe = FeatureExtraction()
NON_BEAT_ANN = [ '[', '!', ']', 'x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', '+', 's', 'T', '*', 'D', '='
    ,'"', '@']
fe.extract_features('sample/100')




