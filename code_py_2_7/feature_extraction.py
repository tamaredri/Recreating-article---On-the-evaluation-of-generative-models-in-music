
#  pip install pretty_midi=0.2.8 scikit-learn python-midi=0.2.4 music21

import json
from argparse import ArgumentParser
import glob
import copy
import os
import numpy as np
from pprint import pprint
import core, utils
from sklearn.model_selection import LeaveOneOut


parser = ArgumentParser()
parser.add_argument('--set1dir', required=True, type=str,
                    help='Path (absolute) to the first dataset (folder)')
parser.add_argument('--set2dir', required=True, type=str,
                    help='Path (absolute) to the second dataset (folder)')
parser.add_argument('--outfile', required=True, type=str,
                    help='File (pickle) where the analysis will be stored')

parser.add_argument('--num-bar', required=False, type=int, default=None,
                    help='Number of bars to account for during processing')

args = parser.parse_args()

set1 = glob.glob(os.path.join(args.set1dir, '*'))
set2 = glob.glob(os.path.join(args.set2dir, '*'))

print('Evaluation sets (sample and baseline):')
print(set1)
print(set2)

if not any(set1):
    print("Error: sample set it empty")
    exit()

if not any(set2):
    print("Error: baseline set it empty")
    exit()

# Initialize Evaluation Set
num_samples = min(len(set2), len(set1))

print(num_samples)
evalset = {
    'total_used_pitch': np.zeros((num_samples, 1))                            # PC
    , 'pitch_range': np.zeros((num_samples, 1))                               # PR
    , 'avg_pitch_shift': np.zeros((num_samples, 1))                           # PI
    , 'avg_IOI': np.zeros((num_samples, 1))                                   # IOI
    , 'total_used_note': np.zeros((num_samples, 1))                           # NC
    , 'bar_used_pitch': np.zeros((num_samples, args.num_bar, 1))
    , 'bar_used_note': np.zeros((num_samples, args.num_bar, 1))
    , 'total_pitch_class_histogram': np.zeros((num_samples, 12))              # PCH
    , 'bar_pitch_class_histogram': np.zeros((num_samples, args.num_bar, 12))
    , 'note_length_hist': np.zeros((num_samples, 12))                         # NLH
    , 'pitch_class_transition_matrix': np.zeros((num_samples, 12, 12))        # PCTM
    , 'note_length_transition_matrix': np.zeros((num_samples, 12, 12))        # NLTM
}

bar_metrics = ['bar_used_pitch', 'bar_used_note', 'bar_pitch_class_histogram']

for metric in bar_metrics:
    print(args.num_bar)
    if not args.num_bar:
        evalset.pop(metric)

# print(evalset)

metrics_list = evalset.keys()

single_arg_metrics = (
    ['total_used_pitch'
        , 'avg_IOI'
        , 'total_pitch_class_histogram'
        , 'pitch_range'
        # , 'total_used_note'
     ])

set1_eval = copy.deepcopy(evalset)
set2_eval = copy.deepcopy(evalset)

sets = [(set1, set1_eval), (set2, set2_eval)]

# Extract Fetures
for _set, _set_eval in sets:
    for i in range(0, num_samples):
        feature = core.extract_feature(_set[i])
        for metric in metrics_list:
            print(metric)
            evaluator = getattr(core.metrics(), metric)
            if metric in single_arg_metrics:
                tmp = evaluator(feature)
            elif metric in bar_metrics:
                # print(metric)
                tmp = evaluator(feature, 0, args.num_bar)
                # print(tmp.shape)
            else:
                tmp = evaluator(feature, 0)
            _set_eval[metric][i] = tmp

loo = LeaveOneOut()
loo.get_n_splits(np.arange(num_samples))
set1_intra = np.zeros((num_samples, len(metrics_list), num_samples - 1))    # 19 x 12 x 18
set2_intra = np.zeros((num_samples, len(metrics_list), num_samples - 1))

