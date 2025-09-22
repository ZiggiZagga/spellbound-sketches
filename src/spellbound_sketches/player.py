
# This file helps us show animated GIFs and lets the computer read text out loud!
# It's a fun way to mix art and storytelling with code.

import tkinter as tk  # tkinter helps us make simple windows and GUIs (Graphical User Interfaces)
from PIL import Image, ImageTk, ImageSequence  # PIL lets us work with images and animations
import threading  # threading lets us do two things at once (like talking and showing pictures)
import pyttsx3  # pyttsx3 is a library that makes the computer talk (Text-to-Speech)
import time


# This function makes the computer say whatever text you give it.
def playtts(text: str):
    if not text:
        return  # If there's nothing to say, just stop
    try:
        engine = pyttsx3.init()  # Start the text-to-speech engine
        engine.say(text)  # Tell the engine what to say
        engine.runAndWait()  # Make it actually speak out loud
    except Exception as e:
        print(f"Error with text-to-speech: {e}")


# This function shows an animated GIF and (optionally) speaks some text at the same time!
# gifpath: where your GIF file is saved
# tts_text: what you want the computer to say (can be empty)
def playgifwithtts(gif_path: str, tts_text: str = ""):
    try:
        # If there's text to say, start talking in the background
        # (so the window doesn't freeze while talking)
        if tts_text:
            threading.Thread(target=playtts, args=(tts_text,), daemon=True).start()

        # Make a new window FIRST (must exist before creating PhotoImage)
        root = tk.Tk()
        root.title("Sketchbook Friend")  # Give the window a cute name
        lbl = tk.Label(root)  # This label will show our animation
        lbl.pack()

        # Open the GIF file
        im = Image.open(gif_path)
        # Get all the frames (pictures) from the GIF so we can animate them
        frames = [ImageTk.PhotoImage(frame.convert("RGBA"), master=root) for frame in ImageSequence.Iterator(im)]
        # How long to show each frame (in milliseconds)
        durations = im.info.get("duration", 100)

        # This function changes the picture every few milliseconds to make the animation
        def animate(i:int=0):
            lbl.config(image=frames[i])  # Show the current frame
            # Wait a bit, then show the next frame (loops back to start)
            root.after(durations, lambda: animate((i+1) % len(frames)))

        animate(0)  # Start the animation!
        root.mainloop()  # Keep the window open until you close it
    except Exception as e:
        print(f"Error playing GIF or TTS: {e}")
