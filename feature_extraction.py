#  pip install numpy pretty_midi seaborn matplotlib scikit-learn py-abc_folk music21 re glob os
import abc
import glob
import numpy as np
import pretty_midi
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import LeaveOneOut

set1 = glob.glob('data/exp_1/abc_folk/*')
print(set1)

num_samples = 3


