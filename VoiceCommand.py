import time;

# ***********************************
# Key Actions Classes
# ***********************************

class KeyAction:
	def __init__(self, key):
		self.keys = []
		# append or extend (both are valid)
		if isinstance(key, list):
			self.keys.extend(key)
		else:
			self.keys.append(key)
	
	def setKeyDown(self):
		for key in self.keys:
			keyboard.setKeyDown(key)	
		
	def setKeyUp(self):
		for key in self.keys:
			keyboard.setKeyUp(key)	
	
	def setKey(self, down):
		for key in self.keys:
			keyboard.setKey(key, down)
			
	def setKeyPressed(self):
		for key in self.keys:
			keyboard.setPressed(key)	
	
	def execute(self):
		raise NotImplementedError("Subclass must implement execute method")

	def update(self, curentTime):
		pass
	
class KeyPress(KeyAction):
	def __init__(self, key):
		KeyAction.__init__(self, key)

	def execute(self):
		self.setKeyPressed()

class KeyRepeat(KeyAction):
	def __init__(self, key, times, timeInterval = 0.1):
		KeyAction.__init__(self, key)
		self.times = times-1
		self.timeInterval = timeInterval
		self.time = time.time()
		self.timesLeft = 0
		
	def execute(self):
		# set the keys down
		self.setKeyPressed()
		# start the update timer
		self.time = time.time()
		self.timesLeft = self.times
			
	def update(self, currentTime):
		if (self.timesLeft > 0):
			if (currentTime - self.time) >= self.timeInterval:
				self.timesLeft = self.timesLeft - 1
				self.time = time.time()
				self.setKeyPressed()

class KeyHold(KeyAction):
	def __init__(self, key, duration):
		KeyAction.__init__(self, key)
		self.duration = duration
		self.time = time.time()
		self.needUpdate = False
		
	def execute(self):
		# set the keys down
		self.setKeyDown()
		# start the update timer
		self.time = time.time()
		self.needUpdate = True
			
	def update(self, currentTime):
		if self.needUpdate:
			# determine if we should stop pressing the keys
			if (currentTime - self.time) >= self.duration:
				self.setKeyUp()
				self.needUpdate = False


# ***********************************
# VoiceCommand Class
# ***********************************

class VoiceCommand:
	def __init__(self, cmd, response, action = None):
		self.cmd = cmd
		self.response = response
		self.action = action
		
	def said(self, confidence, response=False):
		return ((self.cmd != "") and speech.said(self.cmd, confidence))

	def playResponse(self):
		if self.response:
			speech.say(self.response)
		
	def execute(self):
		if self.action:
			self.action.execute()
			
	def update(self, currentTime):
		if self.action:
			self.action.update(currentTime)


# ***********************************
# Config and commands
# ***********************************

if starting:
	confidenceLevel = 0.7

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


# ***********************************
# Main Loop
# ***********************************

currentTime = time.time()
for command in commands:
	# if said execute action
	if command.said(confidenceLevel):
		command.playResponse()
		command.execute()
	command.update(currentTime)
