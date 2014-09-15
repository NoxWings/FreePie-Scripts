def setupHydra(i):
	if (i == Left):
		hydra[i].side = 'L'
	else:
		hydra[i].side = 'R'
	hydra[i].enabled = True
	
def setupMove(i):
	psmove[i].resetOrientation()
	psmove[i].resetPosition()

def setup(index):
	setupHydra(index)
	setupMove(index)

def updateHydra(i):
	hydra[i].x         = -psmove[i].position.x * PositionScale
	hydra[i].y         = psmove[i].position.y * PositionScale
	hydra[i].z         = -psmove[i].position.z * PositionScale
	
	hydra[i].yaw       = psmove[i].pitch
	hydra[i].pitch     = -psmove[i].roll
	hydra[i].roll      = psmove[i].yaw
	
	hydra[i].one       = xbox360[i].left 
	hydra[i].two       = xbox360[i].right
	hydra[i].three     = xbox360[i].a 
	hydra[i].four      = xbox360[i].b
	
	hydra[i].bumper    = xbox360[i].leftShoulder
	hydra[i].joybutton = xbox360[i].leftThumb
	hydra[i].start     = xbox360[i].down
	hydra[i].isDocked  = xbox360[i].up

	hydra[i].trigger   = xbox360[i].leftTrigger * TriggerScale 
	hydra[i].joyx      = xbox360[i].leftStickX * AxisScale
	hydra[i].joyy      = xbox360[i].leftStickY * AxisScale

def update(index):
	if psmove[index].getButtonDown( PSMoveButton.Move ):
		setupMove(index)
	updateHydra(index)
		
if starting:
	Left = 0
	Right = 1
	AxisScale = TriggerScale = 1
	PositionScale = 50
	setup(Left)
	setup(Right)

update(Left)
update(Right)