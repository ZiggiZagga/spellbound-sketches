"""Render animated GIFs from a simple action plan.

This module reads a base character image and an action plan (translate,
scale, swap_image) and produces a GIF. It also includes small helpers
for interpolation and easing.
"""

from PIL import Image
import numpy as np
from pathlib import Path
import math
import logging
from typing import Optional, Dict, Any

logger = logging.getLogger("spellbound_sketches.animator")

def lerp(a: float, b: float, t: float) -> float:
    """Linearly interpolate between two values."""
    return a + (b - a) * t

def ease_out(t: float) -> float:
    """Ease-out function: start fast, end slow."""
    return 1 - (1 - t) * (1 - t)

def render_animation_from_plan(
    plan: Dict[str, Any],
    char_png: str | Path,
    parts_dir: Optional[str | Path] = None,
    out_gif: str | Path = "out.gif"
) -> Optional[str]:
    """Render an animated GIF from a plan and a base character image.

    The plan may include:
      - "duration_ms": total animation duration in milliseconds
      - "fps": frames per second
      - "actions": a list of actions with keys such as:
          * type: "translate" | "scale" | "swap_image"
          * part: "root" or a specific part for swapping
          * start_frame, end_frame: frame range for the action
          * start_offset/end_offset, start_scale/end_scale, easing, variant
      - "variants": mapping of variant names to image file paths

    Args:
        plan: Dictionary describing timing, actions, and optional variants.
        char_png: Path to the main character PNG (RGBA recommended).
        parts_dir: Optional directory containing extra part images.
        out_gif: Output path for the rendered GIF.

    Returns:
        The output GIF path on success, or None if rendering fails.
    """

    try:
        char_png = Path(char_png)
        if parts_dir is not None:
            parts_dir = Path(parts_dir)
        out_gif = Path(out_gif)
        # Get how long the animation should be and how smooth (frames per second)
        duration_ms = plan.get("duration_ms", 1000)
        fps = plan.get("fps", 12)
        total_frames = max(1, int(duration_ms / 1000 * fps))
        base = Image.open(char_png).convert("RGBA")
        w, h = base.size
        frames = []

        # Load extra parts if we have them (like head, wings)
        parts = {}
        if parts_dir and parts_dir.is_dir():
            for name in ("body", "head", "leftwing", "rightwing"):
                p = parts_dir / f"{name}.png"
                if p.exists():
                    parts[name] = Image.open(p).convert("RGBA")

        # This helper puts everything together for each frame
        def compose_frame(offset=(0,0), scale=(1.0,1.0), head_img=None, extra_overlay=None):
            """Build a single frame with optional transforms and overlays."""

            canvas = Image.new("RGBA", base.size, (255,255,255,0))
            # Resize the character for scaling
            sw = int(base.width * scale[0])
            sh = int(base.height * scale[1])
            base_resized = base.resize((sw, sh), resample=Image.BICUBIC)
            x = (w - sw)//2 + offset[0]
            y = (h - sh)//2 + offset[1]
            canvas.paste(base_resized, (int(x), int(y)), base_resized)

            # If we have a special head image, put it on top
            if head_img is not None and "head" in parts:
                canvas.paste(head_img, ((w - head_img.width)//2, (h - head_img.height)//2 - 20), head_img)
            # Add any extra overlays
            if extra_overlay:
                canvas.paste(extra_overlay, (0,0), extra_overlay)
            return canvas

        # Load any special images (like eyes closed) from the plan
        variants = {}
        for k, v in plan.get("variants", {}).items():
            v_path = Path(v)
            if v_path.exists():
                variants[k] = Image.open(v_path).convert("RGBA")

        # For each frame, figure out what should move or change
        for f in range(total_frames):
            offset = [0,0]
            scale = [1.0,1.0]
            head_variant = None
            for act in plan.get("actions", []):
                sf, ef = act.get("start_frame", 0), act.get("end_frame", total_frames)
                if f < sf or f > ef:
                    continue
                t_norm = (f - sf) / max(1, (ef - sf))
                easing = act.get("easing")
                if easing == "ease_out":
                    t = ease_out(t_norm)
                else:
                    t = t_norm
                if act["type"] == "translate" and act.get("part") == "root":
                    so = act.get("start_offset", [0,0])
                    eo = act.get("end_offset", [0,0])
                    offset[0] += int(lerp(so[0], eo[0], t))
                    offset[1] += int(lerp(so[1], eo[1], t))
                if act["type"] == "scale" and act.get("part") == "root":
                    ss = act.get("start_scale", [1.0,1.0])
                    es = act.get("end_scale", [1.0,1.0])
                    scale[0] *= lerp(ss[0], es[0], t)
                    scale[1] *= lerp(ss[1], es[1], t)
                if act["type"] == "swap_image" and act.get("variant"):
                    vname = act["variant"]
                    if vname in variants:
                        head_variant = variants[vname]
            frame = compose_frame(offset=tuple(offset), scale=tuple(scale), head_img=head_variant)
            frames.append(frame.convert("RGBA"))

        # Save all the frames as a GIF (animation)
        frames[0].save(out_gif, saveall=True, append_images=frames[1:], duration=int(1000/fps), loop=0, disposal=2)
        return str(out_gif)
    except Exception as e:
        logger.error(f"Error rendering animation: {e}")
        return None
