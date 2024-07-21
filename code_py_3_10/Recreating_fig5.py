import json
import matplotlib.pyplot as plt

# ################ exp 3 #################### #

'''
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
12 - kl midiNet1,
13 - ol midiNet1

---------
# dataMidi2
12 - kl midiNet2
13 - ol midiNet2
----
'''

# ------------------- Read json files ---------------------
with open('../data/exp_3/measurments_results/Feature_extraction_results1.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data_midi1 = json.load(file)

with open('../data/exp_3/measurments_results/Feature_extraction_results2.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data_midi2 = json.load(file)

# ------------------- Get kl&ol midiNet1 and lk&ol midiNet2 ---------------------
kl_index = 12
ol_index = 13
midiNet1_kld = [values[kl_index] for _, values in data_midi1.items()] # [2.1, 1.8, 2.5, 3.0, 2.7, 2.3, 2.1, 1.8, 2.0, 2.5, 3.2, 2.9]  # KLD values for MidiNet 1
midiNet1_oa = [values[ol_index] for _, values in data_midi1.items()] # [0.65, 0.72, 0.68, 0.60, 0.62, 0.70, 0.68, 0.65, 0.72, 0.75, 0.68, 0.70]  # OA values for MidiNet 1

midiNet2_kld = [values[kl_index] for _, values in data_midi2.items()] # [1.5, 1.3, 1.8, 2.2, 2.0, 1.6, 1.4, 1.7, 1.9, 2.2, 2.5, 2.3]  # KLD values for MidiNet 2
midiNet2_oa = [values[ol_index] for _, values in data_midi2.items()] # [0.75, 0.78, 0.76, 0.58, 0.60, 0.80, 0.77, 0.78, 0.79, 0.76, 0.73, 0.75]  # OA values for MidiNet 2


# ------------------- Create fig5 ---------------------
'''
1: PC
2: PC/bar
3: NC
4: NC/bar
5: PCH
6: PCH/bar
7: PCTM
8: PR
10: PI
11: IOI
12: NLH
13: NLTM
'''

features = ['PC', 'PC/bar', 'NC',
            'NC/bar', 'PCH', 'PCH/bar', 'PCTM', 'PR', 'PI', 'IOI', 'NLH', 'NLTM']

# Marker sizes
marker_size = 250
colors = ['#1F77B4', '#AEC7E8', '#FFBB78', '#2CA02C', '#D62829', '#FF9896', '#C5B0D5', '#8C564B', '#F0B1CC', '#BBBBBB', '#BCBD22', '#17BECF']

# Plotting each feature comparison
plt.figure(figsize=(9, 7))
for i, feature in enumerate(features):
    # Plot MidiNet 1
    plt.scatter(midiNet1_kld[i], midiNet1_oa[i], marker='^', s=marker_size, color=colors[i])
    plt.text(midiNet1_kld[i], midiNet1_oa[i], str(i + 1), fontsize=8, ha='center', va='top')

    # Plot MidiNet 2
    plt.scatter(midiNet2_kld[i], midiNet2_oa[i], marker='o', s=marker_size, color=colors[i])
    plt.text(midiNet2_kld[i], midiNet2_oa[i], str(i + 1), fontsize=8, ha='center', va='center')

    # Draw connecting lines
    plt.plot([midiNet1_kld[i], midiNet2_kld[i]], [midiNet1_oa[i], midiNet2_oa[i]],
             linestyle='--', linewidth=1.5, color=colors[i])


legend_handles = []
for i, feature in enumerate(features):
    legend_handles.append(plt.Line2D([0], [1], color=colors[i], linestyle='--', linewidth=1.5, label=f'{i+1}: {feature}'))

plt.legend(handles=legend_handles, loc='upper right')

# Adding labels and title
plt.xlabel('KLD')
plt.ylabel('OA')
plt.title('△ MidiNet 1 ○ MidiNet 2')

# Display the plot
plt.tight_layout()
plt.savefig('../data/exp_3/measurments_results/Fig5.png')