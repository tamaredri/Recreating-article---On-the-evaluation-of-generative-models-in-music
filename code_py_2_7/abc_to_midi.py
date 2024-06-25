import os
import re
import glob
from music21 import converter


def extract_first_8_bars(body):
    bars = body.split('|')
    if len(bars) > 8:
        first_8_bars = '|'.join(bars[:8]) + '|'
    else:
        first_8_bars = body  # If less than 8 bars, return the whole body
    return first_8_bars.strip()


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
            body = match.group('body').strip()
            first_8_bars = extract_first_8_bars(body)
            parsed_tunes.append({
                'index': match.group('index'),
                'title': match.group('title'),
                'body': first_8_bars
            })

    return parsed_tunes


def save_first_8_bars(parsed_tunes, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for tune in parsed_tunes:
        file_name = "tune_" + tune['index'] + "_first_8_bars.abc"
        file_path = os.path.join(output_dir, file_name)
        with open(file_path, 'w') as file:
            file.write("X:" + tune['index'] + "\n")
            file.write("T:" + tune['title'] + "\n")
            file.write(tune['body'] + "\n")


def convert_abc_to_midi(abc_dir, midi_dir):
    # Create a new directory for the 8-bar ABC files
    abc_8bar_dir = os.path.join(abc_dir, '8bar')
    if not os.path.exists(abc_8bar_dir):
        os.makedirs(abc_8bar_dir)

    # Get all ABC files in the directory
    abc_files = glob.glob(os.path.join(abc_dir, "*.abc"))

    # Process each ABC file
    for abc_file in abc_files:
        parsed_tunes = parse_abc(abc_file)
        save_first_8_bars(parsed_tunes, abc_8bar_dir)

    # Get all 8-bar ABC files
    abc_8bar_files = glob.glob(os.path.join(abc_8bar_dir, "*.abc"))

    # Convert each 8-bar ABC file to MIDI
    for abc_file in abc_8bar_files:
        midi_file = os.path.join(midi_dir, os.path.basename(abc_file).replace('.abc', '.mid'))
        try:
            abc_score = converter.parse(abc_file, format='abc')
            abc_score.write('midi', fp=midi_file)
            print("Converted {} to {}".format(abc_file, midi_file))
        except Exception as e:
            print("Failed to convert {}: {}".format(abc_file, e))


if __name__ == "__main__":
    convert_abc_to_midi("data/exp_1/abc/", "data/exp_1/midi")
