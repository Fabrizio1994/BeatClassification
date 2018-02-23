import wfdb

class Utility:
    # CODE TO CLEAN SIGNAL FROM NON BEAT ANNOTATIONS
    def remove_non_beat(self):
        annotation = wfdb.rdann("sample/100","atr")
        new_sample = []
        new_symbol= []
        samples = annotation.sample
        symbols = annotation.symbol
        j = 0

        for j in range(len(samples)):
            if(symbols[j] not in NON_BEAT_ANN):
                new_sample.append(samples[j])
                new_symbol.append(symbols[j])

        new_sample = np.asarray(new_sample)
        new_symbol = np.asarray(new_symbol)
        wfdb.wrann("100","atr", new_sample, new_symbol)
