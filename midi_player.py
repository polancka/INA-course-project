from pydub import AudioSegment
from pydub.generators import Sine
import pygame
from miditime.miditime import MIDITime

# Functionality of reading the MIDI notation list of notes and save it to a wav file (and optionally instantly play it)

def pitch_to_midi(pitch, octave, accidental):
    # Mapping of pitch names to MIDI numbers
    pitch_mapping = {'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
                     'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
                     'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11}

    if pitch == 'rest':
        return None  # Return None for rest
    else: 
        # Calculate MIDI pitch
        midi_pitch = pitch_mapping[pitch]

        # Adjust MIDI pitch based on octave
        midi_pitch += (int(octave) + 1) * 12  # Assuming MIDI octave starts from -1

        # Adjust MIDI pitch based on accidental
        if accidental == 'sharp':
            midi_pitch += 1
        elif accidental == 'flat':
            midi_pitch -= 1

    return midi_pitch

def duration_to_value(duration):
    # Mapping of duration names to numerical values
    duration_mapping = {'breve':2.0,'whole': 1.0, 'half': 0.5, 'quarter': 0.25,
                        'eighth': 0.125, '16th': 0.0625}

    # Return the numerical value of the duration
    return duration_mapping[duration]

def duration_to_midi(duration):
     # Mapping of duration names to MIDI note lengths
    duration_mapping = {'breve': 8, 'whole': 4, 'half': 2, 'quarter': 1,
                        'eighth': 0.5, '16th': 0.25, '32nd': 0.125, '64th': 0.0625}
    
    # Return the MIDI note length
    return float(duration_mapping[duration])

def create_note(pitch, octave, accidental, duration):
    if pitch == "rest":
        # Return a silent audio segment for the rest duration
        duration_value = duration_to_value(duration)
        return AudioSegment.silent(duration=int(duration_value * 1000))  # duration in milliseconds
    else: 
        # Calculate MIDI pitch
        midi_pitch = pitch_to_midi(pitch, octave, accidental)
        
        # Convert duration to numerical value
        duration_value = duration_to_value(duration)
        print(midi_pitch, duration_value)
        # Calculate frequency from MIDI pitch
        frequency = 440 * (2 ** ((midi_pitch - 69) / 12))
        
        # Generate sine wave with the calculated frequency and duration
        sine_wave = Sine(frequency)
        note = sine_wave.to_audio_segment(duration_value * 1000)  # duration in milliseconds
        note = note.fade_in(10).fade_out(10)
        return note


def save_to_file(notes, path):
    # Initialize an empty audio segment
    melody = AudioSegment.silent(duration=0)

    # Create and concatenate audio segments for each note or chord
    for element in notes:
        # Check if the element is a chord or a single note
        if element.startswith('(('):
            # Element is a chord, parse it into a list of notes
            chord_notes = eval(element)
            
            # Create audio segments for each note in the chord
            chord_segments = []
            for note_str in chord_notes:
                pitch, octave, accidental, duration = note_str
                note = create_note(pitch, octave, accidental, duration)
                chord_segments.append(note)
            
            # Combine audio segments for each note in the chord
            chord_segment = sum(chord_segments)
            melody += chord_segment
        else:
            # Element is a single note, parse it into components and create audio segment
            pitch, octave, accidental, duration = eval(element)
            note = create_note(pitch, octave, accidental, duration)
            melody += note

     # Set sample width and frame rate
    melody = melody.set_sample_width(2)  # 16-bit
    melody = melody.set_frame_rate(44100)  # 44100 Hz
    
    # Export the melody
    melody.export(path, format="wav")

def save_to_midi_file(notes, filename):
    print("writing to midi file")

    # Create MIDI object with the desired BPM and number of beats per section
    midi = MIDITime(90, filename, 5, 5, 1)
    beats = 0.0
    midi_notes = []
    velocity = 127 
    for note in notes: 
        if note.startswith('(('):
            # Element is a chord, parse it into a list of notes
            chord_notes = eval(note)
            for note_str in chord_notes:
                pitch, octave, accidental, duration = note_str
                if pitch == 'rest': #THIS IS A PAUSE; BUT IN A CHORD SO WE CAN JUST SKIP IT
                    continue
                pitch = pitch_to_midi(pitch, octave, accidental)
                duration_beats = duration_to_midi(duration)
                midi_notes.append([beats, pitch, velocity, duration_beats])
            beats = beats + duration_beats
            
        else: #is not chord, is a note
            pitch, octave, accidental, duration = eval(note)
            if pitch == 'rest': #THIS IS A PAUSE
                duration_beats = duration_to_midi(duration)
                beats = beats + duration_beats
                continue
            pitch = pitch_to_midi(pitch, octave, accidental)
            duration_beats = duration_to_midi(duration)
            midi_notes.append([beats, pitch, velocity, duration_beats])
            beats = beats + duration_beats

    print(midi_notes)            
    midi.add_track(midi_notes)
    # Export the melody as a MIDI file
    midi.save_midi()


def play_melody(file):
    # Initialize pygame
    pygame.mixer.init()
    
    # Load and play the WAV file
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)



def main(notes):
    print("notes")
    # path = "melody3.wav"
    midi_path = "songs/scotishLute_multi_5.mid"
    # save_to_file(notes, path)
    save_to_midi_file(notes,midi_path)
    # play_melody(path)
    #play_melody(midi_path)

if __name__ == "__main__":
    main()

