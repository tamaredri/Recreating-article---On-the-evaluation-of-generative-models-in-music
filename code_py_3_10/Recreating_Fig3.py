import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Read the JSON file
with open('../data/exp_1/measurments_results/Feature_extraction_results.json', 'r') as file:
    data = json.load(file)

# Sample cell names
notes = [
    '𝅝',  # Whole Note
    '𝅗𝅥',  # Half Note
    '𝅘𝅥',  # Quarter Note
    '𝅘𝅥𝅮',  # Eighth Note
    '𝅘𝅥𝅯',  # Sixteenth Note
    '𝅗𝅥.',  # Dotted Half Note
    '𝅘𝅥.',  # Dotted Quarter Note
    '𝅘𝅥𝅮.',  # Dotted Eighth Note
    '𝅘𝅥𝅯.',  # Dotted Sixteenth Note
    '𝅗𝅥 𝅗𝅥 𝅗𝅥',  # Triplet Half Notes
    '𝅘𝅥 𝅘𝅥 𝅘𝅥',  # Triplet Quarter Notes
    '𝅘𝅥𝅮 𝅘𝅥𝅮 𝅘𝅥𝅮'  # Triplet Eighth Notes
]

# Convert to Pandas DataFrame for better control
df1 = pd.DataFrame(data['pitch_class_transition_matrix'][0], index=notes, columns=notes)  # Set 1
df2 = pd.DataFrame(data['pitch_class_transition_matrix'][2], index=notes, columns=notes)  # Set 2

# Create a single figure with two subplots side by side
fig, axes = plt.subplots(1, 2, figsize=(20, 8))

# Plot the first heatmap
sns.heatmap(df1, annot=True, cmap='viridis', ax=axes[0])
axes[0].set_title('Folk')
axes[0].set_xlabel('Columns')
axes[0].set_ylabel('Rows')

# Plot the second heatmap
sns.heatmap(df2, annot=True, cmap='viridis', ax=axes[1])
axes[1].set_title('Jazz')
axes[1].set_xlabel('Columns')
axes[1].set_ylabel('Rows')

# Adjust layout
plt.tight_layout()

# Save the figure to a PNG file
plt.savefig('../data/exp_1/measurments_results/Fig3_Section4.1.png')

print("The heatmaps have been saved to 'heatmaps.png'.")
