
"""Display animated GIFs and optionally speak accompanying text (TTS)."""

import tkinter as tk  # tkinter helps us make simple windows and GUIs (Graphical User Interfaces)
from PIL import Image, ImageTk, ImageSequence  # PIL lets us work with images and animations
import threading  # threading lets us do two things at once (like talking and showing pictures)
import pyttsx3  # pyttsx3 is a library that makes the computer talk (Text-to-Speech)
import time
import logging
from typing import Optional

logger = logging.getLogger("spellbound_sketches.player")

def playtts(text: Optional[str]) -> None:
    """Speak the given text using the system TTS engine."""
    if not text:
        return  # If there's nothing to say, just stop
    try:
        engine = pyttsx3.init()  # Start the text-to-speech engine
        engine.say(text)  # Tell the engine what to say
        engine.runAndWait()  # Make it actually speak out loud
    except Exception as e:
        logger.error(f"Error with text-to-speech: {e}")

def playgifwithtts(gif_path: str, tts_text: Optional[str] = "") -> None:
    """Play an animated GIF and optionally speak text at the same time.

    Args:
        gif_path: Path to the GIF file.
        tts_text: Optional text to speak via TTS while the GIF plays.
    """
    # Always show a window, even if error occurs
    root = tk.Tk()
    root.title("Sketchbook Friend")
    lbl = tk.Label(root)
    lbl.pack()
    # Show loading indicator
    lbl.config(text="Loading animation...", image="")
    root.update()
    try:
        # If there's text to say, start talking in the background
        # Why: threading keeps the UI responsive while TTS runs
        if tts_text:
            threading.Thread(target=playtts, args=(tts_text,), daemon=True).start()

        # Open the GIF file
        im = Image.open(gif_path)

        # Keep PhotoImage objects alive by storing them in a list
        # Note: master=root ties their lifecycle to the window
        frames = [ImageTk.PhotoImage(frame.convert("RGBA"), master=root) for frame in ImageSequence.Iterator(im)]

        # Duration can be an int or per-frame; this code uses a single value
        durations = im.info.get("duration", 100)

        # Advance frames on the Tk event loop timer
        def animate(i=0):
            lbl.config(image=frames[i], text="")
            root.after(durations, lambda: animate((i+1) % len(frames)))

        animate(0)
    except Exception as e:
        logger.error(f"Error playing GIF or TTS: {e}")
        # Show a friendly error in the same window
        lbl.config(text=f"Error: Could not play animation.\n{e}", image="")
    root.mainloop()
