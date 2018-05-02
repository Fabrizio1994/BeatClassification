import numpy as np
import wfdb
import os
from evaluation import evaluation


class Main:

    def time2sample(self, time):
        return round(time * 360)

    def update_window(self, rr_intervals, index):
            RR1 = rr_intervals[index - 1]
            RR2 = rr_intervals[index]
            RR3 = rr_intervals[index + 1]
            return RR1, RR2, RR3

    def find_beat_annotation(self, peaks_file, patient):
        print(patient)
        const1 = 1.15
        const2 = 1.8
        const3 = 1.2
        rr_intervals = []
        current_index = 1
        prediction = []

        for rr_interval in peaks_file:
            rr_interval = rr_interval.replace('\n', '')
            rr_intervals.append(int(rr_interval))

        # INITIALIZATION
        while current_index < len(rr_intervals) - 1:
            RR1, RR2, RR3 = self.update_window(rr_intervals, current_index)
            # RULE 1
            cond1 = RR2 < self.time2sample(0.6)
            cond2 = const2 * RR2 < RR1
            if cond1 and cond2:
                vf_prediction = ['VF']
                vf_index = current_index + 1
                if vf_index < len(rr_intervals) - 1:
                    RR1, RR2, RR3 = self.update_window(rr_intervals, vf_index)
                    condition = self.vf_condition(RR1, RR2, RR3)
                    while condition and vf_index < len(rr_intervals) - 1:
                        vf_prediction.append('VF')
                        vf_index = vf_index + 1
                        RR1, RR2, RR3 = self.update_window(rr_intervals, vf_index)
                        condition = self.vf_condition(RR1, RR2, RR3)
                if len(vf_prediction) >= 4:
                    prediction.extend(vf_prediction)
                    current_index = vf_index
                    continue
                else:
                    # go back to current index
                    RR1, RR2, RR3 = self.update_window(rr_intervals, current_index)

            # RULE 2
            cond1 = const1 * RR2 < RR1
            cond2 = const1 * RR2 < RR3
            cond3 = abs(RR1 - RR2) < self.time2sample(0.3)
            cond4 = RR1 < self.time2sample(0.8)
            cond5 = RR2 < self.time2sample(0.8)
            cond6 = RR3 > const3 * np.mean([RR1, RR2])
            cond7 = abs(RR2 - RR3) < self.time2sample(0.3)
            cond8 = RR2 < self.time2sample(0.8)
            cond9 = RR3 < self.time2sample(0.8)
            cond10 = RR1 > const3 * np.mean([RR2, RR3])
            if (cond1 and cond2) or (cond3 and cond4 and cond5 and cond6) or (cond7 and cond8 and cond9 and cond10):
                prediction.append('PVC')
                current_index = current_index + 1
                continue

            # RULE 3
            cond1 = RR2 > self.time2sample(2.2)
            cond2 = RR2 < self.time2sample(3.0)
            cond3 = abs(RR1 - RR2) < self.time2sample(0.2)
            cond4 = abs(RR2 - RR3) < self.time2sample(0.2)

            if (cond1 and cond2) and (cond3 or cond4):
                prediction.append('BII')
            else:
                prediction.append('N')
            current_index = current_index + 1

        out_file = open('results/' + patient + '_results.tsv', 'w')
        for value in prediction:
            out_file.write(value + '\n')

    def vf_condition(self, RR1, RR2, RR3):
        cond1 = RR1 < self.time2sample(0.7)
        cond2 = RR2 < self.time2sample(0.7)
        cond3 = RR3 < self.time2sample(0.7)
        cond4 = RR1 + RR2 + RR3 < self.time2sample(1.7)
        return (cond1 and cond2 and cond3) or cond4

    def predict(self):
        for name in os.listdir("original_annotations"):
            if name.endswith(".atr"):
                patient = name.replace(".atr","")
                peaks_file = open("peaks/" + patient + "_peaks.tsv", "r")
                self.find_beat_annotation(peaks_file, patient)

    def write_peaks(self):
        ann_loc = "sample/mitdb/"
        peaks_loc = "peaks/"
        for name in os.listdir("original_annotations"):
            if name.endswith(".atr"):
                patient = name.replace(".atr","")
                file = open(peaks_loc + patient + "_peaks.tsv", "w")
                ann = wfdb.rdann(ann_loc + patient, "atr")
                peaks = np.diff(ann.sample)
                for p in peaks:
                    file.write("%s\n" % str(p))
                file.close()

if __name__ == '__main__':
  eval = evaluation()
  eval.eval_rr_intervals()