import wfdb
import numpy as np

class Utility:

    NON_BEAT_ANN = [ '[', '!', ']', 'x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', '+', 's', 'T', '*', 'D', '='
        ,'"', '@']

    # CODE TO CLEAN SIGNAL FROM NON BEAT ANNOTATIONS
    def remove_non_beat(self, sample_name):
        annotation = wfdb.rdann(sample_name,"atr")
        new_sample = []
        new_symbol= []
        samples = annotation.sample
        symbols = annotation.symbol
        j = 0

        for j in range(len(samples)):
            if symbols[j] not in self.NON_BEAT_ANN:
                new_sample.append(samples[j])
                new_symbol.append(symbols[j])

        new_sample = np.asarray(new_sample)
        new_symbol = np.asarray(new_symbol)
        wfdb.wrann(sample_name.replace("sample/", ""),"atr", new_sample, new_symbol)
