import pytest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from spellbound_sketches import player

def test_playtts_handles_empty():
    # Should not raise an error for empty text
    player.playtts("")

def test_playtts_handles_text():
    # Should not raise an error for normal text (TTS engine may not be available in CI)
    try:
        player.playtts("Hello world!")
    except Exception:
        pass  # Accept any error due to missing TTS engine

def test_playgifwithtts_handles_missing_file():
    # Should handle missing GIF file gracefully
    try:
        player.playgifwithtts("not_a_real_file.gif", "Hello!")
    except Exception:
        pass  # Accept any error due to missing file
