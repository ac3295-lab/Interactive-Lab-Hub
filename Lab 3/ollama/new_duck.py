#!/usr/bin/env -S /home/pi/Interactive-Lab-Hub/Lab\ 3/.venv/bin/python

# ========== IMPORTS ==========
from google import genai
from google.genai import types
import sounddevice as sd
import queue
from vosk import Model, KaldiRecognizer
import json
import subprocess
import threading
import board
from adafruit_apds9960.apds9960 import APDS9960
import time
import os

# ========== GEMINI SETUP ==========
# TODO: Paste your Google API Key here
GOOGLE_API_KEY = "AIzaSyARp8DTTcb1vsYyys7YmkfxVD7aNRMqJYM"

client = genai.Client(api_key=GOOGLE_API_KEY)

# 'helper_chat' remembers the conversation while in helper mode
helper_chat = client.chats.create(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are a calm, thoughtful assistant who helps people think clearly. Keep replies concise.",
        temperature=0.7
    )
)

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
    # -a 10 is volume, -s 150 is speed
    subprocess.run(["espeak", "-a", "90", "-s", "150", text], check=False)

# ========== AUDIO PLAYBACK ==========
def play_audio(filename):
    """Play .wav files directly"""
    print(f"Playing: {filename}")
    if os.path.exists(filename):
        os.system(f"aplay {filename}")
    else:
        print(f"Warning: {filename} not found")

# ========== AI FUNCTIONS ==========
def ask_gemini_chat(message):
    """Sends message to the helper chat history."""
    try:
        response = helper_chat.send_message(message)
        return response.text
    except Exception as e:
        print(f"Gemini Error: {e}")
        return "I'm having trouble connecting to the brain."

# ========== TIMER MODE ==========
def run_focus_timer():
    """Run a 45-second focus timer with audio cues"""
    print("Starting focus timer...")
    
    # Step 1 — Play start message
    if os.path.exists("start.wav"):
        play_audio("start.wav")
    else:
        speak("Let's begin! Starting your focus session now.")
    
    # Step 2 — Timer countdown
    total_seconds = 45
    five_min_warning_given = False
    
    while total_seconds > 0:
        time.sleep(1)
        total_seconds -= 1
        
        # 5-minute warning at 20 seconds remaining (for demo purposes)
        if total_seconds == 20 and not five_min_warning_given:
            five_min_warning_given = True
            
            # Soft notification
            if os.path.exists("soft_quack.wav"):
                play_audio("soft_quack.wav")
            
            # Warning chime
            if os.path.exists("notice.wav"):
                play_audio("notice.wav")
            
            # Verbal warning
            if os.path.exists("five_min_left.wav"):
                play_audio("five_min_left.wav")
            else:
                speak("Only 5 minutes left. Stay with me.")
    
    # Step 3 — Session complete
    if os.path.exists("finish_generic.wav"):
        play_audio("finish_generic.wav")
    else:
        speak("Great job! Your focus session is complete.")
    
    print("Focus timer complete!")

# ========== GESTURE SENSOR SETUP ==========
i2c = board.I2C()
apds = APDS9960(i2c)
apds.enable_proximity = True
apds.enable_gesture = True

assistant_mode = "timer"  # default mode

def gesture_listener():
    global assistant_mode
    while True:
        try:
            gesture = apds.gesture()
            if gesture == 0x01:  # UP gesture
                # Only speak if we are actually changing modes
                if assistant_mode != "timer":
                    assistant_mode = "timer"
                    print("Gesture: UP -> Timer mode")
                    speak("Timer mode activated!")
            elif gesture == 0x02:  # DOWN gesture
                if assistant_mode != "help":
                    assistant_mode = "help"
                    print("Gesture: DOWN ->Problem-solving mode")
                    speak("Problem solving mode activated.")
            time.sleep(0.1)
        except OSError:
            pass

threading.Thread(target=gesture_listener, daemon=True).start()

# ========== MAIN INTERACTION ==========
speak("System ready. Waiting for input.")

while True:
    print(f"[{assistant_mode.upper()} MODE] Listening... (say 'finished' when done)")
    
    # Timer mode - runs immediately without waiting for voice input
    if assistant_mode == "timer":
        run_focus_timer()
        # After timer completes, switch to helper mode
        assistant_mode = "help"
        speak("Timer complete. Switching to helper mode.")
        continue
    
    # Helper mode - listen for voice input
    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype="int16",
                           channels=1, callback=callback):
        rec = KaldiRecognizer(model, samplerate)
        user_input = ""
        listening = True
        
        while listening:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print("You said:", text)
                    user_input += text + " "
                    # Check for exit phrase
                    if "finished" in text.lower():
                        listening = False

    # Clean the trigger phrase out of the input
    clean_input = user_input.lower().replace("finished", "").strip()

    if clean_input:
        print(f"Sending to helper chat: {clean_input}")
        
        # Call the chat function
        answer = ask_gemini_chat(clean_input)
       
        # Clean text for espeak (remove asterisks used for bolding)
        answer = answer.replace("*", "") 
        cleaned_answer = answer.encode('ascii', 'ignore').decode('ascii')
        
        print("Assistant:", cleaned_answer)
        speak(cleaned_answer)
    else:
        # Optional: Short beep or silence if nothing was heard
        pass

    # Small buffer before listening again
    time.sleep(0.5)