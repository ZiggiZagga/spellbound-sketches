
import pytest
import tempfile
import os
import sys
from spellbound_sketches import player

import tkinter

def test_playtts_permission_error(monkeypatch):
    # Simulate error in TTS engine
    def raise_permission(*a, **kw):
        raise PermissionError("No audio device")
    monkeypatch.setattr("pyttsx3.init", raise_permission)
    player.playtts("Hello!")  # Should not raise

@pytest.mark.skipif(
    not os.environ.get("DISPLAY") and sys.platform != "win32",
    reason="No display available for Tkinter GUI tests."
)
def test_playgifwithtts_invalid_gif(monkeypatch):
    # Simulate error when opening GIF
    def raise_ioerror(*a, **kw):
        raise IOError("Cannot open file")
    monkeypatch.setattr("PIL.Image.open", raise_ioerror)
    player.playgifwithtts("not_a_real_file.gif", "Hello!")  # Should not raise
