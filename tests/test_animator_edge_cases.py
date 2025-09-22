import pytest
import tempfile
import os
from spellbound_sketches import animator
from PIL import Image

def test_render_animation_from_plan_invalid_gif_path(monkeypatch):
    # Simulate error when saving GIF
    plan = {"duration_ms": 100, "fps": 1, "actions": [], "variants": {}}
    img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))
    with tempfile.TemporaryDirectory() as tmpdir:
        char_path = os.path.join(tmpdir, "char.png")
        img.save(char_path)
        out_gif = os.path.join(tmpdir, "out.gif")
        def raise_permission(*a, **kw):
            raise PermissionError("No write access")
        monkeypatch.setattr("PIL.Image.Image.save", raise_permission)
        result = animator.render_animation_from_plan(plan, char_path, out_gif=out_gif)
        assert result is None

def test_render_animation_from_plan_large_image():
    # Render animation for a large image
    plan = {"duration_ms": 100, "fps": 1, "actions": [], "variants": {}}
    img = Image.new("RGBA", (1024, 1024), (255, 0, 0, 255))
    with tempfile.TemporaryDirectory() as tmpdir:
        char_path = os.path.join(tmpdir, "char.png")
        img.save(char_path)
        out_gif = os.path.join(tmpdir, "out.gif")
        result = animator.render_animation_from_plan(plan, char_path, out_gif=out_gif)
        assert result == out_gif
        assert os.path.exists(out_gif)
