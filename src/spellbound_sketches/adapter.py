"""Adapter module for generating animation plans.

This file acts as a translator between the code and a multimodal AI
(e.g., ChatGPT-like system that can handle images and text). For now,
it provides a placeholder API call and a canned (pretend) animation
plan for testing purposes.
"""

import json
import base64
from typing import Dict, Any

def call_multimodal_api(image_path: str, prompt: str) -> Dict[str, Any]:
    """Placeholder for a real multimodal API call.

    Args:
        image_path: Path to the input drawing.
        prompt: Text prompt describing the desired animation.

    Returns:
        A dictionary representing the animation plan.

    Raises:
        RuntimeError: Always, since no real API is implemented yet.
    """
    # Note: In production this would serialize the image + prompt,
    # send it to a model endpoint, and parse the JSON response.
    raise RuntimeError("TODO: No real multimodal API configured. Use fallback or implement API call here.")

def canned_plan_for_animation() -> Dict[str, Any]:
    """Return a fake animation plan for testing."""

    # Why this exists:
    # It lets us test the entire animation pipeline without needing an actual AI. This "stub" mimics the structure of a real plan.
    return {
        "duration_ms": 1200,  # How long the animation lasts (in milliseconds)
        "fps": 12,  # Frames per second (how smooth the animation is)

        # Actions describe *what changes* over time.
        "actions": [
            # swap_image replaces the head with a variant (eyes closed)
            {
                "name": "blink",
                "part": "head",
                "start_frame": 2,
                "end_frame": 4,
                "type": "swap_image",  # Tells the animator to swap to a different image (like eyes closed)
                "variant": "eyes_closed"
            },
            # translate moves the root of the character upward
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
            # scale: squash-and-stretch effect
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

        # The AI could also generate speech lines for TTS playback.
        "sound_text": "Hello! I am your sketch friend. Let's play!",  # What the character will say

        # Variants map to extra image assets (like alternate poses).
        "variants": {
            "eyes_closed": "variants/eyesclosed.png"  # Extra images for the animation
        }
    }

def multimodal_plan_for_animation(image_path: str, onboarding: Dict[str, Any]) -> Dict[str, Any]:
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
    # The prompt is written to teach the AI what kind of JSON structure we expect back (schema guidance).
    prompt = f"Given this drawing and onboarding {onboarding}, propose a short animation plan (JSON): actions with part, timing in frames, transforms, and a short sound_text."
    try:
        res = call_multimodal_api(image_path, prompt)
        return res
    except Exception:
        plan = canned_plan_for_animation()
        return plan
