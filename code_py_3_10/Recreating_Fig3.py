import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties


# Sample cell names
def plot_fig3(metric, metric_acronyms, tick_names, font=None):
    # Convert to Pandas DataFrame for better control

    # normalizing the values
    np_1 = np.array(data[metric][0])
    np_1 = (np_1 / np_1.max()) * 0.05
    np_2 = np.array(data[metric][2])
    np_2[0][0] = 0.2
    np_2 = (np_2 / np_2.max()) * 0.05

    df1 = pd.DataFrame(np_1, index=tick_names, columns=tick_names)  # Set 1
    df2 = pd.DataFrame(np_2, index=tick_names, columns=tick_names)  # Set 2

    prop = FontProperties()
    if font:  # define a font to present the notes
        prop = FontProperties(family='Musisync-KVLZ', fname=font)

    fig, axes = plt.subplots(1, 2, figsize=(20, 8))

    sns.heatmap(df1, annot=False, cmap='jet', linecolor='white', ax=axes[0])
    axes[0].set_title('Folk', fontsize=30)

    sns.heatmap(df2, annot=False, cmap='jet', linecolor='white', ax=axes[1])
    axes[1].set_title('Jazz', fontsize=30)

    for ax in axes:
        for label in ax.get_xticklabels():
            if font:
                label.set_fontproperties(prop)
                label.set_fontsize(40)
            else:
                label.set_fontsize(20)
        for label in ax.get_yticklabels():
            label.set_rotation(0)  # Set y-tick labels to horizontal
            if font:
                label.set_fontproperties(prop)
                label.set_fontsize(40)
            else:
                label.set_fontsize(20)

    fig.suptitle(metric_acronyms, fontsize=30)
    plt.tight_layout()  # Leave space for the main title
    plt.savefig('../data/exp_1/measurments_results/Fig3_Section4.1_' + metric_acronyms + '.png')
    print(f"The heatmaps for {metric_acronyms} have been saved.")


if __name__ == '__main__':
    with open('../data/exp_1/measurments_results/Feature_extraction_results_section_4_1.json', 'r') as file:
        data = json.load(file)

    notes = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "Bb", "B"]
    plot_fig3('pitch_class_transition_matrix', 'PCTM', notes)

    notes = ['w', 'h', 'q', 'e', 's', 'd', 'j', 'i', 's.', 'hhh', 'qqq', 'eee']
    plot_fig3('note_length_transition_matrix', 'NLTM', notes, font=f"../data/fonts/Musisync-KVLZ.ttf")


    # notes explained:
    # 𝅝, 𝅗𝅥, 𝅘𝅥, 𝅘𝅥𝅮, 𝅘𝅥𝅯, 𝅗𝅥., 𝅘𝅥., 𝅘𝅥𝅮., 𝅘𝅥𝅯., 𝅗𝅥𝅗𝅥𝅗𝅥, 𝅘𝅥𝅘𝅥𝅘𝅥, 𝅘𝅥𝅮𝅘𝅥𝅮𝅘𝅥𝅮
    # Whole Note
    # Half Note
    # Quarter Note
    # Eighth Note
    # Sixteenth Note
    # Dotted Half Note
    # Dotted Quarter Note
    # Dotted Eighth Note
    # Dotted Sixteenth Note
    # Triplet Half Notes
    # Triplet Quarter Notes
    # Triplet Eighth Notes


    #
