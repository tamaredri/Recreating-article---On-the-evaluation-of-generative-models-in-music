import pandas as pd
import json

# ################ exp 3 #################### #

# ------------------- Read json files ---------------------
with open('../data/exp_1/measurments_results/Feature_extraction_results_section_4_1.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data_midi1 = json.load(file)

with open('../data/exp_1/measurments_results/Feature_extraction_results_section_4_1.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data_midi2 = json.load(file)

# ------------------- Reorder indices ---------------------
"""
[
0 - mean train, 
1 - std train, 
2 - mean midiNet, 
3 - std midiNet,
4 - mean_intra train, 
5 - std_intra train, 
6 - mean_intra midiNet, 
7 - std_intra midiNet,
8 - mean_sets_inter, 
9 - std_sets_inter,
10 - kl train, 
11 - ol train, 
12 - kl midiNet, 
13 - ol midiNet]

# dataMidi1
0 - (6) - mean_intra midiNet1
1 - (7) - std_intra midiNet1,

2 - (12) - kl midiNet1,
3 - (13) - ol midiNet1

---------
# dataMidi2
0 - (6) - mean_intra midiNe
1 - (7) - std_intra midiNet

2 - (12) - kl midiNet2
3 - (13) - ol midiNet2


----
# dataMidi1 == # dataMidi2
0 -  (4) - mean_intra train
1 -  (5) - std_intra train
 
"""
reorder_indices_midi = [6, 7, 12, 13]
reorder_indices_train = [4, 5]


# Function to reorder values and handle numpy arrays
def reorder_and_handle_numpy(values, reorder_indices):
    reordered_values = []
    for i in reorder_indices:
        value = values[i]
        if isinstance(value, list) and len(value) == 1:
            reordered_values.append(value[0])
        elif isinstance(value, list):
            reordered_values.append('-')
        else:
            reordered_values.append(value)
    return reordered_values


# ------------------- Create a new dictionary with reordered values ---------------------
reordered_data_midi1 = {key: reorder_and_handle_numpy(values, reorder_indices_midi) for key, values in
                        data_midi1.items()}
reordered_data_midi2 = {key: reorder_and_handle_numpy(values, reorder_indices_midi) for key, values in
                        data_midi2.items()}
reordered_data_train = {key: reorder_and_handle_numpy(values, reorder_indices_train) for key, values in
                        data_midi2.items()}


# ------------------- Create table4 ---------------------
df_midi = pd.DataFrame([reordered_data_midi1["total_used_pitch"] + reordered_data_midi2["total_used_pitch"],
                        reordered_data_midi1["bar_used_pitch"] + reordered_data_midi2["bar_used_pitch"],
                        reordered_data_midi1["total_used_note"] + reordered_data_midi2["total_used_note"],
                        reordered_data_midi1["bar_used_note"] + reordered_data_midi2["bar_used_note"],
                        reordered_data_midi1["total_pitch_class_histogram"] + reordered_data_midi2[
                            "total_pitch_class_histogram"],
                        reordered_data_midi1["bar_pitch_class_histogram"] + reordered_data_midi2[
                            "bar_pitch_class_histogram"],
                        reordered_data_midi1["pitch_class_transition_matrix"] + reordered_data_midi2[
                            "pitch_class_transition_matrix"],
                        reordered_data_midi1["pitch_range"] + reordered_data_midi2["pitch_range"],
                        reordered_data_midi1["avg_pitch_shift"] + reordered_data_midi2["avg_pitch_shift"],
                        reordered_data_midi1["avg_IOI"] + reordered_data_midi2["avg_IOI"],
                        reordered_data_midi1["note_length_hist"] + reordered_data_midi2["note_length_hist"],
                        reordered_data_midi1["note_length_transition_matrix"] + reordered_data_midi2[
                            "note_length_transition_matrix"]
                        ],
                       index=pd.Index(['PC',
                                       'PC/Bar',
                                       'NC',
                                       'NC/Bar',
                                       'PCH',
                                       'PCH/Bar',
                                       'PCTM',
                                       'PR',
                                       'PI',
                                       'IOI',
                                       'NLH',
                                       'NLTM'],
                                      name='Metrics:'),
                       columns=pd.MultiIndex.from_product(
                           [['MidiNet 1', 'MidiNet 2'],
                            ['Intra-set', 'Inter-set'],
                            ['mean', 'STD']],
                           names=['Genre:', 'Measurement type:', 'Statistics:']))

df_training = pd.DataFrame([reordered_data_train["total_used_pitch"],
                            reordered_data_train["bar_used_pitch"],
                            reordered_data_train["total_used_note"],
                            reordered_data_train["bar_used_note"],
                            reordered_data_train["total_pitch_class_histogram"],
                            reordered_data_train["bar_pitch_class_histogram"],
                            reordered_data_train["pitch_class_transition_matrix"],
                            reordered_data_train["pitch_range"],
                            reordered_data_train["avg_pitch_shift"],
                            reordered_data_train["avg_IOI"],
                            reordered_data_train["note_length_hist"],
                            reordered_data_train["note_length_transition_matrix"]
                            ],
                           index=pd.Index(['PC',
                                           'PC/Bar',
                                           'NC',
                                           'NC/Bar',
                                           'PCH',
                                           'PCH/Bar',
                                           'PCTM',
                                           'PR',
                                           'PI',
                                           'IOI',
                                           'NLH',
                                           'NLTM'],
                                          name='Metrics:'),
                           columns=pd.MultiIndex.from_product(
                               [['Training data'],
                                ['Intra-set'],
                                ['mean', 'STD']],
                               names=['model:', 'Measurement type:', 'Statistics:']))

df_combined = pd.concat([df_training, df_midi], axis=1)
print(df_combined)
df_combined.to_excel('../data/exp_3/measurments_results/Table4_section4.3.xlsx')
