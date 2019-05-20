from __future__ import print_function
from __future__ import division


from builtins import range
from past.utils import old_div
from malmo import MalmoPython 
import os
import sys
import time
import json
from random import randrange
from math import *

if sys.version_info[0] == 2:
	sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)  # flush print output immediately
else:
	import functools
	print = functools.partial(print, flush=True)


missionXML='''<?xml version="1.0" encoding="UTF-8" standalone="no" ?>
			<Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
			
			  <About>
				<Summary>Hello world!</Summary>
			  </About>
			  
			<ServerSection>
			  <ServerInitialConditions>
				<Time>
					<StartTime>1000</StartTime>
					<AllowPassageOfTime>false</AllowPassageOfTime>
				</Time>
				<Weather>clear</Weather>
			  </ServerInitialConditions>
			  <ServerHandlers>
				  <FlatWorldGenerator generatorString="3;7,44*49,73,35:1,159:4,95:13,35:13,159:11,95:10,159:14,159:6,35:6,95:6;12;"/>
				  
				  <ServerQuitFromTimeUp timeLimitMs="300000"/>
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>
			  
			  <AgentSection mode="Survival">
				<Name>MalmoTutorialBot</Name>
				<AgentStart>
					<Placement x="0.5" y="56.0" z="0.5" yaw="90"/>
					<Inventory>
						<InventoryItem slot="8" type="diamond_pickaxe"/>
					</Inventory>
				</AgentStart>
				<AgentHandlers>
				  <ObservationFromFullStats/>
				  <ObservationFromGrid>
					  <Grid name="floor">
						<min x="-2" y="-1" z="-2"/>
						<max x="2" y="-1" z="2"/>
					  </Grid>
				  </ObservationFromGrid>
				  <DiscreteMovementCommands/>
				  <InventoryCommands/>
				  <AgentQuitFromTouchingBlockType>
					  <Block type="diamond_block" />
				  </AgentQuitFromTouchingBlockType>
				  <ObservationFromNearbyEntities> 
					<Range name="player" xrange="1" yrange="1" zrange="1"/>
				  </ObservationFromNearbyEntities>
				</AgentHandlers>
			  </AgentSection>
			</Mission>'''

# Create default Malmo objects:

agent_host = MalmoPython.AgentHost()
try:
	agent_host.parse( sys.argv )
except RuntimeError as e:
	print('ERROR:',e)
	print(agent_host.getUsage())
	exit(1)
if agent_host.receivedArgument("help"):
	print(agent_host.getUsage())
	exit(0)

my_mission = MalmoPython.MissionSpec(missionXML, True)
my_mission_record = MalmoPython.MissionRecordSpec()

# Attempt to start a mission:
max_retries = 3
for retry in range(max_retries):
	try:
		agent_host.startMission( my_mission, my_mission_record )
		break
	except RuntimeError as e:
		if retry == max_retries - 1:
			print("Error starting mission:",e)
			exit(1)
		else:
			time.sleep(2)

# Loop until mission starts:
print("Waiting for the mission to start ", end=' ')
world_state = agent_host.getWorldState()
while not world_state.has_mission_begun:
	print(".", end="")
	time.sleep(0.1)
	world_state = agent_host.getWorldState()
	for error in world_state.errors:
		print("Error:",error.text)

print()
print("Mission running ", end=' ')

def updateState():
	global observations
	global world_state
	world_state = agent_host.getWorldState()
	if world_state.number_of_observations_since_last_state > 0:
		msg = world_state.observations[-1].text
		observations = json.loads(msg)
		return True
	return False

def coords(i, j):
	return 5*(i+2) + j + 2

'''
def walkDirection(offset):
	TIME = 2
	updateState()
	
	print("New Walk:")
	print("\tCurrent x: {}".format(observations["XPos"]))
	print("\tCurrent z: {}".format(observations["ZPos"]))
	
	TargetX = float(int(floor(observations["XPos"]))) + 0.5
	TargetZ = float(int(floor(observations["ZPos"]))) + 0.5
	
	
	
	print("\tTarget x: {}".format(TargetX))
	print("\tTarget z: {}".format(TargetZ))
	
	
	rawYaw = observations["Yaw"] + 180.0 + offset
	yaw = rawYaw % 360
	yaw -= 180
	yaw = offset
	#Negative Z
	if (abs(yaw) >= 135):
		TargetZ -= 1
	#Positive Z
	elif (abs(yaw) <= 45):
		TargetZ += 1
	#Negative X
	elif (yaw > 0):
		TargetX -= 1
	#Positive X
	else:
		TargetX += 1
	
		
	print("\tTarget x: {}".format(TargetX))
	print("\tTarget z: {}".format(TargetZ))
	
	x = observations["XPos"] - TargetX
	z = observations["ZPos"] - TargetZ
	
	distance = 0
	
	if (abs(x) > abs(z)):
		distance = abs(x)
	else:
		distance = abs(z)
	
	#distance = sqrt(((observations["XPos"] - TargetX)**2) + ((observations["ZPos"] - TargetZ)**2))
	print("\t\tDistance: {}".format(distance))
	speedMod = 1 / (4.3 * TIME)
	move =  distance * speedMod
	strafe =  distance * speedMod

	
	
	if (abs(x) > abs(z)):
		agent_host.sendCommand("move {}".format(move))
	
	else:
		agent_host.sendCommand("strafe {}".format(strafe))
		
	time.sleep(TIME-.025)
		
	agent_host.sendCommand("strafe 0")
	agent_host.sendCommand("move 0")

agent_host.sendCommand("pitch 1") #Start looking downward slowly
time.sleep(1.5)                        #Wait a second until we are looking in roughly the right direction
agent_host.sendCommand("pitch 0")    #Stop tilting the camera


'''

while world_state.is_mission_running:

	updateState()
	i = randrange(0,8)
	#Walk Forward
	if (i == 0):
		#walkDirection(-180)
		agent_host.sendCommand("move 1")
	#Walk Left
	elif (i == 1):
		#walkDirection(0)
		agent_host.sendCommand("strafe -1")
	#Walk Right
	elif (i == 2):
		#walkDirection(-90)
		agent_host.sendCommand("strafe 1")
	#Walk Backward
	elif (i == 3):
		#walkDirection(90)
		agent_host.sendCommand("move -1")
	#Jump Forward
	elif (i == 4):
		#walkDirection(-180)
		agent_host.sendCommand("move 1")
		agent_host.sendCommand("move 1")
	#Jump Left
	elif (i == 5):
		#walkDirection(0)
		agent_host.sendCommand("strafe -1")
		agent_host.sendCommand("strafe -1")
	#Jump Right
	elif (i == 6):
		#walkDirection(-90)
		agent_host.sendCommand("strafe 1")
		agent_host.sendCommand("strafe 1")
	#Jump Backward
	elif (i == 7):
		#walkDirection(90)
		agent_host.sendCommand("move -1")
		agent_host.sendCommand("move -1")
	if (i <= 3):
		time.sleep(0.25)
	else:
		print ("jumped")
		time.sleep(0.6)
	updateState()
	print("x: {}".format(int(observations["XPos"])))
	print("z: {}".format(int(observations["ZPos"])))
	grid = observations.get(u'floor', 0)
	floorGrid = []
	for g in grid:
		if (g == "air"):
			floorGrid.append(0)
		else:
			floorGrid.append(1)
	
	for i in range (-2,3):
		for j in range(-2,3):
			print(floorGrid[coords(i,j)],end="\t")
		print()
	
	print()

print()
print("Mission ended")
# Mission has ended.
