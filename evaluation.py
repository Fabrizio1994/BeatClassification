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

    def eval_rr_intervals(self):

        category = {'PVC': ['V'],
                    'VF': ['[', '!', ']'],
                    'BII': ['BII'],
                    'N': ['N']}
        temp_values = []
        for cat in category.keys():
            for value in category[cat]:
                temp_values.append(value)
        '''non_beat_annotation = ['x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', 's', 'T', '*', 'D', '=', '"', '@',
                               "(AB\x00", "(AFIB\x00", "(AFL\x00", "(B\x00", "(IVR\x00", "(N\x00",
                                "(NOD\x00", "(P\x00", "(PREX\x00", "(SBR\x00", "(SVTA\x00", "(T\x00", "(VFL\x00",
                                "(VT\x00"]'''

        non_beat_annotation = ['x', '(', ')', 'p', 't', 'u', '`', '\'', '^', '|', '~', 's', 'T', '*', 'D', '=', '"',
                               '@']

        out_file = open('sensitivity.tsv', 'a')
        for patient in os.listdir('original_annotations'):
            results = []
            if patient.endswith('.atr'):
                patient = patient.replace('.atr', '')
                annotations = wfdb.rdann('original_annotations/' + patient, 'atr')
                symbols = annotations.symbol
                file = open('results/' + patient + '_results.tsv', 'r')
                for value in file:
                    results.append(value.replace('\n', ''))
                evaluation = self.initialize_map(category)
                for j in range(len(symbols)):
                    if symbols[j] == '+' and annotations.aux_note[j] == '(BII\x00':
                       symbols[j] = "BII"
                cleaned_symbols = list(filter(lambda x: x not in non_beat_annotation, symbols))
                for j in range(len(cleaned_symbols)):
                    if cleaned_symbols[j] not in temp_values:
                        cleaned_symbols[j] = 'N'
                end_index = len(cleaned_symbols) - 1
                cleaned_symbols = cleaned_symbols[2:end_index]
                evaluation = self.evaluate_prediction(category, cleaned_symbols, evaluation, results)

                out_file.write('|%s|' % patient)
                for categ in evaluation.keys():
                    if (evaluation[categ]['TP'] + evaluation[categ]['FN']) != 0:
                        se = evaluation[categ]['TP']/(evaluation[categ]['TP'] + evaluation[categ]['FN'])
                    else:
                        se = 0.0
                    out_file.write('%s|' % (str(se)))
                out_file.write('\n')

    def evaluate_prediction(self, category, cleaned_symbols, evaluation, results):
        for j in range(len(cleaned_symbols) - 1):
            label = cleaned_symbols[j]
            pred = results[j]
            if label in category[pred]:
                evaluation[pred]['TP'] += 1
            else:
                evaluation[pred]['FP'] += 1
                for categ in category.keys():
                    if label in category[categ]:
                        evaluation[categ]['FN'] += 1
        return evaluation



