def clicollectonboarding():

# This file lets you use the project from the command line (like a little program you run in the terminal)
# It guides you through making your own animated character from a drawing!

import logging
import os
import json
import typer

from adapter import multimodal_plan_for_animation
from preprocess import remove_background, export_parts
from animator import render_animation_from_plan
from player import playgifwithtts

# Set up logging (for messages and errors)
logging.basicConfig(level=logging.INFO)
name = "Spellbound Sketch CLI"
logger = logging.getLogger(name)

# This makes it easy to create command-line commands
app = typer.Typer(pretty_exceptions_enable=False)

# This function asks the user a few questions to personalize the experience
def cli_collect_onboarding():
    print("Welcome! Three quick questions to make this yours.")
    q1 = input("1) What colors do you like most? (e.g. bright, pastel, dark): ").strip()
    q2 = input("2) Do you like adventures, cozy tales, or silly jokes? ").strip()
    q3 = input("3) Should the character ask you before acting, or surprise you sometimes? (ask/surprise): ").strip()
    return {"colors": q1, "tone": q2, "autonomy": q3}

# This is the main command to create an animation from your drawing!
@app.command()
def sketch():
    print("Sketchbook Animator — quick prototype")
    img_path = input("Path to photo/scan of the drawing (png/jpg): ").strip()
    if not img_path:
        print("No image path provided. Exiting.")
        return
    onboarding = cli_collect_onboarding()

    print("Preprocessing image (removing background)...")
    charpng = remove_background(img_path, out_path="character.png")
    if not charpng:
        print("Failed to preprocess image. Exiting.")
        return

    print("Optional: export parts for better puppeting (head, body, leftwing, rightwing).")
    parts = export_parts(charpng, parts_dir="parts", auto=True)  # returns dict or None
    if parts is None:
        print("Warning: Could not export parts. Continuing with main image only.")

    print("Requesting animation plan from multimodal adapter...")
    plan = multimodal_plan_for_animation(image_path=charpng, onboarding=onboarding)
    print("Plan received:")
    print(json.dumps(plan, indent=2))

    print("Rendering animation frames...")
    gifpath = render_animation_from_plan(plan, charpng, parts_dir="parts")
    if not gifpath:
        print("Failed to render animation. Exiting.")
        return
    print(f"Saved GIF to {gifpath}")

    print("Playing animation with short voice line...")
    try:
        playgifwithtts(gifpath, plan.get("sound_text", ""))
    except Exception as e:
        print(f"Error playing animation or TTS: {e}")


# This lets you run the app by typing 'python cli.py' in the terminal
if __name__ == "__main__":
    app()
