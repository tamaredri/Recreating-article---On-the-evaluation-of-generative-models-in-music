from music21 import converter
import re
import os
import glob

failed = []


def extract_first_8_bars(body):
    bars = body.split('|')
    if len(bars) > 8:
        first_8_bars = '|'.join(bars[:8]) + '|'
    else:
        first_8_bars = body  # If less than 8 bars, return the whole body
    return first_8_bars.strip()


def parse_abc(abc_file_path):

    # 1. read the file with 100 abc_folk tunes
    with open(abc_file_path, 'r') as file:
        content = file.read()

    # 2. Split the file into tunes based on "X:" which denotes the start of a tune
    tunes = content.split('\nX:')
    tunes = ['X:' + tune if not tune.startswith('X:') else tune for tune in tunes]

    parsed_tunes = []
    tune_re = re.compile(r'X:(?P<index>\d+)\s*T:(?P<title>[^\n]+)\s*(?P<body>.*?)\n(?=X:|\Z)', re.DOTALL)

    # 3. save in parsed_tunes the first 8 bars for each tune
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


def save_abc_tunes(parsed_tunes, abc_dir_path):
    if not os.path.exists(abc_dir_path):
        os.makedirs(abc_dir_path)

    for tune in parsed_tunes:
        abc_file_name = f"tune_{tune['index']}_first_8_bars.abc_folk"
        abc_file_path = os.path.join(abc_dir_path, abc_file_name)
        with open(abc_file_path, 'w') as file:
            file.write(f"X:{tune['index']}\n")
            file.write(f"T:{tune['title']}\n")
            file.write(f"{tune['body']}\n")


def convert_abc_to_midi(abc_file, midi_file):
    global failed
    try:
        abc_score = converter.parse(abc_file, format='abc_folk')
        abc_score.write('midi_folk', fp=midi_file)
        print(f"\nConverted {abc_file} to {midi_file}", end='')
    except Exception as e:
        print(f"\nFailed to convert {abc_file}: {e}", end='')
        failed += [abc_file]


def convert_multiple_abc_to_midi(abc_dir_path, midi_dir_path):

    # Get all ABC files in the directory
    abc_files = glob.glob(os.path.join(abc_dir_path, "*.abc_folk"))

    if not os.path.exists(midi_dir_path):
        os.makedirs(midi_dir_path)

    # Convert each ABC file to MIDI
    for abc_file in abc_files:
        midi_file = os.path.join(midi_dir_path, os.path.basename(abc_file).replace('.abc_folk', '.mid'))
        convert_abc_to_midi(abc_file, midi_file)


if __name__ == "__main__":
    # 1 extract 100 abc_folk file from abc_collection and extract only first 8 bars from each abc_folk tune
    print("1. extract 100 abc_folk file from abc_collection", end='')
    parsed_abc_tunes = parse_abc("abc_collection.abc")
    print("---end\n")

    # 2. save list of abc_folk tune to abc_folk file
    print("2. Saved the first 8 bars of each tune to abc_folk dir", end='')
    save_abc_tunes(parsed_abc_tunes, "abc_folk")
    print("---end\n")

    # 3. convert abc_folk files (from abc_folk directory) to midi_folk files
    print("3. convert abc_folk files to midi_folk files", end='')
    convert_multiple_abc_to_midi("abc_folk", "midi_folk")
    print("---end\n")
    print(failed)