# Calculate Intra-set Metrics
for i, metric in enumerate(metrics_list):
    for train_index, test_index in loo.split(np.arange(num_samples)):
        set1_intra[test_index[0]][i] = utils.c_dist(
            set1_eval[metrics_list[i]][test_index], set1_eval[metrics_list[i]][train_index])
        set2_intra[test_index[0]][i] = utils.c_dist(
            set2_eval[metrics_list[i]][test_index], set2_eval[metrics_list[i]][train_index])

loo = LeaveOneOut()
loo.get_n_splits(np.arange(num_samples))
sets_inter = np.zeros((num_samples, len(metrics_list), num_samples))

# Calculate Inter-set Metrics
for i, metric in enumerate(metrics_list):
    for _, test_index in loo.split(np.arange(num_samples)):
        sets_inter[test_index[0]][i] = utils.c_dist(set1_eval[metric][test_index], set2_eval[metric])

plot_set1_intra = np.transpose(
    set1_intra, (1, 0, 2)).reshape(len(metrics_list), -1)
plot_set2_intra = np.transpose(
    set2_intra, (1, 0, 2)).reshape(len(metrics_list), -1)
plot_sets_inter = np.transpose(
    sets_inter, (1, 0, 2)).reshape(len(metrics_list), -1)

output = {}
pdf_distance_output = {
    'set1': {metric: [] for metric in metrics_list},
    'set2': {metric: [] for metric in metrics_list},
    'sets': {metric: [] for metric in metrics_list}
}


output = {}
for i, metric in enumerate(metrics_list):
    print('calculating kl of: {}'.format(metric))

    mean1 = np.mean(set1_eval[metric], axis=0).tolist()
    std1 = np.std(set1_eval[metric], axis=0).tolist()

    mean2 = np.mean(set2_eval[metric], axis=0).tolist()
    std2 = np.std(set2_eval[metric], axis=0).tolist()

    mean_intra1, std_intra1 = utils.pdf_mean_std(plot_set1_intra[i])
    mean_intra2, std_intra2 = utils.pdf_mean_std(plot_set2_intra[i])
    mean_sets_inter, std_sets_inter = utils.pdf_mean_std(plot_sets_inter[i])

    print(metric)
    pprint(plot_set1_intra[i])
    pprint(plot_set2_intra[i])
    pprint(plot_sets_inter[i])

    kl1 = utils.kl_dist(plot_set1_intra[i], plot_sets_inter[i])
    ol1 = utils.overlap_area(plot_set1_intra[i], plot_sets_inter[i])
    kl2 = utils.kl_dist(plot_set2_intra[i], plot_sets_inter[i])
    ol2 = utils.overlap_area(plot_set2_intra[i], plot_sets_inter[i])

    # The PDF of the intra-set distances
    intra_set1_pdf_val, intra_set1_pdf_samples = utils.intra_set_pdf(plot_set1_intra[i])
    intra_set2_pdf_val, intra_set2_pdf_samples = utils.intra_set_pdf(plot_set2_intra[i])
    inter_sets_pdf_val, inter_sets_pdf_samples = utils.intra_set_pdf(plot_sets_inter[i])

    pdf_distance_output["set1"][metric] = [intra_set1_pdf_val.tolist(), intra_set1_pdf_samples.tolist()]
    pdf_distance_output["set2"][metric] = [intra_set2_pdf_val.tolist(), intra_set2_pdf_samples.tolist()]
    pdf_distance_output["sets"][metric] = [inter_sets_pdf_val.tolist(), inter_sets_pdf_samples.tolist()]

    print(kl1)
    print(kl2)
    output[metric] = [mean1, std1, mean2, std2,
                      mean_intra1, std_intra1, mean_intra2, std_intra2,
                      mean_sets_inter, std_sets_inter,
                      kl1, ol1, kl2, ol2]

    '''if metric == 'pitch_class_transition_matrix':
        output[metric].append([])
        for tune in set2_eval[metric]:
            output[metric][14].append(tune.tolist())'''


# Save output
if os.path.exists(args.outfile):
    os.remove(args.outfile)

output_file = open(args.outfile, 'w')
json.dump(output, output_file, indent=4)
output_file.close()

with open('../data/exp_1/measurments_results/PDF_distances.json', 'w') as json_file:
    json.dump(pdf_distance_output, json_file, indent=4)

print('Saved output to file: ' + args.outfile)
