from music21 import converter
import re
import os
import glob

import requests
import zipfile


def get_abc_file():
    # Download the ZIP file from Henrik Norbeck's ABC Tunes website
    url = "https://www.norbeck.nu/abc/henrikabc.zip"
    r = requests.get(url)
    zip_path = "henrikabc.zip"

    with open(zip_path, "wb") as f:
        f.write(r.content)

    # Extract the ZIP file
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall("henrikabc")

    # List files in the extracted directory
    os.listdir("henrikabc")


def single_abc():
    # Example ABC notation as a string
    abc_string = """
    R:air
    B:Goodman manuscripts, http://port.itma.ie/score/ITMA_1401
    Z:id:hn-air-31
    M:3/4
    L:1/8
    K:Am
    A/B/c/d/ | e2 ea ge | dc B2 AF | A2 G2 A/B/c/d/ | d2 d2 fe | dc A2 GB | A4
    A/B/c/d/ | e2 ea ge | dc B2 AG | G2 G2 A/B/c/d/ | d2 d2 (3fed | dc A2 G2 | A4 ||
    eg | a2 a2 (3baf | ge d2 dc | B2 A2 eg | a2 a2 ba | ge d2 ea | g4
    Bd | e2 ea ge | ge d2 BA | A2 G2 A/B/c/d/ | d2 d2 gf | ed B2 G2 | A4 :|
    """

    # Parse the ABC notation
    abc_score = converter.parse(abc_string, format='abc')

    # Save the parsed ABC as a MIDI file
    abc_score.write('midi', fp='simple_tune_1.mid')

    # Print a message to confirm the conversion
    print("MIDI file created successfully.")


def multiple_abc():
    # Create a directory for ABC files (for demonstration purposes, this directory should already contain your ABC files)
    os.makedirs("abc_files", exist_ok=True)

    # Sample code to simulate having ABC files in the directory
    # In practice, you should have actual ABC files downloaded from a reliable source
    sample_abc_content = """
    X: 1
    T: Simple Tune
    M: 4/4
    L: 1/8
    K: C
    CDEFGABc | cBAGFEDC |
    """
    with open("abc_files/sample1.abc", "w") as f:
        f.write(sample_abc_content)
    with open("abc_files/sample2.abc", "w") as f:
        f.write(sample_abc_content)

    # Directory containing the ABC files
    abc_dir = "abc_files"
    midi_dir = "midi_files"

    # Create directory to save MIDI files
    os.makedirs(midi_dir, exist_ok=True)

    # Get all ABC files in the directory
    abc_files = glob.glob(os.path.join(abc_dir, "*.abc"))

    # Function to convert ABC to MIDI
    def convert_abc_to_midi(abc_file, midi_file):
        try:
            abc_score = converter.parse(abc_file, format='abc')
            abc_score.write('midi', fp=midi_file)
            print(f"Converted {abc_file} to {midi_file}")
        except Exception as e:
            print(f"Failed to convert {abc_file}: {e}")

    # Convert each ABC file to MIDI
    for abc_file in abc_files:
        midi_file = os.path.join(midi_dir, os.path.basename(abc_file).replace('.abc', '.mid'))
        convert_abc_to_midi(abc_file, midi_file)

    print("Conversion completed.")

    # Zip the MIDI files directory
    import shutil
    shutil.make_archive("midi_files", 'zip', midi_dir)


def parse_abc(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    # Split the file into tunes based on "X:" which denotes the start of a tune
    tunes = content.split('\nX:')
    tunes = ['X:' + tune if not tune.startswith('X:') else tune for tune in tunes]

    parsed_tunes = []
    tune_re = re.compile(r'X:(?P<index>\d+)\s*T:(?P<title>[^\n]+)\s*(?P<body>.*?)\n(?=X:|\Z)', re.DOTALL)

    for tune in tunes:
        match = tune_re.search(tune)
        if match:
            parsed_tunes.append({
                'index': match.group('index'),
                'title': match.group('title'),
                'body': match.group('body').strip()
            })

    return parsed_tunes


def print_parsed_tunes(parsed_tunes):
    for tune in parsed_tunes:
        print(f"X: {tune['index']}")
        print(f"T: {tune['title']}")
        print(f"{tune['body']}\n")
        print("=" * 40)


if __name__ == "__main__":
    # file_path = "sample_data/hnair0.abc"
    # parsed_tunes = parse_abc("sample_data/hnair0.abc")
    print_parsed_tunes(parse_abc("sample_data/hnair0.abc"))
