# Chatterboxes
**NAMES OF COLLABORATORS HERE** (Solo)


## Prep for Part 1: Get the Latest Content and Pick up Additional Parts 


### Get the Latest Content


## Part 1.
### Setup 

### Text to Speech 

\*\***Write your own shell file to use your favorite of these TTS engines to have your Pi greet you by name.**\*\*
(This shell file should be saved to your own repo for this lab.)
Look at hello_amy.sh in speech_scripts!

  
### Speech to Text


\*\***Write your own shell file that verbally asks for a numerical based input (such as a phone number, zipcode, number of pets, etc) and records the answer the respondent provides.**\*\*
Look at the ask_number folder!

### 🤖 NEW: AI-Powered Conversations with Ollama


\*\***Try creating a simple voice interaction that combines speech recognition, Ollama processing, and text-to-speech output. Document what you built and how users responded to it.**\*\*
Check out weather_assistant.py! When testing sometimes the transcript wasn't 100% correct and if the description of the weather wasn't specific enough Ollama protested slightly saying the description went against it's orignial instructions but gave a response nevertheless. Lastly, the responses took slightly too long to realistically be used in everyday life.  


### Storyboard

Storyboard and/or use a Verplank diagram to design a speech-enabled device. (Stuck? Make a device that talks for dogs. If that is too stupid, find an application that is better than that.) 

\*\***Post your storyboard and diagram here.**\*\*
<img width="1165" height="851" alt="Screenshot 2025-10-01 at 4 06 24 PM" src="https://github.com/user-attachments/assets/50bf8e5f-32e9-47d5-a7d4-070e68f04027" />

Write out what you imagine the dialogue to be. Use cards, post-its, or whatever method helps you develop alternatives or group responses. 

\*\***Please describe and document your process.**\*\*
I drew a diagram with possible interactions with different branches with different responses issues. 
![script](https://github.com/user-attachments/assets/a9c40c00-a17b-4fe1-a293-f211d92d2650)


### Acting out the dialogue

Find a partner, and *without sharing the script with your partner* try out the dialogue you've designed, where you (as the device designer) act as the device you are designing.  Please record this interaction (for example, using Zoom's record feature).

\*\***Describe if the dialogue seemed different than what you imagined when it was acted out, and how.**\*\*
I imagined the ducky being used to solve math and programming problems, but I described it as a helper that sits on your desk. As a result, it got asked a question about helping schedule time. Nevertheless there was still a line of dialogue where the ducky could ask questions to help the user come to a conclusion to their issue which is how I envisioned the duck to interact with the user instead of just giving the user the answer immediately. There was also room for the duck to be friendly. 
(link to transcript): https://docs.google.com/document/d/11_u0qU6dTTe9RkN74eHQU7arC2S0g0o86TyNUaAA8DE/edit?usp=sharing


### Wizarding with the Pi (optional)
In the [demo directory](./demo), you will find an example Wizard of Oz project. In that project, you can see how audio and sensor data is streamed from the Pi to a wizard controller that runs in the browser.  You may use this demo code as a template. By running the `app.py` script, you can see how audio and sensor data (Adafruit MPU-6050 6-DoF Accel and Gyro Sensor) is streamed from the Pi to a wizard controller that runs in the browser `http://<YouPiIPAddress>:5000`. You can control what the system says from the controller as well!

\*\***Describe if the dialogue seemed different than what you imagined, or when acted out, when it was wizarded, and how.**\*\*

# Lab 3 Part 2

For Part 2, you will redesign the interaction with the speech-enabled device using the data collected, as well as feedback from part 1.

## Prep for Part 2

1. What are concrete things that could use improvement in the design of your device? For example: wording, timing, anticipation of misunderstandings...
2. What are other modes of interaction _beyond speech_ that you might also use to clarify how to interact?
3. Make a new storyboard, diagram and/or script based on these reflections.
   
I would make it so the duck has two modes: regular rubber ducky mode that just listens and is supportive, and TA rubber duck mode that gives hints as well as add a sensor to make a clear switch between the two. Currently, the Ollama the model I'm using is a bit slow when responding to prompts, so ideally I would switch over to a faster model. Additionally, I will give a more indepth overview of the ducky to help mitage misunderstandings and provide better expectations for new users. Below are new storyboards adding to the design.
![new_storyboard](https://github.com/user-attachments/assets/e1f2c97e-768c-4629-8724-5fddc26da9ae)

## Prototype your system

The system should:
* use the Raspberry Pi 
* use one or more sensors
* require participants to speak to it. 

*Document how the system works*

*Include videos or screencaptures of both the system and the controller.*
The system is primarily controlled by user input and the duck.py file found in the ollama. The sysem relies on the plush duck to create familiarity, the mic to get sound, the sensor for swipe up and swipe down, the speaker to deliver responses, and the pi to control and connect all of the components. Below is a demo of the system in action with myself as the user controlling it. 
https://youtube.com/shorts/c7Q9j20735w?feature=share

<details>
  <summary><strong>Submission Cleanup Reminder (Click to Expand)</strong></summary>
  
  **Before submitting your README.md:**
  - This readme.md file has a lot of extra text for guidance.
  - Remove all instructional text and example prompts from this file.
  - You may either delete these sections or use the toggle/hide feature in VS Code to collapse them for a cleaner look.
  - Your final submission should be neat, focused on your own work, and easy to read for grading.
  
  This helps ensure your README.md is clear professional and uniquely yours!
</details>

## Test the system
Try to get at least two people to interact with your system. (Ideally, you would inform them that there is a wizard _after_ the interaction, but we recognize that can be hard.)

Answer the following:

### What worked well about the system and what didn't?
\*\**your answer here*\*\*

### What worked well about the controller and what didn't?

\*\**your answer here*\*\*

### What lessons can you take away from the WoZ interactions for designing a more autonomous version of the system?

\*\**your answer here*\*\*


### How could you use your system to create a dataset of interaction? What other sensing modalities would make sense to capture?

\*\**your answer here*\*\*












