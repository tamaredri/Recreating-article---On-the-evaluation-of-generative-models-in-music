# Recreating-article---On-the-evaluation-of-generative-models-in-music
Tamar Edri & Reut Marmerosh

Steps for recreating the article:
### EXP1:
1. Download the Folk & Jazz songs in ABC format from - https://www.norbeck.nu/abc/download.asp and https://trillian.mit.edu/~jc/cgi/abc/find.cgi?P=jazz&find=FIND&m=title&W=wide&scale=0.65&limit=1000&thresh=5&fmt=single&V=1&Tsel=tune&Nsel=0 accordingly.
2. Run the 'code_py_2_7/abc_to_midi.py' to convert the songs into MID files.
3. Run the 'code_py_2_7/feature_extraction.py' for feature extraction.
4. Run the 'code_py_3_10/Recreating_table2.py' and 'code_py_3_10/Recreating_Fig3.py' to recreate table 2 and figure 3 for Folk & Jazz extracted features.

### EXP2:
 Magenta:

1. Download the xml song files from https://github.com/owencm/hooktheory-data.
2. Run the 'code_py_3_7/TheoryTab_crawler/convert_xml_to_leed_sheet_format.py' to convert the xml files to the expected file system.
3. Run the 'code_py_3_7/TheoryTab_crawler/main.py' to convert xml files to MID.
4. Select 1 MID file, cut it's first bar and put ot in 'code_py_3_7/Magenta' directory.
5. Run the 'code_py_3_7/Magenta/magenta_model.py' to generate 100 samples according to this bar.

For MidiNet:
We were unable to run the code from the official repositories provided for those models.
- MidiNet Model - https://github.com/RichardYang40148/MidiNet
- MuesGan Model - https://github.com/salu133445/musegan

#Plotting the results
The directory 'code_3_10' contains scripts that, given the feature extraction results, can generate the plots from the article.
Since we do not have the MidiNet results, we were only able to run Recreating_table2.py and Recreating_Fig3.py.
