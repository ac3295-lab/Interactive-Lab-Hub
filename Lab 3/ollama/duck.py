#!/usr/bin/env -S /home/pi/Interactive-Lab-Hub/Lab\ 3/.venv/bin/python

import requests
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json
import subprocess
import threading
import board
from adafruit_apds9960.apds9960 import APDS9960
import time

# ========== SPEECH RECOGNITION SETUP ==========
q = queue.Queue()

def callback(indata, frames, time_, status):
    if status:
        print(status)
    q.put(bytes(indata))

print("Loading Vosk model...")
model = Model(lang="en-us")
device_info = sd.query_devices(None, "input")
samplerate = int(device_info["default_samplerate"])

# ========== TEXT-TO-SPEECH ==========
def speak(text):
    subprocess.run(["espeak", "-a", "10", "-s", "150", text], check=False)

# ========== OLLAMA FUNCTIONS ==========
def ask_cheer(message):
    """Friendly cheerleader assistant."""
    system_prompt = (
        "You are a cheerful motivational assistant who hypes people up, "
        "encourages them, and gives them confidence. Keep your replies very, very short and uplifting!"
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": message,
            "system": system_prompt,
            "stream": False
        }
    )
    return response.json().get("response", "You're doing great!")

def ask_helper(message):
    """Problem-solving assistant."""
    system_prompt = (
        "You are a calm, thoughtful assistant who helps people think through their problems "
        "clearly. Ask gentle guiding questions or provide practical steps to move forward. Keep your replies concise."
    )
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": message,
            "system": system_prompt,
            "stream": False
        }
    )
    return response.json().get("response", "Let's think about it together.")

# ========== GESTURE SENSOR SETUP ==========
i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

assistant_mode = "cheer"  # default mode

def gesture_listener():
    global assistant_mode
    while True:
        gesture = apds.gesture()
        if gesture == 0x01:
            assistant_mode = "cheer"
            print("Gesture: up: Cheerleader mode")
            speak("Cheerleader mode activated!")
        elif gesture == 0x02:
            assistant_mode = "help"
            print("Gesture: down: Problem-solving mode")
            speak("Problem solving mode activated.")
        time.sleep(0.1)

# Start gesture listener thread
threading.Thread(target=gesture_listener, daemon=True).start()

# ========== MAIN INTERACTION ==========
while True:
    print(f"Current mode: {assistant_mode}")
    if assistant_mode == "cheer":
        speak("You are in cheerleader mode. Tell me how you're doing!")
    else:
        speak("You are in problem solving mode. What's on your mind?")

    print("Say something (say 'ok finished' when done)...")

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        user_input = ""

        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("You said:", text)
                    user_input += text + " "
                    if "ok finished" in text.lower() or "okay finished" in text.lower():
                        break

    if user_input.strip():
        print(f"Mode: {assistant_mode}")
        print("You said:", user_input.strip())

        if assistant_mode == "cheer":
            answer = ask_cheer(user_input.strip())
        else:
            answer = ask_helper(user_input.strip())
       
        answer = answer.encode('ascii', 'ignore').decode('ascii')
        print("Assistant:", answer)
        speak(answer)
    else:
        print("No speech detected.")

    speak("You can swipe up or down to change modes, or speak again.")
    time.sleep(1)
