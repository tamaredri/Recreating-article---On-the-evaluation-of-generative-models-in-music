# pip install pandas seaborn matplotlib.pyplot openpyxl

import json

with open('../data/exp_1/measurments_results/results.json', 'r') as file:
    # Parse the JSON file into a Python dictionary or list
    data = json.load(file)

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Sample 12x12 matrix
# matrix = np.random.rand(12, 12)

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
    '𝅗𝅥 𝅗𝅥 𝅗𝅥',  # (Triplet Half Notes, indicated by "3" above/below)
    '𝅘𝅥 𝅘𝅥 𝅘𝅥',  # (Triplet Quarter Notes, indicated by "3" above/below)
    '𝅘𝅥𝅮 𝅘𝅥𝅮 𝅘𝅥𝅮'  # (Triplet Eighth Notes, indicated by "3" above/below)
]

# Convert to Pandas DataFrame for better control
df1 = pd.DataFrame(data['pitch_class_transition_matrix'][0], index=notes, columns=notes) # set 1
df2 = pd.DataFrame(data['pitch_class_transition_matrix'][2], index=notes, columns=notes) # set 2

# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df1, annot=True, cmap='viridis')

# Customize plot
plt.title('Folk')
plt.xlabel('Columns')
plt.ylabel('Rows')

# Display the heatmap
plt.show()


# Plot the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df2, annot=True, cmap='viridis')

# Customize plot
plt.title('Jazz')
plt.xlabel('Columns')
plt.ylabel('Rows')

# Display the heatmap
plt.show()

