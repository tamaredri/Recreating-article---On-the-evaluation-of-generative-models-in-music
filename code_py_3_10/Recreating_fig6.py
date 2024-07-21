import matplotlib.pyplot as plt
import json

# ################ exp 3 #################### #

# ------------------- Example data ---------------------
'''midinet1_intra_set = np.random.normal(loc=0, scale=1, size=1000)
midinet1_inter_set = np.random.normal(loc=1, scale=1.5, size=1000)
midinet2_intra_set = np.random.normal(loc=0.2, scale=1, size=1000)
midinet2_inter_set = np.random.normal(loc=1.2, scale=1.5, size=1000)
training_data_intra_set = np.random.normal(loc=0, scale=1, size=1000)

data = {
    'Training Data intra': training_data_intra_set,
    'MidiNet1 intra': midinet1_intra_set,
    'MidiNet1 inter': midinet1_inter_set,
    'MidiNet2 intra': midinet2_intra_set,
    'MidiNet2 inter': midinet2_inter_set,
}
'''

# ------------------- Read json files ---------------------
with open('../data/exp_1/measurments_results/PDF_distances.json', 'r') as f:
    pdf_distance_midi1 = json.load(f)

with open('../data/exp_1/measurments_results/PDF_distances.json', 'r') as f:
    pdf_distance_midi2 = json.load(f)

# ------------------- Get data ---------------------
'''
pdf_distance_midi1 = [
set1: training_data_intra_set
set2: midinet1_intra_set
sets: midinet1_inter_set
]

pdf_distance_mid2 = [
set1: training_data_intra_set
set2: midinet2_intra_set
sets: midinet2_inter_set
]
'''
data = {
    'Training Data intra': pdf_distance_midi1["set1"]["bar_pitch_class_histogram"],
    'MidiNet1 intra': pdf_distance_midi1["set2"]["bar_pitch_class_histogram"],
    'MidiNet1 inter': pdf_distance_midi1["sets"]["bar_pitch_class_histogram"],
    'MidiNet2 intra': pdf_distance_midi2["set2"]["bar_pitch_class_histogram"],
    'MidiNet2 inter': pdf_distance_midi2["sets"]["bar_pitch_class_histogram"]
}

# ------------------- Create fig6 ---------------------
colors = {
    'Training Data intra': '#C7575A',
    'MidiNet1 intra': '#3D66A9',
    'MidiNet1 inter': '#3D66A9',
    'MidiNet2 intra': '#45A05A',
    'MidiNet2 inter': '#45A05A'
}
line_styles = {
    'Training Data intra': '-',
    'MidiNet1 intra': '--',
    'MidiNet1 inter': '-',
    'MidiNet2 intra': '--',
    'MidiNet2 inter': '-'
}

plt.figure(figsize=(12, 8))

for label, dist in data.items():
    density = dist[0]
    x = dist[1]
    plt.plot(x, density, label=label, color=colors[label], linestyle=line_styles[label])

plt.xlabel('Euclidean Distance')
plt.ylabel('Density')
plt.title('Pitch class histogram per bar')
plt.legend()
plt.savefig('../data/exp_3/measurments_results/Fig6.png')
