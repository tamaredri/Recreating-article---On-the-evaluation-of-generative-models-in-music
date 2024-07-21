# Directory for code using Python 2.7.18

### This repository contains the following scripts:
1. Conversion from ABC to MID files
2. Performing the process of feature extraction

## Dependencies
* python 2.7
* pretty_midi=0.2.8 
* scikit-learn 
* python-midi=0.2.4 
* music21

### ABC to MIDI
Requires the following parameters: (in main.py)
* abc_dirs = folder names list for the input abc files 
* input_abc_dir = base dir for the input abc folders
* output_midi_dir = base dir for the output midi folders and files

# Feature extraction
Requires the following parameters: (in configuration args)
* set1dir, set2dir - paths to the 2 datasets
* outfile - path to the output directory
* num-bar - number of bars to include in the process
