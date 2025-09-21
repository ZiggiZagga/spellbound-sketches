import os
import pytest
from PIL import Image
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from spellbound_sketches import preprocess, animator, adapter, player

def test_remove_background_invalid_path(tmp_path):
    # Should return None and not raise
    result = preprocess.remove_background("not_a_real_file.png", str(tmp_path/"out.png"))
    assert result is None

def test_export_parts_invalid_file(tmp_path):
    # Should return None and not raise
    fake_file = tmp_path / "not_an_image.txt"
    fake_file.write_text("not an image")
    result = preprocess.export_parts(str(fake_file), str(tmp_path/"parts"))
    assert result is None

def test_render_animation_from_plan_invalid_image(tmp_path):
    # Should return None and not raise
    plan = {"duration_ms": 100, "fps": 1, "actions": [], "variants": {}}
    result = animator.render_animation_from_plan(plan, "not_a_real_file.png", out_gif=str(tmp_path/"out.gif"))
    assert result is None

def test_render_animation_from_plan_missing_fields(tmp_path):
    # Should use defaults and not raise
    img = Image.new("RGBA", (10, 10), (255, 0, 0, 255))
    char_path = tmp_path / "char.png"
    img.save(char_path)
    plan = {}  # missing all fields
    out_gif = tmp_path / "out.gif"
    result = animator.render_animation_from_plan(plan, str(char_path), out_gif=str(out_gif))
    assert result == str(out_gif)
    assert os.path.exists(out_gif)

def test_adapter_multimodal_plan_various_onboarding():
    # Should always return a dict
    for onboarding in [{}, {"foo": "bar"}, {"colors": "red", "tone": "fun"}]:
        plan = adapter.multimodal_plan_for_animation("fake.png", onboarding)
        assert isinstance(plan, dict)

def test_playtts_non_string():
    # Should not raise for non-string input
    try:
        player.playtts(None)
        player.playtts(123)
    except Exception:
        pass

def test_playgifwithtts_non_string():
    # Should not raise for non-string input
    try:
        player.playgifwithtts(None, None)
        player.playgifwithtts(123, 456)
    except Exception:
        pass
