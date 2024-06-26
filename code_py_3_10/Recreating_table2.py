import pandas as pd
import numpy as np

import json

with open('../data/exp_1/measurments_results/Feature_extraction_results.json', 'r') as file:
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
"""

# Reorder indices
reorder_indices = [4, 5, 0, 1, 6, 7, 2, 3]


# Function to reorder values and handle numpy arrays
def reorder_and_handle_numpy(values):
    reordered_values = []
    for i in reorder_indices:
        value = values[i]
        if isinstance(value, list):
            value = np.array(value)
        if isinstance(value, np.ndarray):
            reordered_values.append(np.mean(value))
        else:
            reordered_values.append(value)
    return reordered_values


# Create a new dictionary with reordered values
reordered_data = {key: reorder_and_handle_numpy(values) for key, values in data.items()}

df = pd.DataFrame([reordered_data["total_used_pitch"],
                   reordered_data["bar_used_pitch"],
                   reordered_data["total_used_note"],
                   reordered_data["bar_used_note"],
                   reordered_data["total_pitch_class_histogram"],
                   reordered_data["bar_pitch_class_histogram"],
                   reordered_data["pitch_class_transition_matrix"],
                   reordered_data["pitch_range"],
                   reordered_data["avg_pitch_shift"],
                   reordered_data["avg_IOI"],
                   reordered_data["note_length_hist"],
                   reordered_data["note_length_transition_matrix"]
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
print(df)
df.to_excel('../data/exp_1/measurments_results/Table2_section4.1.xlsx')
