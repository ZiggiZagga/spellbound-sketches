import pytest
from spellbound_sketches import adapter

def test_multimodal_plan_for_animation_fallback(monkeypatch):
    # Simulate API raising an error, should fallback to canned plan
    def raise_runtime(*a, **kw):
        raise RuntimeError("API not available")
    monkeypatch.setattr(adapter, "call_multimodal_api", raise_runtime)
    plan = adapter.multimodal_plan_for_animation("fake_path.png", {"colors": "blue"})
    assert isinstance(plan, dict)
    assert "actions" in plan
    assert "sound_text" in plan
    assert plan["sound_text"].startswith("Hello!")

def test_multimodal_plan_for_animation_success(monkeypatch):
    # Simulate API returning a custom plan
    def fake_api(image_path, prompt):
        return {"duration_ms": 100, "fps": 1, "actions": [], "sound_text": "API success!", "variants": {}}
    monkeypatch.setattr(adapter, "call_multimodal_api", fake_api)
    plan = adapter.multimodal_plan_for_animation("fake_path.png", {"colors": "red"})
    assert isinstance(plan, dict)
    assert plan["sound_text"] == "API success!"
