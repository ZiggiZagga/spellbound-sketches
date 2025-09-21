def removebackground(inputpath: str, out_path: str = "character.png"):
def exportparts(charpngpath: str, partsdir="parts", auto=True):

# This file helps us get drawings ready for animation!
# It can remove the background from a picture and split it into parts (like head, body, wings).

from PIL import Image, ImageOps
import numpy as np
import os

# This function removes the white background from a drawing, so only the character is left.
def removebackground(input_path: str, out_path: str = "character.png"):
    img = Image.open(input_path).convert("RGBA")
    arr = np.array(img)
    # This line finds all the pixels that are NOT white (so we keep the character)
    r, g, b, a = arr[:,:,0], arr[:,:,1], arr[:,:,2], arr[:,:,3]
    mask = ~((r>240)&(g>240)&(b>240))  # keep non-white
    arr[:,:,3] = mask.astype(np.uint8)*255  # Make background transparent
    res = Image.fromarray(arr)
    res.save(out_path)
    return out_path

# This function tries to split the character into parts (head, body, wings) by cropping the image.
# It's a simple guess, but it works for basic drawings!
def exportparts(charpng_path: str, parts_dir="parts", auto=True):
    """
    Quick trick: create body/head/leftwing/rightwing by cropping the image into sections.
    For a real project, you might want to use a smarter method or do it by hand.
    """
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
        "leftwing": os.path.join(parts_dir, "left_wing.png"),
        "rightwing": os.path.join(parts_dir, "right_wing.png"),
    }
