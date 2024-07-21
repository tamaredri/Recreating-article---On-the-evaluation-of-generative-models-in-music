import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json

# ################ exp 2 #################### #

# ------------------- Example data ---------------------
'''
np.random.seed(42)

data_magenta = {
    'Model': ['Magenta']*100,
    'PCH': np.random.normal(loc=62, scale=6, size=100),
    'PCTM': np.random.normal(loc=67, scale=8, size=100),
    'NLH': np.random.normal(loc=72, scale=11, size=100),
    'NLTM': np.random.normal(loc=77, scale=13, size=100)
}

data_midinet = {
    'Model': ['MidiNet'] * 100,
    'PCH': np.random.normal(loc=62, scale=6, size=100),
    'PCTM': np.random.normal(loc=67, scale=8, size=100),
    'NLH': np.random.normal(loc=72, scale=11, size=100),
    'NLTM': np.random.normal(loc=77, scale=13, size=100)
}
'''

# ------------------- Read json files ---------------------
with open('../data/exp_1/measurments_results/PDF_distances.json', 'r') as f:
    pdf_distance_output = json.load(f)


# ------------------- Get data ---------------------
data_magenta = {
    'Model': ['Magenta']*1000,
    'PCH': pdf_distance_output["set1"]["total_pitch_class_histogram"][0], # np.random.normal(loc=60, scale=5, size=100),
    'PCTM': pdf_distance_output["set1"]["pitch_class_transition_matrix"][0], # np.random.normal(loc=65, scale=7, size=100),
    'NLH': pdf_distance_output["set1"]["note_length_hist"][0], # np.random.normal(loc=70, scale=10, size=100),
    'NLTM': pdf_distance_output["set1"]["note_length_transition_matrix"][0] # np.random.normal(loc=75, scale=12, size=100)
}

data_midiNet = {
    'Model': ['MidiNet']*1000,
    'PCH': pdf_distance_output["set2"]["total_pitch_class_histogram"][0], # np.random.normal(loc=60, scale=5, size=100),
    'PCTM': pdf_distance_output["set2"]["pitch_class_transition_matrix"][0], # np.random.normal(loc=65, scale=7, size=100),
    'NLH': pdf_distance_output["set2"]["note_length_hist"][0], # np.random.normal(loc=70, scale=10, size=100),
    'NLTM': pdf_distance_output["set2"]["note_length_transition_matrix"][0] # np.random.normal(loc=75, scale=12, size=100)
}

# ------------------- Create fig4 ---------------------
df_magenta = pd.DataFrame(data_magenta)
df_midiNet = pd.DataFrame(data_midiNet)

df = pd.concat([df_magenta, df_midiNet])

palette = {'Magenta': '#5975A4', 'MidiNet': '#5F9E6E'}

plt.figure(figsize=(12, 8))
sns.violinplot(x='variable', y='value', hue='Model', data=pd.melt(df, id_vars='Model'), split=True, palette=palette)

for violin in plt.gca().collections:
    violin.set_edgecolor('none')

plt.title('Violin Plot of Intra-Set Distances for Magenta and MidiNet')
plt.xlabel('Features')
plt.ylabel('Distance')
plt.legend(title='Model', loc='upper right')
plt.savefig('../data/exp_2/measurments_results/Fig4.png')

