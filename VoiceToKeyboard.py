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
			#keyboard.setPressed(key)
			keyboard.setKeyDown(key)
			keyboard.setKeyUp(key)
						
	def execute(self):
		raise NotImplementedError("Subclass must implement execute method")

	def update(self, curentTime):
		pass


class KeyPress(KeyAction):
	def __init__(self, key, duration = 0.07):
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


class KeyRepeat(KeyAction):
	def __init__(self, key, times, timeInterval = 0.1, duration = 0.07):
		KeyAction.__init__(self, key)
		self.times = times-1 
		self.timeInterval = timeInterval
		# Duration cannot be larger than time interval
		if (duration > timeInterval):
			self.duration = timeInterval
		else:
			self.duration = duration
		#internal use variables
		self.time = time.time()
		self.timesLeft = 0
		
	def execute(self):
		# set the keys down
		self.setKeyDown()
		# start the update timer
		self.time = time.time()
		self.timesLeft = self.times
			
	def update(self, currentTime):
		if (self.timesLeft > 0):
			elapsedTime = currentTime - self.time
			# Release Current Key
			if (elapsedTime >= self.duration):
				self.setKeyUp()
			# Press Next KeyDown
			if (elapsedTime >= self.timeInterval):
				self.setKeyDown()
				self.time = time.time()
				self.timesLeft = self.timesLeft - 1
				

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
# VoiceToKeyboard
# ***********************************

class VoiceToKeyboard:
	def __init__(self, confidenceLevel, commands = None):
		self.confidenceLevel = confidenceLevel
		self.commands = []
		self.setCommands(commands)
	
	def setCommands(self, commands):
		if isinstance(commands, list):
			self.commands = commands
	
	def addCommand(self, cmd, response, action = None):
		self.commands.append( VoiceCommand(cmd, response, action) )

	def executeLoop(self):
		currentTime = time.time()
		for command in self.commands:
			# if said execute action
			if command.said(self.confidenceLevel):
				command.playResponse()
				command.execute()
			command.update(currentTime)

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
	v2k.addCommand("Test single repeat", "Bajando velocidad a IDS 1", KeyRepeat( Key.C, 5 ))
	v2k.addCommand("Test multiple repeat", "Subiendo velocidad a IDS 5", KeyRepeat( [ Key.LeftShift, Key.C ], 5 , 0.1, 0.07 ))
	

v2k.executeLoop() 

