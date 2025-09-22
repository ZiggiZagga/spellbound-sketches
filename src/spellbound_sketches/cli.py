"""Command line interface for creating a simple animated GIF from a drawing."""

import logging
import json
import typer
from pathlib import Path

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

def cli_collect_onboarding() -> dict:
    """Collect preferences to personalize the animation, including age group and more."""
    logger.info("Welcome! Let's personalize your animation experience.")
    print("\n--- Onboarding ---")
    print("Choose your age group for a tailored experience:")
    print("  1) Young child (5-8)")
    print("  2) Older child (9-12)")
    print("  3) Teen/Adult")
    age_group = input("Select age group [1/2/3, default 1]: ").strip()
    if age_group not in {"1", "2", "3"}:
        age_group = "1"

    # Presets for each age group
    presets = {
        "1": {"colors": "bright", "tone": "silly", "autonomy": "ask", "difficulty": "easy"},
        "2": {"colors": "pastel", "tone": "adventures", "autonomy": "surprise", "difficulty": "medium"},
        "3": {"colors": "dark", "tone": "cozy tales", "autonomy": "surprise", "difficulty": "advanced"},
    }
    preset = presets[age_group]

    print("\nYou can customize your experience or press Enter to use the suggested preset.")
    q1 = input(f"1) Favorite colors? (e.g. bright, pastel, dark) [{preset['colors']}]: ").strip()
    if not q1:
        q1 = preset["colors"]
    q2 = input(f"2) Story style? (adventures, cozy tales, silly jokes) [{preset['tone']}]: ").strip()
    if not q2:
        q2 = preset["tone"]
    q3 = input(f"3) Should the character ask before acting, or surprise you? (ask/surprise) [{preset['autonomy']}]: ").strip()
    if not q3:
        q3 = preset["autonomy"]
    q4 = input(f"4) Animation difficulty? (easy, medium, advanced) [{preset['difficulty']}]: ").strip()
    if not q4:
        q4 = preset["difficulty"]
    q5 = input("5) Would you like sound effects? (yes/no) [yes]: ").strip().lower()
    if not q5:
        q5 = "yes"

    onboarding = {
        "age_group": age_group,
        "colors": q1,
        "tone": q2,
        "autonomy": q3,
        "difficulty": q4,
        "sound_effects": q5 == "yes"
    }
    print("\nThank you! Your preferences are saved.\n")
    return onboarding

@app.command()
def sketch() -> None:
    """Create an animation from a user supplied drawing."""
    logger.info("Sketchbook Animator — quick prototype")
    print("\n--- Image Selection ---")
    print("Tip: You can use your own drawing (PNG/JPG) or just press Enter to use the sample.")
    img_path = input("Path to photo/scan of the drawing [sample_data/sample_drawing.png]: ").strip()
    if not img_path:
        img_path = "sample_data/sample_drawing.png"
    img_path = Path(img_path)
    onboarding = cli_collect_onboarding()

    logger.info("Preprocessing image (removing background)...")
    print("\n[Info] Removing background from your image...")
    charpng = remove_background(img_path, out_path=Path("character.png"))
    if not charpng:
        print("[Error] Failed to preprocess image. Please check the file path and format.")
        logger.error("Failed to preprocess image. Exiting.")
        return

    logger.info("Optional: export parts for better puppeting (head, body, leftwing, rightwing).")
    print("[Info] Exporting character parts for animation...")
    parts_dir = Path("parts")
    parts = export_parts(charpng, parts_dir=parts_dir, auto=True)  # returns dict or None
    if parts is None:
        print("[Warning] Could not export parts. Continuing with main image only.")
        logger.warning("Could not export parts. Continuing with main image only.")

    logger.info("Requesting animation plan from multimodal adapter...")
    print("[Info] Requesting animation plan from the AI...")
    plan = multimodal_plan_for_animation(image_path=charpng, onboarding=onboarding)

    # --- Animation Plan Preview Step ---
    while True:
        print("\n[Preview] Here is your animation plan:")
        print(json.dumps(plan, indent=2))
        print("Options:")
        print("  [a] Accept and render animation")
        print("  [e] Edit plan (duration/fps/actions)")
        print("  [r] Randomize/regenerate plan")
        print("  [q] Quit")
        choice = input("What would you like to do? [a/e/r/q]: ").strip().lower()
        if choice in {"a", ""}:
            break
        elif choice == "e":
            # Editing will be implemented in the next step
            print("[Edit] Editing not yet implemented. Please choose another option.")
        elif choice == "r":
            print("[Info] Regenerating animation plan...")
            plan = multimodal_plan_for_animation(image_path=charpng, onboarding=onboarding)
        elif choice == "q":
            print("[Info] Exiting without rendering.")
            return
        else:
            print("[Warning] Invalid option. Please choose again.")

    logger.info("Rendering animation frames...")
    print("[Info] Rendering animation frames...")
    gifpath = render_animation_from_plan(plan, charpng, parts_dir=parts_dir)
    if not gifpath:
        print("[Error] Failed to render animation. Please check your image and try again.")
        logger.error("Failed to render animation. Exiting.")
        return
    print(f"[Success] Saved GIF to {gifpath}")
    logger.info(f"Saved GIF to {gifpath}")

    logger.info("Playing animation with short voice line...")
    print("[Info] Playing animation with voice line...")
    try:
        playgifwithtts(gifpath, plan.get("sound_text", ""))
    except Exception as e:
        print(f"[Error] Could not play animation or TTS: {e}")
        logger.error(f"Error playing animation or TTS: {e}")


# This lets you run the app by typing 'python cli.py' in the terminal
if __name__ == "__main__":
    app()