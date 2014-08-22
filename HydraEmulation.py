#-------------------------------
	
def update():
    global yaw
    yaw = android[0].googleYaw
    global pitch
    pitch = -android[0].googlePitch
    global roll
    roll = android[0].googleRoll

if starting:
    centerYaw = 0
    centerPitch = 0
    centerRoll = 0
   
    yaw = 0
    pitch = 0
    roll = 0
    android[0].update += update

if keyboard.getKeyDown(Key.LeftControl) and keyboard.getPressed(Key.C):
    centerYaw = yaw
    centerPitch = pitch
    centerRoll = roll


#---------------------------


# --------------------
#  DATA STRUCTURES AND FUNCTIONS 
# --------------------

class POVDir:
	none = -1
	up = 0
	down = 18000
	left = 27000
	right = 9000
    
    
class NavButton:
#	Using nav through ps3 emulation
#	X = 2
#	O = 1
#	L1 = 4
#	joybutton = 9
#   Using nav through xbox360 emulation
	X = 0
	O = 1
	L1 = 4
	joybutton = 8


def setButtonMappings(hydraIndex, navconIndex):
	# BUTTONS
	hydra[hydraIndex].one       = (joystick[navconIndex].pov[0] == POVDir.left)
	hydra[hydraIndex].two       = (joystick[navconIndex].pov[0] == POVDir.right)
	hydra[hydraIndex].three     = joystick[navconIndex].getDown( NavButton.X )
	hydra[hydraIndex].four      = joystick[navconIndex].getDown( NavButton.O )
	hydra[hydraIndex].bumper    = joystick[navconIndex].getDown( NavButton.L1 )
	hydra[hydraIndex].joybutton = joystick[navconIndex].getDown( NavButton.joybutton )
	hydra[hydraIndex].start     = (joystick[navconIndex].pov[0] == POVDir.down)


	# AXIS
	hydra[hydraIndex].trigger   = (joystick[navconIndex].z / TriggerScale) 
	hydra[hydraIndex].joyx      = (joystick[navconIndex].x / AxisScale)
	hydra[hydraIndex].joyy      = (joystick[navconIndex].y / AxisScale)

def setHydraTracking(hydraIndex):
	hydra[hydraIndex].x = 0
	hydra[hydraIndex].y = 0
	hydra[hydraIndex].z = 0
	hydra[hydraIndex].yaw  = yaw - centerYaw
	hydra[hydraIndex].pitch = pitch - centerPitch
	hydra[hydraIndex].roll = roll - centerRoll
	

def hydraEmulation(hydraIndex, navconIndex):
	setButtonMappings(hydraIndex, navconIndex)
	setHydraTracking(hydraIndex)

# --------------------
#  CONFIG AND DEBUG 
# --------------------

if starting:
	Left = 0
	Right = 1
	Debug = True
	AxisScale = TriggerScale = 1
	joysticksConnected = (len(joystick) >= 2)
	if (not joysticksConnected):
		diagnostics.debug( "ERROR: You need 2 joysticks connected. Currently: %d joysticks" % len(joystick) )
	else:
		hydra[0].side = "L"
		hydra[1].side = "R"
		hydra[0].enabled = True
		hydra[1].enabled = True
		
def joystickName(index):
	if (index == Left):
		return "Left joystick: "
	else:
		return "Right joystick: "

def debug(index):
	for x in range(0, 32):
		if joystick[index].getPressed(x):
			diagnostics.debug( joystickName(index) + "Button %d pressed" % x )
	if (joystick[index].pov[0] != POVDir.none):
		diagnostics.debug( joystickName(index) + "POV set to %d" % joystick[index].pov[0] )
	if (joystick[index].x != 0):
		diagnostics.debug( joystickName(index) + "Axis X set to %d" % joystick[index].x )
	if (joystick[index].y != 0):
		diagnostics.debug( joystickName(index) + "Axis Y set to %d" % joystick[index].y )
	if (joystick[index].z != 0):
		diagnostics.debug( joystickName(index) + "Axis Z set to %d" % joystick[index].z )

def debugHydra(index):
	if (hydra[index].joyx != 0):
		diagnostics.debug( joystickName(index) + " Axis JoyX set to %d" % hydra[index].joyx) 
	if (hydra[index].joyy != 0):
		diagnostics.debug( joystickName(index) + " Axis JoyY set to %d" % hydra[index].joyy)

# --------------------
#  MAIN PROGRAM
# --------------------

if (joysticksConnected):
	hydraEmulation(0, Left)
	hydraEmulation(1, Right)
	if Debug:
		debug(Left)
		debug(Right)

if keyboard.getKeyDown( Key.LeftAlt ) and keyboard.getPressed( Key.C ):
	Debug = not Debug
	
	
