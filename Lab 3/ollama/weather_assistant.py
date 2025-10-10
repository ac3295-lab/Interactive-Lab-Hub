#!/usr/bin/env -S /home/pi/Interactive-Lab-Hub/Lab\ 3/.venv/bin/python

import requests
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json
import subprocess

# ========== SPEECH RECOGNITION SETUP ==========
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

print("Loading Vosk model...")
model = Model(lang="en-us")

device_info = sd.query_devices(None, "input")
samplerate = int(device_info["default_samplerate"])

# ========== LLM FUNCTION (OLLAMA) ==========
def ask_weather_advice(question):
    """Ask Ollama for outfit advice based on weather."""
    system_prompt = (
        "You are a friendly fashion assistant that helps people decide what to wear "
        "based on the weather. Be brief and practical, giving clear outfit suggestions."
    )

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": question,
            "system": system_prompt,
            "stream": False
        }
    )
    return response.json().get("response", "Sorry, I couldn’t get advice right now.")
# ========== TEXT-TO-SPEECH FUNCTION ==========
def speak(text):
    subprocess.run(["espeak", "-a", "30", "-s", "150", text], check=False)


# ========== MAIN INTERACTION ==========
print("Ask about what to wear with the weather (say 'ok finished' when done)...")

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
                

# Send to Ollama and respond
if user_input.strip():
    print("You asked:", user_input.strip())
    answer = ask_weather_advice(user_input.strip())
    print("Assistant:", answer)
    speak(answer)
else:
    print("No speech detected.")
