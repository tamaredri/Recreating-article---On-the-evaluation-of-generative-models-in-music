import pandas as pd
import json

# ################ exp 2 #################### #

with open('../data/exp_1/measurments_results/Feature_extraction_results_section_4_1.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data = json.load(file)

"""
0 - abs mean 1
1 - abs std 1

2 - abs mean 2
3 - abs mean 2

4 - intra mean 1
5 - intra std 1

6 - intra mean 2
7 - intra std 2

8 - inter mean
9 - inter std
"""

# Reorder indices
reorder_indices = [4, 5, 0, 1, 6, 7, 2, 3, 8, 9]


# Function to reorder values and handle numpy arrays
def reorder_and_handle_numpy(values):
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


# Create a new dictionary with reordered values
reordered_data = {key: reorder_and_handle_numpy(values) for key, values in data.items()}

df_intra = pd.DataFrame([reordered_data["total_used_pitch"][:8],
                         reordered_data["bar_used_pitch"][:8],
                         reordered_data["total_used_note"][:8],
                         reordered_data["bar_used_note"][:8],
                         reordered_data["total_pitch_class_histogram"][:8],
                         reordered_data["bar_pitch_class_histogram"][:8],
                         reordered_data["pitch_class_transition_matrix"][:8],
                         reordered_data["pitch_range"][:8],
                         reordered_data["avg_pitch_shift"][:8],
                         reordered_data["avg_IOI"][:8],
                         reordered_data["note_length_hist"][:8],
                         reordered_data["note_length_transition_matrix"][:8]
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
                            [['Folk', 'Jazz'],
                             ['Intra-set', 'Absolute measures'],
                             ['mean', 'STD']],
                            names=['Genre:', 'Measurement type:', 'Statistics:']))

df_inter = pd.DataFrame([reordered_data["total_used_pitch"][8:],
                         reordered_data["bar_used_pitch"][8:],
                         reordered_data["total_used_note"][8:],
                         reordered_data["bar_used_note"][8:],
                         reordered_data["total_pitch_class_histogram"][8:],
                         reordered_data["bar_pitch_class_histogram"][8:],
                         reordered_data["pitch_class_transition_matrix"][8:],
                         reordered_data["pitch_range"][8:],
                         reordered_data["avg_pitch_shift"][8:],
                         reordered_data["avg_IOI"][8:],
                         reordered_data["note_length_hist"][8:],
                         reordered_data["note_length_transition_matrix"][8:]
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
                            [[' '],
                             ['Inter-set'],
                             ['mean', 'STD']],
                            names=['Genre:', 'Measurement type:', 'Statistics:']))

df_combined = pd.concat([df_intra, df_inter], axis=1)
print(df_combined)
df_combined.to_excel('../data/exp_2/measurments_results/Table3_section4.2.xlsx')
