"""Basic image preprocessing for animation: background removal and naive part export."""

from PIL import Image, ImageOps
import numpy as np
import os

def remove_background(input_path: str, out_path: str = "character.png"):
    """Remove (near-)white background and save a transparent PNG.

    Args:
        input_path: Path to the source drawing (RGBA will be used).
        out_path: Output path for the processed PNG.

    Returns:
        The output path on success, or None on failure.
    """
    try:
        img = Image.open(input_path).convert("RGBA")
        arr = np.array(img)
        # This line finds all the pixels that are NOT white (so we keep the character)
        r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
        mask = ~((r>240)&(g>240)&(b>240))  # keep non-white
        arr[:,:,3] = mask.astype(np.uint8)*255  # Make background transparent
        res = Image.fromarray(arr)
        res.save(out_path)
        return out_path
    except Exception as e:
        print(f"Error removing background: {e}")
        return None

def export_parts(charpng_path: str, parts_dir="parts", auto=True):
    """Naively crop an image into head/body/left_wing/right_wing parts.

    Args:
        charpng_path: Path to the character PNG.
        parts_dir: Directory to write part images into.
        auto: Present for API shape; cropping is always naive here.

    Returns:
        Dict of part names to file paths, or None on failure.
    """
    try:
        os.makedirs(parts_dir, exist_ok=True)
        img = Image.open(charpng_path).convert("RGBA")
        w, h = img.size
        # Split the image into parts using simple math (thirds of the image)
        head = img.crop((int(w*0.35), int(h*0.05), int(w*0.65), int(h*0.35)))
        body = img.crop((int(w*0.25), int(h*0.25), int(w*0.75), int(h*0.75)))
        left_wing = img.crop((0, int(h*0.25), int(w*0.35), int(h*0.6)))
        right_wing = img.crop((int(w*0.65), int(h*0.25), w, int(h*0.6)))

        head.save(os.path.join(parts_dir, "head.png"))
        body.save(os.path.join(parts_dir, "body.png"))
        left_wing.save(os.path.join(parts_dir, "left_wing.png"))
        right_wing.save(os.path.join(parts_dir, "right_wing.png"))

        return {
            "head": os.path.join(parts_dir, "head.png"),
            "body": os.path.join(parts_dir, "body.png"),
            "left_wing": os.path.join(parts_dir, "left_wing.png"),
            "right_wing": os.path.join(parts_dir, "right_wing.png"),
        }
    except Exception as e:
        print(f"Error exporting parts: {e}")
        return None
