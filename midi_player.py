from pydub import AudioSegment
from pydub.generators import Sine
import pygame


def create_note(pitch, duration):
    # Calculate frequency from MIDI pitch
    frequency = 440 * (2 ** ((pitch - 69) / 12))
    
    # Generate sine wave with the calculated frequency and duration
    sine_wave = Sine(frequency)
    note = sine_wave.to_audio_segment(duration * 1000)  # duration in milliseconds
    
    return note

def play_notes(notes):
    # Initialize an empty audio segment
    melody = AudioSegment.silent(duration=0)

    # Create and concatenate audio segments for each note
    for pitch, duration in notes:
        note = create_note(pitch, duration)
        melody += note
    
    # Export the melody
    melody.export("melody.wav", format="wav")

    #for playing right away
    # # Initialize pygame
    # pygame.mixer.init()
    
    # # Load and play the WAV file
    # pygame.mixer.music.load("melody.wav")
    # pygame.mixer.music.play()
    
    # # Wait for the music to finish playing
    # while pygame.mixer.music.get_busy():
    #     pygame.time.Clock().tick(10)

def main(notes_list):
    notes = create_note(notes_list)
    play_notes(notes)

if __name__ == "__main__":
    main()

# # Example usage
# notes = [(60, 1), (62, 0.5), (64, 0.5), (65, 1)]  # Example notes (MIDI pitch, duration)
# play_notes(notes)

