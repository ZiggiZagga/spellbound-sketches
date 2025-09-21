import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from spellbound_sketches import adapter

def test_canned_plan_for_animation():
    plan = adapter.canned_plan_for_animation()
    assert isinstance(plan, dict)
    assert "actions" in plan
    assert "duration_ms" in plan
    assert "fps" in plan
    assert "sound_text" in plan
    assert "variants" in plan

def test_multimodal_plan_for_animation_fallback():
    # Should fallback to canned plan
    plan = adapter.multimodal_plan_for_animation("fake_path.png", {"colors": "blue"})
    assert isinstance(plan, dict)
    assert "actions" in plan
