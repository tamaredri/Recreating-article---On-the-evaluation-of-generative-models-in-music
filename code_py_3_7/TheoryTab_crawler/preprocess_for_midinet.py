import os
import numpy as np
import mido
import pypianoroll
from pypianoroll import Multitrack, Track

# Define constants
BASIC_CHORD_TRIADS = {
    'C': [0, 4, 7], 'Cm': [0, 3, 7], 'C#': [1, 5, 8], 'C#m': [1, 4, 8],
    'D': [2, 6, 9], 'Dm': [2, 5, 9], 'D#': [3, 7, 10], 'D#m': [3, 6, 10],
    'E': [4, 8, 11], 'Em': [4, 7, 11], 'F': [5, 9, 0], 'Fm': [5, 8, 0],
    'F#': [6, 10, 1], 'F#m': [6, 9, 1], 'G': [7, 11, 2], 'Gm': [7, 10, 2],
    'G#': [8, 0, 3], 'G#m': [8, 11, 3], 'A': [9, 1, 4], 'Am': [9, 0, 4],
    'A#': [10, 2, 5], 'A#m': [10, 1, 5], 'B': [11, 3, 6], 'Bm': [11, 2, 6]
}
CHORD_KEYS = list(BASIC_CHORD_TRIADS.keys())
CHORD_TYPES = {'major': 0, 'minor': 1}
OCTAVE_SHIFT = 5  # C4 to B5
NUM_MIDI_NOTES = 128


# Define helper functions
def is_basic_chord(chord_notes):
    for chord_name, chord_intervals in BASIC_CHORD_TRIADS.items():
        if set(chord_notes) == set(chord_intervals):
            return True
    return False


def process_melody(track):
    # Convert to two octaves C4 to B5
    track.pianoroll = np.clip(track.pianoroll, 60, 83)
    # Remove velocity
    track.pianoroll[track.pianoroll > 0] = 1
    # Prolong notes if necessary
    for i in range(track.pianoroll.shape[0] - 1):
        if np.sum(track.pianoroll[i + 1]) == 0:
            track.pianoroll[i + 1] = track.pianoroll[i]
    # Shift all notes to be within the two octaves
    track.pianoroll = np.where((track.pianoroll >= 60) & (track.pianoroll <= 83), track.pianoroll, 0)
    return track


def process_chords(track):
    # Reduce to one chord per bar
    bars = np.split(track.pianoroll, np.arange(0, track.pianoroll.shape[0], 16))
    new_chords = []
    for bar in bars:
        if np.sum(bar) > 0:
            new_chords.append(np.sum(bar, axis=0))
        else:
            new_chords.append(np.zeros(bar.shape[1]))
    track.pianoroll = np.vstack(new_chords)
    return track


def augment_data(multitrack):
    augmented_tracks = []
    for i in range(12):
        augmented_multitrack = multitrack.copy()
        for track in augmented_multitrack.tracks:
            track.pianoroll = np.roll(track.pianoroll, i * 12, axis=1)
        augmented_tracks.append(augmented_multitrack)
    return augmented_tracks


def process_midi(filename, beats_in_measure):
    multitrack = pypianoroll.read(filename)
    melody_track = None
    chord_track = None

    # Find melody and chord tracks
    for track in multitrack.tracks:
        if 'melody' in track.name.lower():
            melody_track = track
        elif 'chord' in track.name.lower():
            chord_track = track

    new_tracks = []

    if melody_track:
        melody_track = process_melody(melody_track)
        new_tracks.append(melody_track)

    if chord_track:
        chord_track = process_chords(chord_track)
        new_tracks.append(chord_track)

    if not new_tracks:
        print(f"Skipping {filename}: No melody or chord track found.")
        return []

    new_multitrack = Multitrack(tracks=new_tracks, resolution=multitrack.resolution)
    return augment_data(new_multitrack)


def main(input_dir, output_dir, beats_in_measure=4):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    all_augmented_tracks = []

    for filename in os.listdir(input_dir):
        if filename.endswith('.mid'):
            filepath = os.path.join(input_dir, filename)
            augmented_tracks = process_midi(filepath, beats_in_measure)
            all_augmented_tracks.extend(augmented_tracks)

    for i, track in enumerate(all_augmented_tracks):
        output_path = os.path.join(output_dir, f"processed_{i}.mid")
        pypianoroll.write(output_path, track)


if __name__ == '__main__':
    input_dir = r'..\hooktheory-data\datasets_new\pianoroll\adam-lambert\whataya-want-from-me'
    output_dir = r'..\hooktheory-data\datasets_clean\adam-lambert\whataya-want-from-me'
    main(input_dir, output_dir)
