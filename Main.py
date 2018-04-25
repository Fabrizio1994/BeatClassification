import numpy as np
from evaluation import evaluation

'''for signal_name in os.listdir('sample/mitdb'):
    if signal_name.endswith('.atr'):
        cleaned_name = signal_name.replace('.atr', '')
        annotation = wfdb.rdann('sample/mitdb/' + cleaned_name, 'atr')
        peaks = annotation.sample
        peaks = np.diff(peaks)
        file = open(cleaned_name + '_peaks.tsv', 'a')
        for peak in peaks:
            file.write('%s\n' % (str(peak)))'''


class Main:

    def time2sample(self, time):
        return round(time * 360)

    def update_window(self, window, rr_intervals, index):
        if index < len(rr_intervals) - 1:
            window[0] = rr_intervals[index - 1]
            window[1] = rr_intervals[index]
            window[2] = rr_intervals[index + 1]

    def find_beat_annotation(self, file, patient):
        const1 = 1.15
        const2 = 1.8
        const3 = 1.2
        rr_intervals = []
        starting_index = 1
        temp_index = 0
        current_index = starting_index
        window = [0] * 3
        prediction = []

        for rr_interval in file:
            rr_interval = rr_interval.replace('\n', '')
            rr_intervals.append(rr_interval)

        # INITIALIZATION
        self.update_window(window, rr_intervals, starting_index)
        while current_index < len(rr_intervals) - 1: #Excluding two beats at the end

            # RULE 1
            cond1 = int(window[1]) < self.time2sample(0.6)
            cond2 = const2 * int(window[1]) < int(window[0])
            if cond1 and cond2:
                temp_prediction = ['VF']
                self.update_window(window, rr_intervals, current_index + 1)
                cond1 = int(window[0]) < self.time2sample(0.7)
                cond2 = int(window[1]) < self.time2sample(0.7)
                cond3 = int(window[2]) < self.time2sample(0.7)
                cond4 = int(window[0]) + int(window[1]) + int(window[2]) < self.time2sample(1.7)
                while ((cond1 and cond2 and cond3) or cond4) and (temp_index < len(rr_intervals) - 1):
                    if temp_index <= current_index:
                        temp_index = current_index + 1
                    else:
                        temp_index = temp_index + 1
                    self.update_window(window, rr_intervals, temp_index)
                    cond1 = int(window[0]) < self.time2sample(0.7)
                    cond2 = int(window[1]) < self.time2sample(0.7)
                    cond3 = int(window[2]) < self.time2sample(0.7)
                    cond4 = int(window[0]) + int(window[1]) + int(window[2]) < self.time2sample(1.7)
                    temp_prediction.append('VF')

                if len(temp_prediction) < 4:
                    self.update_window(window, rr_intervals, current_index)
                else:
                    prediction.extend(temp_prediction)
                    current_index = current_index + 1
                    self.update_window(window, rr_intervals, current_index)


            # RULE 2
            cond1 = const1 * int(window[1]) < int(window[0])
            cond2 = const1 * int(window[1]) < int(window[2])
            cond3 = abs(int(window[0]) - int(window[1])) < self.time2sample(0.3)
            cond4 = int(window[0]) < self.time2sample(0.8)
            cond5 = int(window[1]) < self.time2sample(0.8)
            cond6 = int(window[2]) > const3 * np.mean([int(window[0]), int(window[1])])
            cond7 = abs(int(window[1]) - int(window[2])) < self.time2sample(0.3)
            cond8 = int(window[1]) < self.time2sample(0.8)
            cond9 = int(window[2]) < self.time2sample(0.8)
            cond10 = int(window[0]) > const3 * np.mean([int(window[1]), int(window[2])])
            if (cond1 and cond2) or (cond3 and cond4 and cond5 and cond6) or (cond7 and cond8 and cond9 and cond10):
                prediction.append('PVC')
                current_index = current_index + 1
                self.update_window(window, rr_intervals, current_index)
                continue

            # RULE 3
            cond1 = int(window[1]) > self.time2sample(2.2)
            cond2 = int(window[1]) < self.time2sample(3.0)
            cond3 = abs(int(window[0]) - int(window[1])) < self.time2sample(0.2)
            cond4 = abs(int(window[1]) - int(window[2])) < self.time2sample(0.2)

            if (cond1 and cond2) and (cond3 or cond4):
                prediction.append('BII')
                current_index = current_index + 1
                self.update_window(window, rr_intervals, current_index)
                continue

            else:
                prediction.append('N')
                current_index = current_index + 1
                self.update_window(window, rr_intervals, current_index)

        out_file = open('results/' + patient + '_results.tsv', 'w')
        for value in prediction:
            out_file.write(value + '\n')






if __name__ == '__main__':
    eval = evaluation()
    eval.eval_rr_intervals()
