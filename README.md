# ✨ Spellbound-Sketches
A tiny, magical friend that brings your drawings to life — blink, hop, sing, and tell stories together.

> _“You are about to open a tiny door painted on the last page of your sketchbook…”_

Behind that door lives a walking gallery, a paper bird that reads poems, and a story-friend who loves your drawings more than anything. Every color you choose, every wish you whisper, changes the tale. This is a place where sketches come alive — where cozy afternoons and silly adventures live on the same page.

So grab your pencils, pick a voice for your story-friend (cheerful, calm, or curious), and get ready to make something only you could invent.

Turn the page. Whisper your first wish. Let the sketchbook door open.

---

## 🧪 What Is This?

A tiny Python prototype that turns your drawing into a living story.

It:
- Accepts a photo of your sketch and three onboarding answers.
- (Mock) calls a multimodal LLM adapter to generate animation keyframes and a short voice line.
- Removes the background, optionally splits the character into parts.
- Renders animated frames using affine transforms.
- Saves a GIF and plays it in a cozy Tkinter window with TTS narration.

---

## 🛠️ Quick Setup

### Requirements

```txt
Pillow>=9.0.0
numpy
opencv-python
pyttsx3
pytest
