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
from PolicyLearning import *

key = [ \
"0131010", \
"0111010", \
"0013110", \
"0101110", \
"0113130", \
"0110100", \
"0113130", \
"0111110", \
"0101300", \
"0111310", \
"0301110", \
"0112110"  \
]

blockTypes = ["air", "stone", "gold_block", "redstone_block"]
spawn = {'x': 0, 'y': 55, 'z': 0}
def drawBlock(type, x, y, z):
	return '<DrawBlock x="{}" y="{}" z="{}" type="{}"/>\n'.format(x,y,z,type)

def makeMaze(key):
	global spawn
	z = -1;
	x = -(int(len(key[0])/2))
	y = 55
	result = ""
	for row in key:
		for block in row:
			type = blockTypes[int(block)]
			result += drawBlock(type, x, y, z)
			if (type == "gold_block"):
				spawn['x'] = x+0.5
				spawn['y'] = y+1
				spawn['z'] = z+0.5
			x += 1
		x = -(int(len(key[0])/2))
		z -= 1
	return result

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
				  <DrawingDecorator>
					<DrawCuboid x1="-20" y1="2" z1="-20" x2="20" y2="55" z2="5" type="air"/>
					''' + makeMaze(key) + '''
					<DrawCuboid x1="-20" y1="55" z1="0" x2="20" y2="55" z2="3" type="emerald_block"/>
				  </DrawingDecorator>
				  <ServerQuitWhenAnyAgentFinishes/>
				</ServerHandlers>
			  </ServerSection>
			  
			  <AgentSection mode="Creative">
				<Name>MalmoTutorialBot</Name>
				<AgentStart>
					''' + '<Placement x="{}" y="{}" z="{}" yaw="0"/>'.format(spawn['x'],spawn['y'],spawn['z']) + '''
				</AgentStart>
				<AgentHandlers>
				  <ObservationFromFullStats/>
				  <ObservationFromGrid>
					  <Grid name="floor">
						<min x="-2" y="-1" z="-2"/>
						<max x="2" y="-1" z="2"/>
					  </Grid>
				  </ObservationFromGrid>
				  <AbsoluteMovementCommands/>
				  <DiscreteMovementCommands/>
				  <InventoryCommands/>
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

def setup():
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
	updateState()
	while(not "observations" in globals()):
		updateState()
		time.sleep(0.01)
	agent_host.sendCommand("tp 0.5 56 -3.5")
	

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

def printFloor(floorGrid):
	for i in range (-2,3):
		for j in range(-2,3):
			print(floorGrid[coords(i,j)],end="\t")
		print()
	print()
	
def getFloor():
	grid = observations.get(u'floor', 0)
	floorGrid = []
	for g in grid:
		if (g == "air"):
			floorGrid.append(0)
		elif (g == "redstone_block"):
			floorGrid.append(2)
		else:
			floorGrid.append(1)
	return floorGrid
	
def purgatory(x, z):
	count = 0
	while(True):
		if (updateState()):
			if (count == 10):
				return
			count += 1
			if (observations["XPos"] == x):
				if (observations["ZPos"] == z):
					return
		time.sleep(0.05)

def movementLoop(p):
	steps = 0
	while world_state.is_mission_running:
		updateState()
		x = observations["XPos"]
		z = observations["ZPos"]
		floorGrid = getFloor()
		i = p.step(floorGrid)
		#print("      Command: {}".format(i))
		#Walk Forward
		if (i == 0):
			#walkDirection(-180)
			agent_host.sendCommand("move 1")
			z += 1
		#Walk Left
		elif (i == 1):
			#walkDirection(0)
			agent_host.sendCommand("strafe -1")
			x += 1
		#Walk Right
		elif (i == 2):
			#walkDirection(-90)
			agent_host.sendCommand("strafe 1")
			x -= 1
		#Walk Backward
		#elif (i == 3):
			#walkDirection(90)
			#agent_host.sendCommand("move -1")
			#z -= 1
		#Jump Forward
		elif (i == 3):
			#walkDirection(-180)
			agent_host.sendCommand("jumpmove 1")
			agent_host.sendCommand("move 1")
			z += 2
		#Jump Left
		elif (i == 4):
			#walkDirection(0)
			agent_host.sendCommand("jumpstrafe -1")
			agent_host.sendCommand("strafe -1")
			x += 2
		#Jump Right
		elif (i == 5):
			#walkDirection(-90)
			agent_host.sendCommand("jumpstrafe 1")
			agent_host.sendCommand("strafe 1")
			x -= 2
		#Jump Backward
		#elif (i == 7):
			#walkDirection(90)
			#agent_host.sendCommand("jumpmove -1")
			#agent_host.sendCommand("move -1")
			#z -= 2
		
		if (i <= 3):
			steps += 1
		else:
			#print ("jumped")
			steps += 2
		#time.sleep(.5)
		#updateState()
		#print("      steps: {}".format(steps))
		#while(not updateState()):
			#time.sleep(0.05)
		#time.sleep(0.25)
		#print("      x: {}".format(x))
		#print("      z: {}".format(z))
		purgatory(x,z)
		floorGrid = getFloor()
			
		#printFloor(floorGrid)
		dead = False;
		if (floorGrid[coords(0,0)] == 0):
			dead = True
		elif (floorGrid[coords(0,0)] == 2):
			i = random.randrange(10)
			if (i < 2):
				dead = True
				
		distance = observations["ZPos"]
		done = False
		if dead :
			done = True
		if distance >= 0:
			done = True
			distance = 0.0
		if steps >= 20:
			done = True
			
		p.update(abs(distance), steps, done)
		
		if done:
			return
	exit()

if __name__ == "__main__":
	setup()
	agent_host.sendCommand("look 1")
	#agent_host.sendCommand("look 1")
	agent_host.sendCommand("tp {} {} {}".format(spawn['x'],spawn['y'],spawn['z']))
	purgatory(spawn['x'],spawn['z'])
	p = PolicyLearner()
	episode = 0;
	while(True):
		episode += 1
		print("Episode: {}".format(episode))
		movementLoop(p)
		p.learn()
		#print("    Succeeded: {}".format(stats[0]))
		#print("      Distance: {}".format(stats[1]))
		#print("      Steps: {}".format(stats[2]))
		agent_host.sendCommand("tp {} {} {}".format(spawn['x'],spawn['y'],spawn['z']))
		purgatory(spawn['x'],spawn['z'])
	print()
	print("Mission ended")
	# Mission has ended.
