#!/usr/bin/env -S /home/pi/Interactive-Lab-Hub/Lab\ 3/.venv/bin/python

import sys
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json

# Queue for incoming audio
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# Load Vosk model
model = Model(lang="en-us")

# Get default input device and sample rate
device_info = sd.query_devices(None, "input")
samplerate = int(device_info["default_samplerate"])

print("Listening... (say 'ok finished' to stop)")

with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16",
                       channels=1, callback=callback):
    rec = KaldiRecognizer(model, samplerate)

    full_text = ""
    try:
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("Heard:", text)
                    if "ok finished" in text.lower() or "okay finished" in text.lower():
                        print("Stop phrase detected. Saving and exiting...")
                        break
                    full_text += text + " "
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

# Save transcript if anything was heard
if full_text.strip():
    with open("response.txt", "w") as f:
        f.write(full_text.strip() + "\n")
    print("Saved transcription to response.txt:")
    print(full_text.strip())
else:
    print("No speech detected.")
