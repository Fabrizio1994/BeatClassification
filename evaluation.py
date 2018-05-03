import wfdb
import os

class evaluation:

    def initialize_map(self, category_map):
        evaluation = {}
        for symbol in category_map.keys():
            evaluation[symbol] = {}
            evaluation[symbol]['TP'] = 0
            evaluation[symbol]['FP'] = 0
            evaluation[symbol]['FN'] = 0
        evaluation['N'] = {}
        evaluation['N']['TP'] = 0
        evaluation['N']['FP'] = 0
        evaluation['N']['FN'] = 0
        return evaluation


    def clean_symbols(self, original_symbols, aux_symbols):
        cleaned_symbols = []
        non_beat_annotation = ['x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', 's', 'T', '*', 'D', '=', '"',
                               '@']
        original_symbols = list(filter(lambda x: x not in non_beat_annotation, original_symbols))
        for j in range(len(original_symbols)):
            if original_symbols[j] == '+' and aux_symbols[j] == '(BII\x00':
                cleaned_symbols.append('BII')
            if original_symbols[j] == '[':
                cleaned_symbols.append('VF')
            if original_symbols[j] == 'V':
                cleaned_symbols.append('PVC')
            if original_symbols[j] not in ['[', '!' ']', 'BII', 'V']:
                cleaned_symbols.append('N')
        return cleaned_symbols[2:len(cleaned_symbols)]

    def eval_rr_intervals(self):

        category = {'PVC': ['V'],
                    'VF': ['[', '!', ']'],
                    'BII': ['BII'],
                    'N': ['N']}
        sensitivity_file = open('sensitivity.tsv', 'a')
        precision_file = open('precision.tsv', 'a')
        sensitivity_file.write("|patient|")
        precision_file.write("|patient|")
        for cat in sorted(category.keys()):
            sensitivity_file.write("%s|" % cat)
            precision_file.write("%s|" % cat)
        sensitivity_file.write("\n")
        precision_file.write("\n")


        for patient in sorted(os.listdir('original_annotations')):
            predictions = []
            if patient.endswith('.atr'):
                patient = patient.replace('.atr', '')
                annotations = wfdb.rdann('original_annotations/' + patient, 'atr')
                file = open('results/' + patient + '_results.tsv', 'r')
                for value in file:
                    predictions.append(value.replace('\n', ''))
                evaluation = self.initialize_map(category)
                symbols = annotations.symbol
                aux_symbols = annotations.aux_note
                cleaned_symbols = self.clean_symbols(symbols, aux_symbols)
                end_index = len(cleaned_symbols) - 1
                cleaned_symbols = cleaned_symbols[2:end_index]
                print(patient)
                evaluation = self.evaluate_prediction(cleaned_symbols, evaluation, predictions)
                sensitivity_file.write('|%s|' % patient)
                precision_file.write('|%s|' % patient)
                for categ in sorted(evaluation.keys()):
                    tp = evaluation[categ]['TP']
                    fn = evaluation[categ]['FN']
                    fp = evaluation[categ]['FP']
                    if tp == 0 and fn == 0:
                        se = 'null'
                    else:
                        se = tp / (tp + fn)
                    if tp == 0 and fp == 0:
                        prec = 'null'
                    else:
                        prec = tp / (tp + fp)
                    if se != 'null':
                        se = round(se, 2)
                    if prec != 'null':
                        prec = round(prec, 2)
                    sensitivity_file.write('%s|' % str(se))
                    precision_file.write('%s|' % str(prec))
                sensitivity_file.write('\n')
                precision_file.write('\n')

    def evaluate_prediction(self, cleaned_symbols, evaluation, predictions):
        j = 0
        k = 0
        while j < (len(cleaned_symbols) - 1) and k < (len(predictions) - 1):
            label = cleaned_symbols[j]
            pred = predictions[k]
            if label == pred:
                evaluation[pred]['TP'] += 1
                j += 1
                k += 1
            else:
                if pred == 'BII':
                    evaluation[pred]['FP'] += 1
                    k += 1
                elif label == 'BII':
                    evaluation[label]['FN'] += 1
                    j += 1
                else:
                    evaluation[pred]['FP'] += 1
                    evaluation[label]['FN'] += 1
                    j += 1
                    k += 1
        return evaluation



