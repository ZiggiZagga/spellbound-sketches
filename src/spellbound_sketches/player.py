
"""Display animated GIFs and optionally speak accompanying text (TTS)."""

import tkinter as tk  # tkinter helps us make simple windows and GUIs (Graphical User Interfaces)
from PIL import Image, ImageTk, ImageSequence  # PIL lets us work with images and animations
import threading  # threading lets us do two things at once (like talking and showing pictures)
import pyttsx3  # pyttsx3 is a library that makes the computer talk (Text-to-Speech)
import time

def playtts(text):
    """Speak the given text using the system TTS engine."""
    if not text:
        return  # If there's nothing to say, just stop
    try:
        engine = pyttsx3.init()  # Start the text-to-speech engine
        engine.say(text)  # Tell the engine what to say
        engine.runAndWait()  # Make it actually speak out loud
    except Exception as e:
        print(f"Error with text-to-speech: {e}")

def playgifwithtts(gif_path: str, tts_text: str = ""):
    """Play an animated GIF and optionally speak text at the same time.

    Args:
        gif_path: Path to the GIF file.
        tts_text: Optional text to speak via TTS while the GIF plays.
    """
    try:
        # If there's text to say, start talking in the background
        # (so the window doesn't freeze while talking)
        if tts_text:
            threading.Thread(target=playtts, args=(tts_text,), daemon=True).start()

        # Open the GIF file
        im = Image.open(gif_path)
        # Get all the frames (pictures) from the GIF so we can animate them
        frames = [ImageTk.PhotoImage(frame.convert("RGBA")) for frame in ImageSequence.Iterator(im)]
        # How long to show each frame (in milliseconds)
        durations = im.info.get("duration", 100)

        # Make a new window
        root = tk.Tk()
        root.title("Sketchbook Friend")  # Give the window a cute name
        lbl = tk.Label(root)  # This label will show our animation
        lbl.pack()

        # This function changes the picture every few milliseconds to make the animation
        def animate(i=0):
            lbl.config(image=frames[i])  # Show the current frame
            # Wait a bit, then show the next frame (loops back to start)
            root.after(durations, lambda: animate((i+1) % len(frames)))

        animate(0)  # Start the animation!
        root.mainloop()  # Keep the window open until you close it
    except Exception as e:
        print(f"Error playing GIF or TTS: {e}")
