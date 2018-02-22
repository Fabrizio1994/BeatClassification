import wfdb
from scipy import signal
import numpy as np

class FeatureExtraction:
    def extract_features(self, sample_name):
        print("Extracting features for signal " + sample_name + "...")
        record = wfdb.rdrecord(sample_name)
        #FILTER TO BOTH CHANNELS OR ONLY ONE?

        first_channel = []
        second_channel = []
        for elem in record.p_signal:
            first_channel.append(elem[0])
            second_channel.append(elem[1])

        filtered_first_channel = self.passband_filter(first_channel)
        filtered_second_channel = self.passband_filter(second_channel)

        #filtered_first_channel = self.func_filter(first_channel)
        #filtered_second_channel = self.func_filter(second_channel)

        #for i in range(len(record.p_signal)):
        #    record.p_signal[i][0] = filtered_first_channel[i]
        #    record.p_signal[i][1] = filtered_second_channel[i]
        gradient_channel1 = np.gradient(filtered_first_channel)
        gradient_channel2 = np.gradient(filtered_second_channel)

        for i in range(len(record.p_signal)):
            record.p_signal[i][0] = gradient_channel1[i]
            record.p_signal[i][1] = gradient_channel2[i]

        features = []
        labels = []

        annotation = wfdb.rdann(sample_name, 'atr')

        wfdb.plot_wfdb(record, annotation=annotation)


    def passband_filter(self, channel):
        freq = 360.0/2.0
        b, a = signal.butter(2, 12/freq, btype='lowpass')
        d, c = signal.butter(1, 5/freq, btype='highpass')

        #new_channel = signal.lfilter(d, c, signal.lfilter(b, a, channel))
        new_channel = signal.filtfilt(d, c, signal.filtfilt(b, a, channel))
        return new_channel


    def func_filter(self, channel):
        d = [-1, 32, 1]
        c = [1, 1]
        b = [1, -2, 1]
        a = [1, -2, 1]


        #new_channel = signal.filtfilt(b, a, signal.filtfilt(d, c, channel))
        new_channel = signal.lfilter(b, a, signal.lfilter(d, c, channel))
        return new_channel