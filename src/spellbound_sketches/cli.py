"""Command line interface for creating a simple animated GIF from a drawing."""

import logging
import os
import json
import typer

from spellbound_sketches.adapter import multimodal_plan_for_animation
from spellbound_sketches.preprocess import remove_background, export_parts
from spellbound_sketches.animator import render_animation_from_plan
from spellbound_sketches.player import playgifwithtts

# Set up logging (for messages and errors)
logging.basicConfig(level=logging.INFO)
name = "Spellbound Sketch CLI"
logger = logging.getLogger(name)

# This makes it easy to create command-line commands
app = typer.Typer(pretty_exceptions_enable=False)

def cli_collect_onboarding():
    """Collect a few preferences to personalize the animation."""
    print("Welcome! Three quick questions to make this yours.")
    q1 = input("1) What colors do you like most? (e.g. bright, pastel, dark) [bright]: ").strip()
    if not q1:
        q1 = "bright"
    q2 = input("2) Do you like adventures, cozy tales, or silly jokes? [adventures]: ").strip()
    if not q2:
        q2 = "adventures"
    q3 = input("3) Should the character ask you before acting, or surprise you sometimes? (ask/surprise) [ask]: ").strip()
    if not q3:
        q3 = "ask"
    return {"colors": q1, "tone": q2, "autonomy": q3}

@app.command()
def sketch():
    """Create an animation from a user supplied drawing."""
    print("Sketchbook Animator — quick prototype")
    img_path = input("Path to photo/scan of the drawing (png/jpg) [sample_data/sample_drawing.png]: ").strip()
    if not img_path:
        img_path = "sample_data/sample_drawing.png"
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