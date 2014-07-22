FreePie-Scripts
===============

Some utility FreePIE scripts for simple things such as speech commands to keyboard mapping

-------------------------

<h2>VoiceCommand.py</h2>

This script provides basic speech to keyboard commands functionality.
The current script features are:

- Speech command recognition
- Auditive response for every command
- Press one or multiple keys at the same time
- Press and repeat pressing keys N times (once every given interval time)
- Hold keys down for N seconds

Soon:

- Play a sequence of N keys using a given interval

<h3><b>How to use/modify it?</b></h3>

- Go to the "Config and commands" section of the script
- Set the confidenceLevel variable [0-1]: the higher the value the more restrictive the speech recognition but more accurate results
- Create a command array like this:
<pre>
	commands =	[
	VoiceCommand("Hello system", 
				"Welcome! Loading system."),
	VoiceCommand("Press single key",
				"Pressing A",
				KeyPress(Key.A)), 
	VoiceCommand("Press multiple keys",
				"Pressing multiple keys",
				KeyPress([Key.LeftShift, Key.A])),
	VoiceCommand("Press 3 times",
				"Pressing a key 3 times",
				KeyRepeat(Key.B, 3, 0.5)),
	VoiceCommand("Hold key",
				"Holding key 3 seconds",
				KeyHold(Key.C, 3)),
	]
</pre>
Each VoiceCommand takes 3 arguments: the voice command to activate it, the speech response it gives and the action it takes.
Currently there are some actions it can take.
- KeyPress( key ) or KeyPress( [keys] )
- KeyRepeat( key, repetitionTimes, timeInterval = 0.1 )
- KeyHold( key, timeToHold )
