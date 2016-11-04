import sys
import random
import time


sys.path.append("/home/laurynas/workspace/ai_mc/Malmo-0.17.0-Linux-Ubuntu-14.04-64bit/Python_Examples")
import MalmoPython


#create default objects
agent_host = MalmoPython.AgentHost()

my_mission = MalmoPython.MissionSpec()
my_mission_record = MalmoPython.MissionRecordSpec()


#try to start mission
max_retries = 5
for retry in range(max_retries):
	try:
		agent_host.startMission(my_mission, my_mission_record)
		break
	except RuntimeError as e:
		if retry == max_retries - 1:
			print "Error starting mission", e
			exit(1)
		else:
			time.sleep(2)

# Loop until mission starts:
print "Waiting for the mission to start ",
state_t = agent_host.getWorldState()
while not state_t.has_mission_begun:
	sys.stdout.write(".")
	time.sleep(0.1)
	state_t = agent_host.getWorldState()
	for error in state_t.errors:
		print "Error:", error.text

random.seed(1)
agentPitchConfusionLevel = 0.1
agentMoveConfusionLevel = 0.1
agentTurnConfusionLevel = 0.1

while state_t.is_mission_running:
	
	# This is a random agent
	try:
		# Random hardwired moves for demo only
		agent_host.sendCommand("pitch " + str(agentPitchConfusionLevel*(random.random()*2-1))) # 0: look straigh ahead
		agent_host.sendCommand("move "  + str(agentMoveConfusionLevel*(random.random()*2-1))) # 1: means: move forward as fast as possible (in direction of sight)
		agent_host.sendCommand("turn "  + str(agentTurnConfusionLevel*(random.random()*2-1))) # start turing in a random direction, rather slowly
	except RuntimeError as e:
		print "Failed to send command:",e
		pass
	
	# Wait 0.5 sec 
	time.sleep(0.5)
		
	# Set the world state
	state_t = agent_host.getWorldState()
	
	# Stop movement
	if state_t.is_mission_running:
		# Enforce a simple discrete behavior by stopping any continuous movement in progress
		agent_host.sendCommand("move "  + str(0))
		agent_host.sendCommand("pitch " + str(0))
		agent_host.sendCommand("turn "  + str(0))

	# Check if anything went wrong along the way
	for error in state_t.errors:
		print "Error:",error.text

