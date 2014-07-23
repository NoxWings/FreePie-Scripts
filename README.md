FreePie-Scripts
===============

Some utility FreePIE scripts for simple things such as speech commands to keyboard mapping

-------------------------

<h2>VoiceToKeyboard.py</h2>

This script provides basic speech to keyboard commands functionality.
The current script features are:

- Speech command recognition
- Auditive response for every command
- Press one or multiple keys at the same time
- Press and repeat pressing keys N times (once every given interval time)
- Hold keys down for N seconds


<h3><b>How to use/modify it?</b></h3>

- Go to the "Config and commands" section of the script
- Set the confidenceLevel variable [0-1]: the higher the value the more restrictive the speech recognition but more accurate results
- Start adding your commands after the line 
<pre>v2k = VoiceToKeyboard( confidenceLevel )</pre>

<pre>
# ***********************************
# Config and commands
# ***********************************

if starting:
	confidenceLevel = 0.7
	v2k = VoiceToKeyboard( confidenceLevel )

	# Voice response only
	v2k.addCommand("Hello", "!Welcome! Initialising system.")

	# Key Press 
	v2k.addCommand("Test single press", "Single key press", KeyPress( Key.A ))
	v2k.addCommand("Test multiple press", "Multiple keys press", KeyPress( [ Key.LeftShift, Key.A ] ))

	# Key Hold
	v2k.addCommand("Test single hold", "Single key hold. 2 seconds", KeyPress( Key.B, 2 ))
	v2k.addCommand("Test multiple hold", "Multipl keys hold. 2 seconds", KeyPress( [ Key.LeftShift, Key.B ], 2 ))

	# Key Repeat
	v2k.addCommand("Test single repeat", "Pressing C key 5 times", KeyRepeat( Key.C, 5 ))
	v2k.addCommand("Test multiple repeat", "Pression Shift and C keys 5 times", KeyRepeat( [ Key.LeftShift, Key.C ], 5 , 0.1, 0.07 ))


v2k.executeLoop() 
</pre>
Each command takes 3 arguments: the voice command to activate it, the speech response it gives and the action it takes.
Currently there are some actions it can take.
- Press keys <pre> KeyPress( key ) or KeyPress( [keys] ) </pre>
- Hold keys <pre> KeyPress( key, timeToHold ) </pre>
- Press keys repeatedly <pre> KeyRepeat( key, repetitionTimes, timeInterval = 0.1, holdDuration = 0.07 ) </pre>

