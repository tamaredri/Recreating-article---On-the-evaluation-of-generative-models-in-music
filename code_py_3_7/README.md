# Directory for code using Python 3.7

### This repository contains the following scripts:
1. Magenta - music generation model
2. TheoryTab crawler

## Dependencies
* Pillow==9.5.0	
* beautifulsoup4==4.12.3	
* fonttools==4.38.0	
* lxml==5.2.2	
* matplotlib==3.5.3	
* mido==1.3.2	
* numpy==1.21.6	
* pretty-midi==0.2.10
* pypianoroll==1.0.4
* requests==2.31.0	
* scipy==1.7.3	
* setuptools==57.0.0	
* urllib3==1.26.15	


## Magenta
- The code requires the prebuilt model - 'lookback_rnn.mag', and the first bar of a song - 'song_name.mid'.
- The results will be stored in a 'generated_samples' folder in the 'Magenta' directory.

## TheoryTab crawler
- The code requires xml files containing songs representation from the theorytab website, 
stored in 'hooktheory-data\xml\' folder.
- Then, run the code in 'convert_xml_to_leed_sheet_format.py' that converts the list of xml files to the file system expected in 'main.py'
- Then run 'main.py' to get the MID representation of the songs.
