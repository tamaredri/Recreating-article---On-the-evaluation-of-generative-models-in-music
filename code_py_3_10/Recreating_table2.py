import pandas as pd
import numpy as np

import json

with open('../data/exp_1/measurments_results/results.json', 'r') as file:
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

"""

PC = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

PC_Bar = [data['bar_used_pitch'][4], data['bar_used_pitch'][5], data['bar_used_pitch'][0], data['bar_used_pitch'][1],
      data['bar_used_pitch'][6], data['bar_used_pitch'][7], data['bar_used_pitch'][2], data['bar_used_pitch'][3]]

NC = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

NC_Bar = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

PCH = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

PCH_Bar = [data['bar_pitch_class_histogram'][4], data['bar_pitch_class_histogram'][5], data['bar_pitch_class_histogram'][0], data['bar_pitch_class_histogram'][1],
      data['bar_pitch_class_histogram'][6], data['bar_pitch_class_histogram'][7], data['bar_pitch_class_histogram'][2], data['bar_pitch_class_histogram'][3]]

PCTM = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

PR = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

PI = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

IOI = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

NLH = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]

NLT = [data["total_used_pitch"][4], data["total_used_pitch"][5], data["total_used_pitch"][0], data["total_used_pitch"][1],
      data["total_used_pitch"][6], data["total_used_pitch"][7], data["total_used_pitch"][2], data["total_used_pitch"][3]]
"""

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
