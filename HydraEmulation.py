# -----------------------------------
# ------ SETUP FUNCTIONS ------------
# -----------------------------------

def setup():
	setupHydra(0)
	resetMove(0)
	setupHydra(1)
	resetMove(1)

def setupHydra(i):
	if (i == LeftMoveIndex):
		hydra[i].side = 'L'
	else:
		hydra[i].side = 'R'
	hydra[i].enabled = True
	
def resetMove(i):
	psmove[i].resetOrientation()
	psmove[i].resetPosition()

# -----------------------------------
# ------ CONTROLLERS HAND BINDING ---
# -----------------------------------

def checkControllersBound():
	checkMoveBound(0)
	checkMoveBound(1)
	checkControllerBound(0)	
	checkControllerBound(1)
	return (LeftMoveIndex != -1) and (LeftControllerIndex != -1)

def checkMoveBound(i):
	if (psmove[i].getButtonDown(PSMoveButton.Move)):
		global LeftMoveIndex
		LeftMoveIndex = i
	
def checkControllerBound(i):
	if (xbox360[i].down):
		global LeftControllerIndex
		LeftControllerIndex = i
		
def getMoveIndex(hydraIndex):
	return hydraIndex

def getControllerIndex(hydraIndex):
	if (LeftMoveIndex == LeftControllerIndex):
		return hydraIndex
	else:
		return 1-hydraIndex

# -----------------------------------
# ------ UPDATE FUNCTIONS -----------
# -----------------------------------

def update(hydraIndex):
	moveIndex = getMoveIndex(hydraIndex)
	controllerIndex = getControllerIndex(hydraIndex)

	if psmove[moveIndex].getButtonDown(PSMoveButton.Move) or xbox360[controllerIndex].down:
		resetMove(moveIndex)

	updateHydra(moveIndex, controllerIndex)	

def updateHydra(i, j):
	hydra[i].yaw       = -psmove[i].yaw
	hydra[i].pitch     =  psmove[i].pitch
	hydra[i].roll      = -psmove[i].roll
	
	hydra[i].one       = xbox360[j].left 
	hydra[i].two       = xbox360[j].right
	hydra[i].three     = xbox360[j].a 
	hydra[i].four      = xbox360[j].b
	
	hydra[i].bumper    = xbox360[j].leftShoulder
	hydra[i].joybutton = xbox360[j].leftThumb
	hydra[i].start     = xbox360[j].down
	hydra[i].isDocked  = xbox360[j].up

	hydra[i].trigger   = (xbox360[j].leftTrigger + psmove[i].trigger)* TriggerScale 
	hydra[i].joyx      = xbox360[j].leftStickX  * AxisScale
	hydra[i].joyy      = xbox360[j].leftStickY  * AxisScale

def updateSmoothTracking():
	hydra[0].x         = filters.simple(-psmove[0].position.x, Smoothing) * PositionScale
	hydra[0].y         = filters.simple( psmove[0].position.y, Smoothing) * PositionScale
	hydra[0].z         = filters.simple(-psmove[0].position.z, DepthSmooth) * PositionScale
	hydra[1].x         = filters.simple(-psmove[1].position.x, Smoothing) * PositionScale
	hydra[1].y         = filters.simple( psmove[1].position.y, Smoothing) * PositionScale
	hydra[1].z         = filters.simple(-psmove[1].position.z, DepthSmooth) * PositionScale

# -----------------------------------
# ------ MAIN PROGRAM ---------------
# -----------------------------------

if starting:
	ControllersBound = False
	LeftMoveIndex = -1
	LeftControllerIndex = -1

	AxisScale = TriggerScale = 1
	PositionScale = 50
	Smoothing = 0.25
	DepthSmooth = 0.35

	diagnostics.debug("USAGE - BOUND CONTROLLERS:")
	diagnostics.debug("Press the the left psmove \"Move\" button")
	diagnostics.debug("Press the left nagivation controller POV down")

if ControllersBound:
	updateSmoothTracking()
	update(0)
	update(1)
else:
	ControllersBound = checkControllersBound()
	if (ControllersBound):
		diagnostics.debug("- CONTROLLERS BOUND! -")
		setup()