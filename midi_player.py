from pydub import AudioSegment
from pydub.generators import Sine
import pygame
from midiutil.MidiFile import MIDIFile

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

def save_to_midi_file(notes, midi_path):
    print("writing to midi file")

    # create your MIDI object
    mf = MIDIFile(1)     # only 1 track
    track = 0   # the only track

    time = 0    # start at the beginning
    mf.addTrackName(track, time, "Sample Track")
    mf.addTempo(track, time, 120)

    channel = 0
    volume = 100
    for note in notes: 
        if note.startswith('(('):
            # Element is a chord, parse it into a list of notes
            chord_notes = eval(note)
            for note_str in chord_notes:
                pitch, octave, accidental, duration = note_str
                if pitch == 'rest':
                    continue
                pitch = pitch_to_midi(pitch, octave, accidental)
                duration = duration_to_value(duration)
                mf.addNote(track, channel, pitch, time, duration, volume)
            time = time + duration
            
        else: #is not chord, is a note
            pitch, octave, accidental, duration = eval(note)
            if pitch == 'rest':
                time = time + duration
            pitch = pitch_to_midi(pitch, octave, accidental)
            duration = duration_to_value(duration)
            mf.addNote(track, channel, pitch, time, duration, volume)
                

    # write it to disk
    with open(midi_path, 'wb') as outf:
        mf.writeFile(outf)


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
    # path = "melody3.wav"
    midi_path = "midi_melody.mid"
    # save_to_file(notes, path)
    save_to_midi_file(notes,midi_path)
    # play_melody(path)
    #play_melody(midi_path)

if __name__ == "__main__":
    main()

