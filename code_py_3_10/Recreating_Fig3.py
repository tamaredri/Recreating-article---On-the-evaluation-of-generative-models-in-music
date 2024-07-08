import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.backends.backend_pdf import PdfPages


def plot_fig3_collection(collection_metric_data, metric_acronyms, tick_names, font=None):

    c_tunes = []
    prop = FontProperties()
    if font:  # define a font to present the notes
        prop = FontProperties(family='Musisync-KVLZ', fname=font)

    with PdfPages('../data/exp_1/measurments_results/Fig3_foreach_tune_Section4.1_' + metric_acronyms + '.pdf') as pdf:
        for index, metric_data in enumerate(collection_metric_data):
            # Normalizing the values
            np_jazz = np.array(metric_data)
            print(f"{index}: {metric_data[0][0]}")
            if metric_data[0][0] > 3.0:
                c_tunes.append(index)
            np_jazz = (np_jazz / np_jazz.max()) * 0.05

            df = pd.DataFrame(np_jazz, index=tick_names, columns=tick_names)  # Set 2

            fig, ax = plt.subplots(figsize=(10, 8))

            sns.heatmap(df, annot=False, cmap='jet', linecolor='white', ax=ax)
            ax.set_title('Jazz', fontsize=30)

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

            if(metric_data[0][0] >= 6.28):
                fig.suptitle(f"{metric_acronyms} - Index {index} | metric_data[0][0] = {metric_data[0][0]}", fontsize=20,
                             bbox=dict(facecolor='yellow', alpha=0.5, edgecolor='none'))
            else:
                fig.suptitle(f"{metric_acronyms} - Index {index} | metric_data[0][0] = {metric_data[0][0]}", fontsize=20)

            plt.tight_layout()  # Leave space for the main title
            pdf.savefig(fig)  # Save the current figure into the PDF
            plt.close(fig)  # Close the figure to free memory

    print(f"All heatmaps have been saved to ../data/exp_1/measurments_results.")
    print(f"c_tunes: {c_tunes}")


# Sample cell names
def plot_fig3(metric_data, metric_acronyms, tick_names, font=None):
    # Convert to Pandas DataFrame for better control

    # normalizing the values
    np_1 = np.array(metric_data[0])
    np_1 = (np_1 / np_1.max()) * 0.05
    np_2 = np.array(metric_data[2])
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
    #plot_fig3(data['pitch_class_transition_matrix'], 'PCTM', notes)

    #notes = ['w', 'h', 'q', 'e', 's', 'd', 'j', 'i', 's.', 'hhh', 'qqq', 'eee']
    #plot_fig3(data['note_length_transition_matrix'], 'NLTM', notes, font=f"../data/fonts/Musisync-KVLZ.ttf")

    # Extract the collection of metric data
    plot_fig3_collection(data['pitch_class_transition_matrix'][12], 'PCTM', notes)

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

