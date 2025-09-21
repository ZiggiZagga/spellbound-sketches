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
```

# 🧰 Why We Need These Python Libraries

Here’s what each library does and why it’s part of our story:

---

## 🖼️ Pillow — The Image Artist

**What it does:**  
Pillow helps us open, edit, and save images.

**Why we need it:**  
When you upload your drawing, Pillow lets us:
- Remove the background (so your character can move freely!)
- Cut it into parts (like head, wings, body)
- Save new versions of your drawing

**Imagine:**  
You’re holding a digital paintbrush that can crop, clean, and transform your sketch.

---

## 🔢 NumPy — The Math Wizard

**What it does:**  
NumPy handles numbers and data super fast.

**Why we need it:**  
Images are made of pixels (tiny dots of color). NumPy helps us:
- Read those pixels as numbers
- Decide which parts are background and which are your drawing
- Do quick calculations for animation (like moving or stretching parts)

**Imagine:**  
A super-smart calculator that speaks the language of pictures.

---

## 🎥 OpenCV — The Vision Expert

**What it does:**  
OpenCV works with images and videos.

**Why we need it:**  
OpenCV helps us:
- Detect shapes and edges
- Prepare your drawing for animation
- (Later) do fancy things like tracking movement or adding effects

**Imagine:**  
A robot eye that understands your drawing and helps it move.

---

## 🗣️ pyttsx3 — The Voice Box

**What it does:**  
pyttsx3 turns text into speech.

**Why we need it:**  
After your character comes to life, it speaks a short line — like  
_"Hello! I’m your sketch friend!"_

**Imagine:**  
Giving your drawing a voice so it can talk to you.

---

## 🧪 pytest — The Tiny Detective

**What it does:**  
pytest helps us test our code to make sure it works.

**Why we need it:**  
As we build more features, we want to check:
- Did we break anything?
- Are all parts working together?

**Imagine:**  
A tiny detective that checks your code and says,  
“Yep, all good!” or “Oops, something’s off!”

---

## 💡 Summary Table

| Library     | Role in the Project                        | What It Feels Like                     |
|-------------|---------------------------------------------|----------------------------------------|
| Pillow      | Image editing                              | 🖌️ Digital paintbrush                  |
| NumPy       | Pixel math                                 | 🔢 Super-smart calculator              |
| OpenCV      | Image understanding                        | 👁️ Robot eye                          |
| pyttsx3     | Text-to-speech                             | 🗣️ Voice box for your character        |
| pytest      | Code testing                               | 🕵️ Tiny detective that checks your work |

---

Let me know if you want to try a mini project with one of these — like making a picture talk or removing a background from a photo.  
We can build something magical together 💫
