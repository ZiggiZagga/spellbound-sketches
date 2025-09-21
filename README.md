
# ✨ Spellbound-Sketches

## 🟢 1-2-3 Quickstart (For Kids & Beginners)

1. **Open a terminal** (or ask an adult to help)
2. **Copy & paste these commands:**

	```bash
	git clone https://github.com/ZiggiZagga/spellbound-sketches.git
	cd spellbound-sketches
	pip install -r requirements.txt
	python -m spellbound_sketches.cli sketch
	```

3. **When it asks for an image, just press Enter** (it will use the sample drawing for you!)

You should see a little window with a moving drawing and hear a voice line. 🎨🗣️

---

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


## � Getting Started (For Everyone!)

### 1. Install Python (if you don't have it)

- **Windows:**
	- Download Python from https://www.python.org/downloads/windows/
	- Run the installer and check "Add Python to PATH" during setup.
- **macOS:**
	- Download from https://www.python.org/downloads/macos/ or use Homebrew: `brew install python`
- **Linux:**
	- Use your package manager, e.g. `sudo apt install python3 python3-pip`

### 2. Install Visual Studio Code (VS Code)

- Download from https://code.visualstudio.com/
- Install the **Python extension** (search for "Python" in the Extensions sidebar).

### 3. Clone this repository

Open a terminal and run:

```bash
git clone https://github.com/ZiggiZagga/spellbound-sketches.git
cd spellbound-sketches
```

### 4. Install dependencies

In your terminal, run:

```bash
pip install -r requirements.txt
```


### 5. Try the sample project!

- Open VS Code in this folder: `code .`
- Run the following command in the terminal:

	```bash
	python -m spellbound_sketches.cli sketch
	```

- When prompted for an image, you can just press Enter to use the provided sample (`sample_data/sample_drawing.png`).
---

## 👨‍👩‍👧 For Parents & Helpers

- The sample image is used by default if no path is given.
- All dependencies are listed in `requirements.txt`.
- The code is commented for young learners and robust against common errors.
- For more details, see the full instructions below.

---

### 6. (Optional) Run the tests

```bash
pytest
```

---

## 🖼️ Sample Data

This repo includes a `sample_data/` folder with:
- `sample_drawing.png` — a sample drawing to get you started
- `variants/eyesclosed.png` — a variant image for animation

You can add your own drawings to this folder and use them in the app!

---

## 🛠️ Requirements (for reference)

```txt
Pillow>=9.0.0
numpy
opencv-python
pyttsx3
pytest
typer
```


# 🧰 Why We Need These Python Libraries
---

## 🏁 Troubleshooting & Tips

- If you see an error about `pyttsx3` or TTS, make sure you have a working audio setup and (on Linux) install `espeak` or `espeak-ng`.
- If you get a `ModuleNotFoundError`, make sure you are running commands from the project root and have installed all requirements.
- If you want to use your own drawing, save it as a PNG or JPG and provide the path when prompted.
- For any issues, try running `pytest` to check your setup.

---

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

