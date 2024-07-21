# pip install magenta note-seq
import note_seq
from magenta.models.melody_rnn import melody_rnn_sequence_generator
from magenta.models.shared import sequence_generator_bundle
from note_seq.protobuf import generator_pb2
from note_seq.protobuf import music_pb2
import os

# Initialize the model
print("Initializing Melody RNN...")
bundle = sequence_generator_bundle.read_bundle_file('lookback_rnn.mag')
generator_map = melody_rnn_sequence_generator.get_generator_map()
melody_rnn = generator_map['lookback_rnn'](checkpoint=None, bundle=bundle)
melody_rnn.initialize()
print('🎉 Done!')

# Load the input MIDI file
input_sequence = note_seq.midi_io.midi_file_to_note_sequence('tune_1_first_bar.mid')

# Parameters for generation
bars_to_generate = 7  # Generate next 7 bars
steps_per_bar = melody_rnn.steps_per_quarter * 4  # Assuming 4/4 time signature
num_steps = steps_per_bar * bars_to_generate
temperature = 1.0  # The higher the temperature, the more random the sequence

# Calculate generation parameters
last_end_time = (max(n.end_time for n in input_sequence.notes) if input_sequence.notes else 0)
qpm = input_sequence.tempos[0].qpm
seconds_per_step = 60.0 / qpm / melody_rnn.steps_per_quarter
total_seconds = num_steps * seconds_per_step

# Create directory to store generated samples
output_dir = 'generated_samples'
os.makedirs(output_dir, exist_ok=True)

# Generate 100 samples
for i in range(100):
    generator_options = generator_pb2.GeneratorOptions()
    generator_options.args['temperature'].float_value = temperature
    generate_section = generator_options.generate_sections.add(
        start_time=last_end_time + seconds_per_step,
        end_time=last_end_time + seconds_per_step + total_seconds
    )

    # Generate the sequence
    generated_sequence = melody_rnn.generate(input_sequence, generator_options)

    # Save the generated sequence to a MIDI file
    output_midi_path = os.path.join(output_dir, f'generated_sample_{i + 1}.mid')
    note_seq.midi_io.note_sequence_to_midi_file(generated_sequence, output_midi_path)

    # Optionally plot the sequence
    note_seq.plot_sequence(generated_sequence)

    print(f'Sample {i + 1} generated and saved to {output_midi_path}')
