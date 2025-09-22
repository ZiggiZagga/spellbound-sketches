import os
import pytest
from PIL import Image
import tempfile
import shutil
from spellbound_sketches import preprocess

def test_remove_background_large_image():
    # Create a large white background image with a black square
    img = Image.new("RGBA", (2048, 2048), (255, 255, 255, 255))
    for x in range(900, 1150):
        for y in range(900, 1150):
            img.putpixel((x, y), (0, 0, 0, 255))
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "large_input.png")
        output_path = os.path.join(tmpdir, "large_output.png")
        img.save(input_path)
        result = preprocess.remove_background(input_path, output_path)
        assert result == output_path
        out_img = Image.open(output_path)
        assert out_img.getpixel((1024, 1024))[3] == 255  # center is black
        assert out_img.getpixel((0, 0))[3] == 0  # corner is transparent

def test_remove_background_permission_error(monkeypatch):
    # Simulate permission error on output
    img = Image.new("RGBA", (10, 10), (255, 255, 255, 255))
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "input.png")
        output_path = os.path.join(tmpdir, "output.png")
        img.save(input_path)
        def raise_permission(*a, **kw):
            raise PermissionError("No write access")
        monkeypatch.setattr("PIL.Image.Image.save", raise_permission)
        result = preprocess.remove_background(input_path, output_path)
        assert result is None

def test_export_parts_invalid_dir(monkeypatch):
    # Simulate error when creating directory
    img = Image.new("RGBA", (100, 100), (0, 0, 0, 255))
    with tempfile.TemporaryDirectory() as tmpdir:
        input_path = os.path.join(tmpdir, "char.png")
        img.save(input_path)
        def raise_oserror(*a, **kw):
            raise OSError("Cannot create directory")
        monkeypatch.setattr("pathlib.Path.mkdir", raise_oserror)
        result = preprocess.export_parts(input_path, parts_dir=os.path.join(tmpdir, "parts"))
        assert result is None

def test_export_parts_invalid_image():
    # Try to export parts from a non-image file
    with tempfile.TemporaryDirectory() as tmpdir:
        fake_file = os.path.join(tmpdir, "not_an_image.txt")
        with open(fake_file, "w") as f:
            f.write("not an image")
        result = preprocess.export_parts(fake_file, parts_dir=os.path.join(tmpdir, "parts"))
        assert result is None
