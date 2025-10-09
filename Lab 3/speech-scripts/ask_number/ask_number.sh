#!/bin/bash
#https://elinux.org/RPi_Text_to_Speech_(Speech_Synthesis)

#!/bin/bash
say() { local IFS=+;/usr/bin/mplayer -ao alsa -really-quiet -noconsolecontrols "http://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&q=$*&tl=en"; }
#say $*
say " Hello, what is your favorite number? Say ok finished when you are done."

/home/pi/Interactive-Lab-Hub/Lab\ 3/.venv/bin/python transcribe_answer.py --model en-us