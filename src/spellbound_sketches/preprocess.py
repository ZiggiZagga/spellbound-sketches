"""Basic image preprocessing for animation: background removal and naive part export."""

from PIL import Image, ImageOps
import numpy as np
from pathlib import Path
import logging
from typing import Optional, Dict

logger = logging.getLogger("spellbound_sketches.preprocess")

def remove_background(input_path: str | Path, out_path: str | Path = "character.png") -> Optional[str]:
    """Remove (near-)white background and save a transparent PNG.

    Args:
        input_path: Path to the source drawing (RGBA will be used).
        out_path: Output path for the processed PNG.

    Returns:
        The output path on success, or None on failure.
    """
    try:
        # Normalize paths early and avoids mixing str/Path later
        input_path = Path(input_path)
        out_path = Path(out_path)
        img = Image.open(input_path).convert("RGBA")
        arr = np.array(img)
        # This line finds all the pixels that are NOT white (so we keep the character)
        r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]

        
        # Threshold near-white pixels as background
        # Note: 240 is a forgiving cutoff so off-white paper is treated as background
        mask = ~((r>240)&(g>240)&(b>240))  # keep non-white
        arr[:,:,3] = mask.astype(np.uint8)*255  
        res = Image.fromarray(arr)
        res.save(out_path)
        return str(out_path)
    except Exception as e:
        logger.error(f"Error removing background: {e}")
        return None

def export_parts(
    charpng_path: str | Path,
    parts_dir: str | Path = "parts",
    auto: bool = True
) -> Optional[Dict[str, str]]:
    """Naively crop an image into head/body/left_wing/right_wing parts.

    Args:
        charpng_path: Path to the character PNG.
        parts_dir: Directory to write part images into.
        auto: Present for API shape; cropping is always naive here.

    Returns:
        Dict of part names to file paths, or None on failure.
    """
    try:
        # Normalize paths and ensure output directory exists
        charpng_path = Path(charpng_path)
        parts_dir = Path(parts_dir)
        parts_dir.mkdir(parents=True, exist_ok=True)
        img = Image.open(charpng_path).convert("RGBA")
        w, h = img.size

        # Naive heuristic: crop by broad regions (works for centered characters)
        # Learners: tweak these fractions to match your artwork layout
        head = img.crop((int(w*0.35), int(h*0.05), int(w*0.65), int(h*0.35)))
        body = img.crop((int(w*0.25), int(h*0.25), int(w*0.75), int(h*0.75)))
        left_wing = img.crop((0, int(h*0.25), int(w*0.35), int(h*0.6)))
        right_wing = img.crop((int(w*0.65), int(h*0.25), w, int(h*0.6)))

        head_path = parts_dir / "head.png"
        body_path = parts_dir / "body.png"
        left_wing_path = parts_dir / "left_wing.png"
        right_wing_path = parts_dir / "right_wing.png"

        head.save(head_path)
        body.save(body_path)
        left_wing.save(left_wing_path)
        right_wing.save(right_wing_path)

        return {
            "head": str(head_path),
            "body": str(body_path),
            "left_wing": str(left_wing_path),
            "right_wing": str(right_wing_path),
        }
    except Exception as e:
        logger.error(f"Error exporting parts: {e}")
        return None
