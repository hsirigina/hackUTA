#!/usr/bin/env python3
"""
Simple TTS to Bluetooth Speaker
Just connect your Bluetooth speaker to your computer first, then run this script.
"""

import pyttsx3

def speak_text(text):
    """
    Speak the given text using pyttsx3 (offline TTS).
    Will output to whatever audio device is set as default (e.g., your Bluetooth speaker).
    """
    engine = pyttsx3.init()

    # Optional: Configure voice properties
    engine.setProperty('rate', 150)    # Speed of speech (words per minute)
    engine.setProperty('volume', 0.9)  # Volume (0.0 to 1.0)

    # Speak the text
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Test the speaker
    print("Testing TTS through your audio output...")
    speak_text("Hello! I am connected to your Bluetooth speaker. This is a test.")
    print("Done! Did you hear that?")