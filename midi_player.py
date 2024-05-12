from pydub import AudioSegment
from pydub.generators import Sine
import pygame

# Functionality of reading the MIDI notation list of notes and save it to a wav file (and optionally instantly play it)

def create_note(pitch, duration):
    # Calculate frequency from MIDI pitch
    frequency = 440 * (2 ** ((pitch - 69) / 12))
    
    # Generate sine wave with the calculated frequency and duration
    sine_wave = Sine(frequency)
    note = sine_wave.to_audio_segment(duration * 1000)  # duration in milliseconds
    
    return note

def save_to_file(notes, path):
    # Initialize an empty audio segment
    melody = AudioSegment.silent(duration=0)

    # Create and concatenate audio segments for each note
    for pitch, duration in notes:
        note = create_note(pitch, duration)
        melody += note
    
    # Export the melody
    melody.export(path, format="wav")


def play_melody(file):
    # Initialize pygame
    pygame.mixer.init()
    
    # Load and play the WAV file
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
    
    # Wait for the music to finish playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def main(notes_list):
    path = "melody.wav"
    save_to_file(notes, path)
    play_melody(path)

if __name__ == "__main__":
    notes = [(60, 1), (62, 0.5), (64, 0.5), (65, 1)]  # Example notes (MIDI pitch, duration)
    main(notes)

