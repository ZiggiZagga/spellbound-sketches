
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
    # Tooltip/help label
    help_lbl = tk.Label(root, text="Tip: You can close this window at any time. Drag and drop a new GIF/PNG to reload.", fg="gray")
    help_lbl.pack()
    # Show loading indicator
    lbl.config(text="Loading animation...", image="")
    root.update()

    def load_and_play_image(path):
        try:
            # If there's text to say, start talking in the background
            if tts_text:
                threading.Thread(target=playtts, args=(tts_text,), daemon=True).start()

            im = Image.open(path)
            frames = [ImageTk.PhotoImage(frame.convert("RGBA"), master=root) for frame in ImageSequence.Iterator(im)]
            durations = im.info.get("duration", 100)

            def animate(i=0):
                lbl.config(image=frames[i], text="")
                root.after(durations, lambda: animate((i+1) % len(frames)))

            animate(0)
            help_lbl.config(text="Tip: Drag and drop a new GIF/PNG to reload.", fg="gray")
        except Exception as e:
            logger.error(f"Error playing GIF or TTS: {e}")
            lbl.config(text=f"Error: Could not play animation.\n{e}", image="")
            help_lbl.config(text="Help: Make sure your image is a valid GIF or PNG and try again.", fg="red")

    # Drag-and-drop support (Windows, Linux, macOS)
    def on_drop(event):
        # event.data may contain file path(s)
        path = event.data if hasattr(event, 'data') else event.widget.tk.splitlist(event.data)[0]
        if path and (path.endswith('.gif') or path.endswith('.png')):
            lbl.config(text="Loading animation...", image="")
            root.update()
            load_and_play_image(path)
    try:
        # TkinterDnD2 is a common cross-platform drag-and-drop extension
        try:
            from tkinterdnd2 import DND_FILES, TkinterDnD
            root.destroy()
            root = TkinterDnD.Tk()
            root.title("Sketchbook Friend")
            lbl = tk.Label(root)
            lbl.pack()
            help_lbl = tk.Label(root, text="Tip: You can close this window at any time. Drag and drop a new GIF/PNG to reload.", fg="gray")
            help_lbl.pack()
            lbl.drop_target_register(DND_FILES)
            lbl.dnd_bind('<<Drop>>', on_drop)
        except ImportError:
            # Fallback: try to use native Tkinter drag-and-drop (limited)
            lbl.bind('<Drag>', lambda e: None)
            lbl.bind('<Drop>', on_drop)
        load_and_play_image(gif_path)
    except Exception as e:
        logger.error(f"Error initializing drag-and-drop: {e}")
        lbl.config(text=f"Error: Could not initialize drag-and-drop.\n{e}", image="")
        help_lbl.config(text="Help: Try installing tkinterdnd2 for drag-and-drop support.", fg="red")
    root.mainloop()
