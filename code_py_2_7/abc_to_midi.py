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
    abc_dirs = [ "jazz"]
    for abc_dir in abc_dirs:
        convert_abc_to_midi("../data/exp_1/abc/abc_" + abc_dir, "../data/exp_1/midi/midi_" + abc_dir)



"""


X:7
T:Groovin' high
M:4/4
L:1/8
C:Dizzy Gillespie
Q:1/4=160
K:Eb
%%text (medium)
%%vskip 20
% A %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
P:A
_c=A || "Ebmaj7"BGz2 z4 | BGz2 z4 | "Am7"z=E=Ac =BA^GE | "D7"=GF^Fd- d4c=A |
"Ebmaj7"BGz2 z4 | BGz2 z4 | "Gm7"zDGB =AG^FD | "C7"=F^D=Ec- c2 B^G ||
P:B
"F7"=AFz2 z4 | (3=ABA F2 z2 | "Fm7"zCF_A GF=EC | "Bb7"_E^CDB- B2A^F |
"Gm7"GBdf-f2df | "Gbm7"(3=e_ed _d4 z4 | "Fm7"FAce-e2ce | "Bb7"(3d_dc _c2 z2 c/_d/c/=A/ ||
P:A
"Ebmaj7"BGz2 z4 | BGz2 z4 | "Am7"z=E=Ac =BA^GE | "D7"=GF^Fd- d4c=A |
"Ebmaj7"BGz2 z4 | BGz2 z4 | "Gm7"zDGB =AG^FD | "C7"=F^D=Ec- c2 B^G ||
P:C
"F7"=AFz2 z4 | (3=ABA F2 z2 | "Fm7"zCF_A GF=EC | "Bb7"_E^CDB- B2A=E |
"Fm7"F2FG AGF2 | "Abm7"A2AB _cBAe | "Eb6"z8 | "T.A."z8 |]
"""