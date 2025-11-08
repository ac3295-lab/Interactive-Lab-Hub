# Observant Systems


For lab this week, we focus on creating interactive systems that can detect and respond to events or stimuli in the environment of the Pi, like the Boat Detector we mentioned in lecture. 
Your **observant device** could, for example, count items, find objects, recognize an event or continuously monitor a room.

This lab will help you think through the design of observant systems, particularly corner cases that the algorithms need to be aware of.

## Prep

1.  Install VNC on your laptop if you have not yet done so. This lab will actually require you to run script on your Pi through VNC so that you can see the video stream. Please refer to the [prep for Lab 2](https://github.com/FAR-Lab/Interactive-Lab-Hub/blob/-/Lab%202/prep.md#using-vnc-to-see-your-pi-desktop).
2.  Install the dependencies as described in the [prep document](prep.md). 
3.  Read about [OpenCV](https://opencv.org/about/),[Pytorch](https://pytorch.org/), [MediaPipe](https://mediapipe.dev/), and [TeachableMachines](https://teachablemachine.withgoogle.com/).
4.  Read Belloti, et al.'s [Making Sense of Sensing Systems: Five Questions for Designers and Researchers](https://www.cc.gatech.edu/~keith/pubs/chi2002-sensing.pdf).

### For the lab, you will need:
1. Pull the new Github Repo
1. Raspberry Pi
1. Webcam 

### Deliverables for this lab are:
1. Show pictures, videos of the "sense-making" algorithms you tried.
1. Show a video of how you embed one of these algorithms into your observant system.
1. Test, characterize your interactive device. Show faults in the detection and how the system handled it.

## Overview
Building upon the paper-airplane metaphor (we're understanding the material of machine learning for design), here are the four sections of the lab activity:

A) [Play](#part-a)

B) [Fold](#part-b)

C) [Flight test](#part-c)

D) [Reflect](#part-d)

---

### Part A
### Play with different sense-making algorithms.

#### Pytorch for object recognition


<img width="498" height="361" alt="Screenshot 2025-10-22 at 4 51 24 PM" src="https://github.com/user-attachments/assets/ed6b1138-7a82-49f5-8652-1bfd97684e77" />

#### More classes

[PyTorch supports transfer learning](https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html), so you can fine‑tune and transfer learn models to recognize your own objects. It requires extra steps, so we won't cover it here.

For more details on transfer learning and deployment to embedded devices, see Deep Learning on Embedded Systems: A Hands‑On Approach Using Jetson Nano and Raspberry Pi (Tariq M. Arif). [Chapter 10](https://onlinelibrary.wiley.com/doi/10.1002/9781394269297.ch10) covers transfer learning for object detection on desktop, and [Chapter 15](https://onlinelibrary.wiley.com/doi/10.1002/9781394269297.ch15) describes moving models to the Pi using ONNX.

### Machine Vision With Other Tools
The following sections describe tools ([MediaPipe](#mediapipe) and [Teachable Machines](#teachable-machines)).

#### MediaPipe


Consider how you might use this position based approach to create an interaction, and write how you might use it on either face, hand or body pose tracking.

You could allow the user to make touchless decisions (ex: changing the volume of a song or striking a pose to make a decision). Additionally, you could use it in body pose tracking for fun games to see who can strick the best poses fastesr etc. Lastly, you can use face tracking to show emotion and make some decision based off of that as well (ex: singing a song to make the user happier). 

<img width="686" height="814" alt="Screenshot 2025-10-22 at 4 46 34 PM" src="https://github.com/user-attachments/assets/ca88c23c-a514-48aa-8759-bbd1604d0beb" />

<img width="1440" height="900" alt="Screenshot 2025-10-22 at 4 47 18 PM" src="https://github.com/user-attachments/assets/82c8677e-db7d-4a78-8749-744a88d2122c" />
<img width="694" height="716" alt="Screenshot 2025-10-22 at 5 26 05 PM" src="https://github.com/user-attachments/assets/50d89e16-7350-4ff6-a3e6-65293fba5843" />


#### Moondream Vision-Language Model

<img width="721" height="682" alt="Screenshot 2025-10-22 at 4 58 49 PM" src="https://github.com/user-attachments/assets/5b00c53b-bfe5-4b22-955c-d255802e70eb" />

**Design consideration**: Think about how slower response times change your interaction design. What kinds of observant systems benefit from thoughtful, delayed responses rather than real-time classification? Consider systems that monitor over longer time periods or provide periodic summaries rather than instant feedback.

You could attach it to something you expect to take a long time to process like polaroids!

#### Teachable Machines
```
<img width="843" height="510" alt="Screenshot 2025-10-22 at 5 05 52 PM" src="https://github.com/user-attachments/assets/a3cfcc2e-83f4-466b-a26e-b821c0f43270" />


Next train your own model. Visit [TeachableMachines](https://teachablemachine.withgoogle.com/train), select Image Project and Standard model. The raspberry pi 4 is capable to run not just the low resource models. Second, use the webcam on your computer to train a model. *Note: It might be advisable to use the pi webcam in a similar setting you want to deploy it to improve performance.*  For each class try to have over 150 samples, and consider adding a background or default class where you have nothing in view so the model is trained to know that this is the background. Then create classes based on what you want the model to classify. Lastly, preview and iterate. Finally export your model as a 'Tensorflow lite' model. You will find an '.tflite' file and a 'labels.txt' file. Upload these to your pi (through one of the many ways such as [scp](https://www.raspberrypi.com/documentation/computers/remote-access.html#using-secure-copy), sftp, [vnc](https://help.realvnc.com/hc/en-us/articles/360002249917-VNC-Connect-and-Raspberry-Pi#transferring-files-to-and-from-your-raspberry-pi-0-6), or a connected visual studio code remote explorer).
![Teachable Machines Browser](Readme_files/tml_browser.gif)
![Tensorflow Lite Download](Readme_files/tml_download-model.png)

Include screenshots of your use of Teachable Machines, and write how you might use this to create your own classifier. Include what different affordances this method brings, compared to the OpenCV or MediaPipe options.
<img width="1440" height="900" alt="Screenshot 2025-10-22 at 5 13 46 PM" src="https://github.com/user-attachments/assets/08580a52-abfa-4ed6-b657-9a2e863390e6" />
I used it to create a classifier of happy and sad faces, this method allows a lot of freedom for what you want to classify and while restricting possible outputs (for example image recognition in pytorch has a lot of possibilites, making it harder if you just want a binary between two things). Compared to media pipe teachable machines would be able to make use of the full context like colors and shapes rather than just hand positions and movements allowing for more flexibility. 

### Part B
### Construct a simple interaction.

* Pick one of the models you have tried, and experiment with prototyping an interaction.
* This can be as simple as the boat detector shown in lecture.
* Try out different interaction outputs and inputs.


**\*\*\*Describe and detail the interaction, as well as your experimentation here.\*\*\***
I really liked the MediaPipe model and thought it was really cool! The sliding feature with your hands caught my eye and it would be cool to control how loud the bluetooth speaker was through the pinching motion. The workflow would be something like this: program prompts listener through a spoken statement if the volume is too loud, explaining the user will be able to use their hands to adjust -> gives 30 second window for user to adjust accordingly -> says what sound level the user has chosen and proceeds to play. I was originally thinking about doing my polaroid idea with moondream-vision language model, but thought that the use of it may be too clunky and slow. A user would have to look at a terminal or screen to be prompted to aim the webcam to take a "polaroid" and then either have a limited amount of time to shoot or have to input a stop command while framing their shot. I then pivoted to the MediaPipe model and was thinking about either using the hand gestures or the percentage control. Ultimately, I decided the percentage control allowed for a more interactive experience. One hand gesture could be mapped to one output (ex: thumbs up to a cheering sound), while the percentage control allows a spectrum or range of outputs. Additionally, using the percentage control allows the user have a simple cause and effect rather than hearing or seeing a long list of different hand gestures to sounds. Lastly, some hand gestures may be hard to convey without visual aid while the single pinching motion may be easier to understand. This was my plan, however, looking at the code, I realized that it is controlling the volume already, so to pivot instead of volume I decided I wanted it to control the opacity of an image overlay. 


### Part C
### Test the interaction prototype

Now flight test your interactive prototype and **note down your observations**:
For example:
1. When does it what it is supposed to do? It does what it's supposed to do when you are visible and the appropriate distance away.
1. When does it fail? When your fingers are overlapping or not visible. 
1. When it fails, why does it fail? It fails to read your hand gesture and cannot accurate pick up your hand. 
1. Based on the behavior you have seen, what other scenarios could cause problems? In lowlight situations, if the user cannot accurately position themselves, if the user overlaps their finders. 

**\*\*\*Think about someone using the system. Describe how you think this will work.\*\*\***
1. Are they aware of the uncertainties in the system? I think they could visually see the lines crossing and see the the model struggles to pick up their hands. Though without documentation they may not know what the purpose of the lines are or what motion they are supposed to do. 
1. How bad would they be impacted by a miss classification? They might get confused and a little annoyed. 
1. How could change your interactive system to address this? I should definitely prompt them to let them know something will happen 
1. Are there optimizations you can try to do on your sense-making algorithm. I think the algorithm works fine, I think it's more on documentaiton and making the users are in the correct spot and distance from the camera. 

### Part D
### Characterize your own Observant system

Now that you have experimented with one or more of these sense-making systems **characterize their behavior**.
During the lecture, we mentioned questions to help characterize a material:
* What can you use X for? You could possibly use it to help adjust opacity and take hands-free, self-edited photos. 
* What is a good environment for X? A reasonably-lit area where the user and their hands are visible. 
* What is a bad environment for X? A dark area. 
* When will X break? It breaks when it cannot read your hand positions or when your fingers overlap. 
* When it breaks how will X break? It won't work how you want it to, won't pick up what you want it to and when it does pick things up it's identification is a bit muddled preventing it from working accurately. 
* What are other properties/behaviors of X? It is very reactive and you can clearly see what it is identifying and reacting to. 
* How does X feel? It is reasonably smooth and corresponds nicely with slower motions, though it is generally able to pick up quicker motions. 

**\*\*\*Include a short video demonstrating the answers to these questions.\*\*\***
This is a link for all but what is a bad environment: https://youtube.com/shorts/WAseYb6eIUU?feature=share

### Part 2.

Following exploration and reflection from Part 1, finish building your interactive system, and demonstrate it in use with a video.
I decided I wanted to develop the interaction a bit to make it usable and add more value to users. I can imagine it in a theme park like disney land with users being amused at the suddenly appearing "ghosts" and able to touchlessly take pictures of them. Being able to take the picture without the user hitting any buttons was important to me as ideally the user would be able to leave the interaction without touching anything. I added visual prompts for when the photo was about to be taken and how to trigger the surprise. It had required some iteration and debugging as originally as soon as the user's hands were out of view the dogs would disappear and the countdown would stop. Also, the original pictures did not include the dogs at all! Ideally I would want this program with the camera in a fixed position with a spot on the floor for users to walk in. While testing it myself, I had my users sit in a chair a specific distance away. Additional user testing had gone ok, though there were some complaints about the sudden picture being taken and not being given enough time to pose. Additionally, as seen in the video below when I ran it myself, the model wasn't able to read the gesture well if the whole hand wasn't in frame, something I hadn't thought of before. I imagine within this exibit in real life some pictures and tips will be posted along the walls near the camera. 
**\*\*\*Include a short video demonstrating the finished result.\*\*\***
https://youtube.com/shorts/FZbXJjUhyf8?feature=share
