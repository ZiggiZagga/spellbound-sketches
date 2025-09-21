import os
import pytest
from PIL import Image
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from spellbound_sketches import animator

def test_render_animation_from_plan(tmp_path):
    # Create a simple plan
    plan = {
        "duration_ms": 200,
        "fps": 2,
        "actions": [
            {"type": "translate", "part": "root", "start_frame": 0, "end_frame": 1, "start_offset": [0, 0], "end_offset": [2, 2]},
        ],
        "variants": {}
    }
    # Create a simple character image
    char_path = tmp_path / "char.png"
    img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))
    img.save(char_path)
    out_gif = tmp_path / "out.gif"
    result = animator.render_animation_from_plan(plan, str(char_path), out_gif=str(out_gif))
    assert result == str(out_gif)
    assert os.path.exists(out_gif)
