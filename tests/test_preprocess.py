import os
import pytest
from PIL import Image
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from spellbound_sketches import preprocess

def test_remove_background(tmp_path):
    # Create a simple white background image with a black square
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    for x in range(3, 7):
        for y in range(3, 7):
            img.putpixel((x, y), (0, 0, 0, 255))
    input_path = tmp_path / "input.png"
    output_path = tmp_path / "output.png"
    img.save(input_path)
    result = preprocess.remove_background(str(input_path), str(output_path))
    assert result == str(output_path)
    out_img = Image.open(output_path)
    # Check that the center is still black and the corner is transparent
    assert out_img.getpixel((5, 5))[3] == 255
    assert out_img.getpixel((0, 0))[3] == 0

def test_export_parts(tmp_path):
    # Create a simple image
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 255))
    input_path = tmp_path / "char.png"
    img.save(input_path)
    parts_dir = tmp_path / "parts"
    result = preprocess.export_parts(str(input_path), str(parts_dir))
    assert isinstance(result, dict)
    for key in ["head", "body", "left_wing", "right_wing"]:
        assert key in result
        assert os.path.exists(result[key])
