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


def convert_abc_to_midi(abc_dir, midi_dir):
    if not os.path.exists(midi_dir):
        os.makedirs(midi_dir)

    # Get all ABC files in the directory
    abc_files = glob.glob(os.path.join(abc_dir, "*.abc"))

    # Process each ABC file
    for abc_file in abc_files:
        parsed_tunes = parse_abc(abc_file)

        # Convert each parsed tune to MIDI
        for tune in parsed_tunes:
            abc_content = "X:{}\nT:{}\n{}".format(tune['index'], tune['title'], tune['body'])
            midi_file = os.path.join(midi_dir, "tune_{}_first_8_bars.mid".format(tune['index']))
            try:
                abc_score = converter.parse(abc_content, format='abc')
                abc_score.write('midi', fp=midi_file)
                print("Converted {} to {}".format(abc_file, midi_file))
            except Exception as e:
                print("Failed to convert {}: {}".format(abc_file, e))


if __name__ == "__main__":
    abc_dirs = ["folk", "jazz"]
    for abc_dir in abc_dirs:
        convert_abc_to_midi("../data/exp_1/abc/abc_" + abc_dir, "../data/exp_1/midi/midi_" + abc_dir)
