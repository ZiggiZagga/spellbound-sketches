"""Adapter module for generating animation plans.

This file acts as a translator between the code and a multimodal AI
(e.g., ChatGPT-like system that can handle images and text). For now,
it provides a placeholder API call and a canned (pretend) animation
plan for testing purposes.
"""

import json
import base64

def call_multimodal_api(image_path: str, prompt: str) -> dict:
    """Placeholder for a real multimodal API call.

    Args:
        image_path: Path to the input drawing.
        prompt: Text prompt describing the desired animation.

    Returns:
        A dictionary representing the animation plan.

    Raises:
        RuntimeError: Always, since no real API is implemented yet.
    """
    raise RuntimeError("TODO: No real multimodal API configured. Use fallback or implement API call here.")

def canned_plan_for_animation():
    """Return a fake animation plan for testing."""

    return {
        "duration_ms": 1200,  # How long the animation lasts (in milliseconds)
        "fps": 12,  # Frames per second (how smooth the animation is)
        "actions": [
            {
                "name": "blink",
                "part": "head",
                "start_frame": 2,
                "end_frame": 4,
                "type": "swap_image",  # Tells the animator to swap to a different image (like eyes closed)
                "variant": "eyes_closed"
            },
            {
                "name": "hop",
                "part": "root",
                "start_frame": 4,
                "end_frame": 8,
                "type": "translate",
                "start_offset": [0, 0],
                "end_offset": [0, -20],
                "easing": "ease_out"
            },
            {
                "name": "squash",
                "part": "root",
                "start_frame": 8,
                "end_frame": 10,
                "type": "scale",
                "start_scale": [1.0, 1.0],
                "end_scale": [1.05, 0.9]
            }
        ],
        "sound_text": "Hello! I am your sketch friend. Let's play!",  # What the character will say
        "variants": {
            "eyes_closed": "variants/eyesclosed.png"  # Extra images for the animation
        }
    }

def multimodal_plan_for_animation(image_path: str, onboarding: dict) -> dict:
    """Get an animation plan using a multimodal AI or fallback.

    Attempts to call the real multimodal API with the given drawing
    and onboarding details. If the API is unavailable or raises an error,
    falls back to the canned plan.

    Args:
        image_path: Path to the input drawing.
        onboarding: Extra onboarding details to include in the prompt.

    Returns:
        A dictionary representing the animation plan.
    """
    
    prompt = f"Given this drawing and onboarding {onboarding}, propose a short animation plan (JSON): actions with part, timing in frames, transforms, and a short sound_text."
    try:
        res = call_multimodal_api(image_path, prompt)
        return res
    except Exception:
        plan = canned_plan_for_animation()
        return plan
