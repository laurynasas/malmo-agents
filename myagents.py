""" 
 Artificial Inteligence 4 
 Assessed Exercise 2016/2017
 
 Solution Template (revision b)
"""


# ----------------------------------------------------------------------------------------------------------------#
class SolutionReport(object):
    # Please do not modify this custom class !
    def __init__(self):
        """ Constructor for the solution info 
        class which is used to store a summary of 
        the mission and agent performance """

        self.start_datetime_wallclock = None;
        self.end_datetime_wallclock = None;
        self.action_count = 0;
        self.reward_cumulative = 0;
        self.mission_xml = None;
        self.mission_type = None;
        self.mission_seed = None;
        self.student_guid = None;
        self.mission_xml_as_expected = None;
        self.is_goal = None;
        self.is_timeout = None;

    def start(self):
        self.start_datetime_wallclock = datetime.datetime.now()

    def stop(self):
        self.checkGoal()
        self.end_datetime_wallclock = datetime.datetime.now()

    def setMissionXML(self, mission_xml):
        self.mission_xml = mission_xml

    def setMissionType(self, mission_type):
        self.mission_type = mission_type

    def setMissionSeed(self, mission_seed):
        self.mission_seed = mission_seed

    def setStudentGuid(self, student_guid):
        self.student_guid = student_guid

    def addAction(self):
        self.action_count += 1

    def addReward(self, reward, datetime_):
        self.reward_cumulative += reward

    def checkMissionXML(self):
        """ This function is part of the final check"""
        # -- It is not included for simplifity --#
        self.mission_xml_as_expected = 'Unknown'

    def checkGoal(self):
        """ This function checks if the goal has been reached based on the expected reward structure (will not work if you change the mission xml!)"""
        # -- It is not included for simplifity --#
        if self.reward_cumulative != None:
            x = round((abs(self.reward_cumulative) - abs(round(self.reward_cumulative))) * 100);
            rem_goal = x % 25
            rem_timeout = x % 20
            if rem_goal == 0 and x != 0:
                self.is_goal = True
            else:
                self.is_goal = False

            if rem_timeout == 0 and x != 0:
                self.is_timeout = True
            else:
                self.is_timeout = False

# ----------------------------------------------------------------------------------------------------------------#


class StateSpace(object):
    """ This is a datatype used to collect a number of important aspects of the environment
    It can be build online or be created offline using the Helper Agent
    
    You are welcome to modify or change it as you see fit
    
    """

    def __init__(self):
        """ Constructor for the local state-space representation derived from the Orcale"""
        self.state_locations = None;
        self.state_actions = None;
        self.start_id = None;  # The id assigned to the start state
        self.goal_id = None;  # The id assigned to the goal state
        self.start_loc = None;  # The real word coordinates of the start state
        self.goal_loc = None;  # The real word coordinates of the goal state
        self.reward_states_n = None
        self.reward_states = None
        self.reward_sendcommand = None
        self.reward_timeout = None
        self.timeout = None


# ----------------------------------------------------------------------------------------------------------------#
def GetMissionInstance(mission_type, mission_seed, agent_type):
    """ Creates a specific instance of a given mission type """

    nir = {
        'small': 3,
        'medium': 24,
        'large': 192,
    }
    msize = {
        'small': 25,
        'medium': 50,
        'large': 100,
    }
    mtimeout = {
        'helper': 120000,
        'small': 60000,
        'medium': 120000,
        'large': 240000,
    }
    mission_type_tmp = mission_type
    if agent_type.lower() == 'helper':
        mission_type_tmp = agent_type.lower()

    # -- Define various parameters used in the generation of the mission --#
    # -- HINT: It is  crucial that you understand the details of the mission, this will require some knowledge of uncertainty/probability and random variables --#
    random.seed(mission_seed)
    reward_goal = abs(round(random.gauss(1000, 400))) + 0.25
    reward_diamond = round(random.gauss(4, 10))
    reward_timeout = -round(abs(random.gauss(1000, 400))) + 0.20
    reward_sendcommand = -random.randrange(2, 10)

    n_intermediate_rewards = random.randrange(1, 5) * nir.get(mission_type, 10)  # How many intermediate rewards...?

    xml_str = '''<?xml version="1.0" encoding="UTF-8" ?>
        <Mission xmlns="http://ProjectMalmo.microsoft.com" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
          <About>
            <Summary>Mission for assessed exercise 2016/2017 University of Glasgow</Summary>
          </About>
          <ServerSection>
            <ServerInitialConditions>
              <Time>
                <StartTime>10</StartTime>
                <AllowPassageOfTime>false</AllowPassageOfTime>
              </Time>
              <Weather>clear</Weather>
              <AllowSpawning>false</AllowSpawning>
            </ServerInitialConditions>
            <ServerHandlers>
              <FlatWorldGenerator generatorString="3;7,220*1,5*3,2;3;,biome_1" />      
              <MazeDecorator>
                <Seed>''' + str(mission_seed) + '''</Seed>
                <SizeAndPosition length="''' + str(msize.get(mission_type, 100)) + '''" width="''' + str(
        msize.get(mission_type, 100)) + '''" yOrigin="215" zOrigin="0" xOrigin="0" height="180"/>
                <GapProbability variance="0.3">0.2</GapProbability>        
                <MaterialSeed>1</MaterialSeed>
                <AllowDiagonalMovement>false</AllowDiagonalMovement>
                <StartBlock fixedToEdge="true" type="emerald_block" height="1"/>
                <EndBlock fixedToEdge="true" type="redstone_block" height="12"/>
                <PathBlock type="glowstone" colour="WHITE ORANGE MAGENTA LIGHT_BLUE YELLOW LIME PINK GRAY SILVER CYAN PURPLE BLUE BROWN GREEN RED BLACK" height="1"/>
                <FloorBlock type="air"/>
                <SubgoalBlock type="glowstone"/>        
                <GapBlock type="stained_hardened_clay" colour="WHITE ORANGE MAGENTA LIGHT_BLUE YELLOW LIME PINK GRAY SILVER CYAN PURPLE BLUE BROWN GREEN RED BLACK" height="3"/>
                <Waypoints quantity="''' + str(n_intermediate_rewards) + '''">
                  <WaypointItem type="diamond"/>          
                </Waypoints>      
              </MazeDecorator>      
              <ServerQuitFromTimeUp timeLimitMs="''' + str(mtimeout.get(mission_type_tmp, 0)) + '''" description="out_of_time"/>
              <ServerQuitWhenAnyAgentFinishes />
            </ServerHandlers>
          </ServerSection>
          <AgentSection>
            <Name>William Wallace by ''' + str(n_intermediate_rewards) + '''</Name>
            <AgentStart>
              <Placement x="0" y="216" z="90"/> <!-- will be overwritten by MazeDecorator -->
            </AgentStart>
            <AgentHandlers>
              <ObservationFromFullStats/>
              <ObservationFromRecentCommands/>
              <ObservationFromFullInventory/>
              <RewardForCollectingItem>                
                <Item reward="''' + str(reward_diamond) + '''" type="diamond"/>
              </RewardForCollectingItem>
              <RewardForSendingCommand reward="''' + str(reward_sendcommand) + '''"/>
              <RewardForMissionEnd rewardForDeath="-100000">
                <Reward description="found_goal" reward="''' + str(reward_goal) + '''" />
                <Reward description="out_of_time" reward="''' + str(reward_timeout) + '''" />
              </RewardForMissionEnd>
              <AgentQuitFromTouchingBlockType>
                <Block type="redstone_block" description="found_goal" />
              </AgentQuitFromTouchingBlockType>                           
            </AgentHandlers>    
          </AgentSection>
        </Mission>'''
    return xml_str, msize.get(mission_type,
                              100), reward_goal, reward_diamond, n_intermediate_rewards, reward_timeout, reward_sendcommand, mtimeout.get(
        mission_type_tmp, 0)


# ----------------------------------------------------------------------------------------------------------------#
# This function initialized the mission based on the input arguments
def init_mission(agent_host, port=0, agent_type='Unknown', mission_type='Unknown', mission_seed=0,
                 movement_type='Continuous'):
    """ Generate, and load the mission and return the agent host """

    # -- Set up the mission via XML definition --#
    mission_xml, msize, reward_goal, reward_intermediate, n_intermediate_rewards, reward_timeout, reward_sendcommand, timeout = GetMissionInstance(
        mission_type, mission_seed, agent_type)
    my_mission = MalmoPython.MissionSpec(mission_xml, True)
    my_mission.forceWorldReset()

    # -- Enforce the specific restriction for the assessed exercise --#
    # -- If you want a super agent, define one for you self  --#
    my_mission.setModeToCreative()
    if agent_type.lower() == 'random':
        n = msize
        my_mission.observeGrid(-n, -1, -n, n, -1, n, 'grid')
        my_mission.requestVideoWithDepth(320, 240)
    elif agent_type.lower() == 'simple':
        n = msize
        my_mission.observeGrid(-n, -1, -n, n, -1, n, 'grid');
        my_mission.requestVideo(320, 240)
    elif agent_type.lower() == 'realistic':
        n = 1  # n=1 means local info only !
        my_mission.observeGrid(-n, -1, -n, n, -1, n, 'grid');
        my_mission.requestVideoWithDepth(320, 240)
        my_mission.observeFullInventory()
    elif agent_type.lower() == 'helper':
        n = 100
        my_mission.observeGrid(-n, -1, -n, n, -1, n, 'grid');
        my_mission.requestVideoWithDepth(320, 240)
    else:
        # -- Define a custom agent and add the sensors you need --#
        n = 100
        my_mission.observeGrid(-n, -1, -n, n, 1, n, 'grid');
        my_mission.requestVideoWithDepth(320, 240)

        # -- Add support for the specific movement type requested (and given the constraints of the assignment) --#
    # -- See e.g. http://microsoft.github.io/malmo/0.17.0/Schemas/MissionHandlers.html   --#
    if movement_type.lower() == 'absolute':
        my_mission.allowAllAbsoluteMovementCommands()
    elif movement_type.lower() == 'continuous':
        my_mission.allowContinuousMovementCommand('move')
        my_mission.allowContinuousMovementCommand('strafe')
        my_mission.allowContinuousMovementCommand('pitch')
        my_mission.allowContinuousMovementCommand('turn')
        my_mission.allowContinuousMovementCommand('crouch')
    elif movement_type.lower() == 'discrete':
        my_mission.allowDiscreteMovementCommand('turn')
        my_mission.allowDiscreteMovementCommand('move')
        my_mission.allowDiscreteMovementCommand('movenorth')
        my_mission.allowDiscreteMovementCommand('moveeast')
        my_mission.allowDiscreteMovementCommand('movesouth')
        my_mission.allowDiscreteMovementCommand('movewest')
        my_mission.allowDiscreteMovementCommand('look')

    # -- Get the resulting xml (and return in order to check that conditions match the report) --#
    final_xml = my_mission.getAsXML(True)

    # Set up a recording for later inspection
    my_mission_record = MalmoPython.MissionRecordSpec('tmp' + ".tgz")
    my_mission_record.recordRewards()
    my_mission_record.recordMP4(24, 400000)

    # -- Attempt to start a mission --#
    max_retries = 5
    for retry in range(max_retries):
        try:
            agent_host.startMission(my_mission, my_mission_record)
            break
        except RuntimeError as e:
            if retry == max_retries - 1:
                print("Error starting mission:", e)
                exit(1)
            else:
                time.sleep(2)

    # -- Loop until mission starts: --#
    print("Waiting for the mission to start ")
    state_t = agent_host.getWorldState()
    while not state_t.has_mission_begun:
        sys.stdout.write(".")
        time.sleep(0.1)
        state_t = agent_host.getWorldState()
        for error in state_t.errors:
            print("Error:", error.text)

    print
    print("Mission started (xml returned)... ")
    return final_xml, reward_goal, reward_intermediate, n_intermediate_rewards, reward_timeout, reward_sendcommand, timeout


# --------------------------------------------------------------------------------------
# -- This class implements the Realistic Agent --#
class AgentRealistic:
    def __init__(self, agent_host, agent_port, mission_type, mission_seed, solution_report, state_space_graph):
        """ Constructor for the realistic agent """
        self.AGENT_MOVEMENT_TYPE = 'Absolute'  # HINT: You can change this if you want {Absolute, Discrete, Continuous}
        self.AGENT_NAME = 'Realistic'

        self.agent_host = agent_host
        self.agent_port = agent_port
        self.mission_seed = mission_seed
        self.mission_type = mission_type
        self.state_space = None  # NOTE: The Realistic can not know anything about the state_space a priori !
        self.solution_report = solution_report  # Python is call by reference !
        self.solution_report.setMissionType(self.mission_type)
        self.solution_report.setMissionSeed(self.mission_seed)
        self.first_time_flag = True
        self.diamond_award = 30
        self.already_visited_reward = 10
        self.history = {}
        self.rewards_by_location_id = {}
        self.previous_rewards_total = 0

    def _convert_grid_arr_to_3x3matrix(self, grid):
        matrix = [[], [], []]

        for i in xrange(len(grid)):
            matrix[i / 3] += [grid[len(grid) - 1 - i]]
        return matrix

    def _get_current_location_id(self, location):
        return "S_" + str(int(location[0])) + "_" + str(int(location[1]))

    '''
    Gets and updates the rewards of all the possible actions from the current location.
    Finds out whether any neighbours have diamonds by teleporting to all possible states and checking for
    diamonds in the bag.
    '''

    def _get_rewards(self, rewards, state_space_actions, state_space_locations, observations,
                     previous_rewards_total):

        curr_loc_id = state_space_actions.keys()[0]
        actions = state_space_actions[curr_loc_id]

        if curr_loc_id not in rewards:
            rewards[curr_loc_id] = -random.randrange(2, 10)

        for action_id in actions.keys():
            real_location = state_space_locations[action_id]

            self.agent_host.sendCommand("tp " + str(real_location[0]) + " " + str(217) + " " + str(real_location[1]))

            if action_id not in rewards.keys():
                rewards[action_id] = -random.randrange(2, 10)

            if u'InventorySlot_0_item' in observations.keys() and observations['InventorySlot_0_item'] == u'diamond':
                if u'InventorySlot_1_item' in observations.keys() and observations[
                    'InventorySlot_1_item'] == u'diamond':
                    total_rewards = observations['InventorySlot_0_size'] + observations['InventorySlot_1_size']
                else:
                    total_rewards = observations['InventorySlot_0_size']

                if total_rewards != previous_rewards_total:
                    rewards[action_id] += self.diamond_award
                    previous_rewards_total += 1

        return rewards, previous_rewards_total

    '''
    Collects all the possible actions by checking the grid information around the agent. If the goal type of block
    is found the termination flag is returned.
    '''

    def _get_local_state_space_actions(self, grid, current_location):
        actions = {}
        locations = {}
        walkable_blocks = [u'glowstone', u'emerald_block']

        grid_matrix = self._convert_grid_arr_to_3x3matrix(grid)
        current_location_id = self._get_current_location_id(current_location)
        current_x = current_location[0]
        current_z = current_location[1]
        locations[current_location_id] = current_location

        if u'redstone_block' in [grid_matrix[0][1], grid_matrix[1][2], grid_matrix[2][1], grid_matrix[1][0]]:
            return dict(), dict(), True

        if grid_matrix[0][1] in walkable_blocks:
            this_location = (current_x, current_z + 1)
            location_id = self._get_current_location_id(this_location)
            actions[location_id] = 1
            locations[location_id] = this_location

        if grid_matrix[1][2] in walkable_blocks:
            this_location = (current_x - 1, current_z)
            location_id = self._get_current_location_id(this_location)
            actions[location_id] = 1
            locations[location_id] = this_location

        if grid_matrix[2][1] in walkable_blocks:
            this_location = (current_x, current_z - 1)
            location_id = self._get_current_location_id(this_location)
            actions[location_id] = 1
            locations[location_id] = this_location

        if grid_matrix[1][0] in walkable_blocks:
            this_location = (current_x + 1, current_z)
            location_id = self._get_current_location_id(this_location)
            actions[location_id] = 1
            locations[location_id] = this_location

        return {current_location_id: actions}, locations, False

    '''
    The algorithm finds the neighbor node with the highest value and returns the node which will be the next step.
    The value method is slightly adjusted by taking into the account previous actions of the agent.
    '''

    def hill_climbing(self, problem, path_history):
        '''From the initial node, keep choosing the neighbor with highest value,
        stopping when no neighbor is better. [Figure 4.2]'''
        current = Node(problem.initial)
        while True:
            neighbors = current.expand(problem)
            if not neighbors:
                break
            neighbor = argmax_random_tie(neighbors,
                                         key=lambda node: problem.value(node.state, path_history))
            if problem.value(neighbor.state, path_history) <= problem.value(current.state, path_history):
                break
            current = neighbor
        return current.state

    def run_agent(self):
        """ Run the Realistic agent and log the performance and resource use """
        '''
        The child class is created in order to override the value method which will take into account
        previous states of the agent. The reward function is made exponential rather than linear, which
        decreases the probability of agent visiting the state which was already visited.
        '''

        class GraphProblemSpecialised(GraphProblem):
            def __init__(self, initial, goal, graph, reward_dict, already_visited_reward):
                GraphProblem.__init__(self, initial, goal, graph)
                self.rewards = reward_dict
                self.already_visited_reward = already_visited_reward

            def value(self, state, history):
                if state in history.keys():
                    return self.rewards[state] - (self.already_visited_reward ** history[state])
                return self.rewards[state]

        # -- Load and init mission --#
        print('Generate and load the ' + self.mission_type + ' mission with seed ' + str(
            self.mission_seed) + ' allowing ' + self.AGENT_MOVEMENT_TYPE + ' movements')
        mission_xml = init_mission(self.agent_host, self.agent_port, self.AGENT_NAME, self.mission_type,
                                   self.mission_seed, self.AGENT_MOVEMENT_TYPE)
        self.solution_report.setMissionXML(mission_xml)
        self.solution_report.start()

        # -- Get the state of the world along with internal state...  --#
        state_t = self.agent_host.getWorldState()

        # -- Main loop: --#
        while state_t.is_mission_running:
            state_t = self.agent_host.getWorldState()

            # -- Check if anything went wrong along the way  --#
            for error in state_t.errors:
                print("Error:", error.text)

            # -- Oracle and Internal Sensors--#
            if state_t.number_of_observations_since_last_state > 0:  # Has any Oracle-like and/or internal sensor observations come in?
                msg = state_t.observations[-1].text  # Get the details for the last observed state
                oracle_and_internal = json.loads(msg)  # Parse the Oracle JSON
                # print oracle_and_internal
                # -- Oracle sensor --#
                grid = oracle_and_internal.get(u'grid', 0)  # Demo only, string with the
                # -- GPS-like sensor  --#
                xpos = oracle_and_internal.get(u'XPos', 0)  # Demo only, position in 2D plane, 1st axis
                zpos = oracle_and_internal.get(u'ZPos', 0)  # Demo only, position in 2D plane, 2nd axis (yes Z!)
                ypos = oracle_and_internal.get(u'YPos', 0)  # Demo only, height as measured from surface! (yes Y!)

                current_location_id = self._get_current_location_id((xpos, zpos))

                if self.history.get(current_location_id):
                    self.history[current_location_id] += 1
                else:
                    self.history[current_location_id] = 1

                if self.first_time_flag:
                    start_location = current_location_id

                # Gets the possible actions and checks for goal block
                state_space_actions, state_space_locations, reached_goal = self._get_local_state_space_actions(grid,
                                                                                                               [xpos,
                                                                                                                zpos])

                if reached_goal:
                    break

                self.rewards_by_location_id, self.previous_rewards_total = self._get_rewards(
                    self.rewards_by_location_id,
                    state_space_actions,
                    state_space_locations,
                    oracle_and_internal,
                    self.previous_rewards_total)

                # Creates a graph for local (neighbourhood) actions
                local_map = UndirectedGraph(state_space_actions)
                local_problem = GraphProblemSpecialised(initial=start_location, goal=None, graph=local_map,
                                                        reward_dict=self.rewards_by_location_id,
                                                        already_visited_reward=self.already_visited_reward)
                # Looks for most optimal next step
                next_step = self.hill_climbing(local_problem, self.history)

                # If the next step is already in history the reward will be exponentially increased (but is negated)
                if next_step in self.history.keys():
                    print "You already visited that so will be punished!"
                    self.rewards_by_location_id[next_step] -= self.already_visited_reward ** self.history[next_step]
                    self.history[next_step] += 1

                next_x, next_z = state_space_locations[next_step]
                self.agent_host.sendCommand("tp " + str(next_x) + " " + str(217) + " " + str(next_z))
                time.sleep(0.1)

                # -- Collect the number of rewards and add to reward_cumulative  --#
                # -- Note: Since we only observe the sensors and environment every a number of rewards may have accumulated in the buffer  --#
                for reward_t in state_t.rewards:
                    print("Reward_t:", reward_t.getValue())
                    self.solution_report.addReward(reward_t.getValue(), datetime.datetime.now())

                # -- Check if anything went wrong along the way  --#
                for error in state_t.errors:
                    print("Error:", error.text)

        print("Mission has ended.either because time has passed or you reached the goal.")
        return


# --------------------------------------------------------------------------------------
# -- This class implements the Simple Agent --#
class AgentSimple:
    def __init__(self, agent_host, agent_port, mission_type, mission_seed, solution_report, state_space):
        """ Constructor for the simple agent """
        self.AGENT_MOVEMENT_TYPE = 'Discrete'  # HINT: You can change this if you want {Absolute, Discrete, Continuous}
        self.AGENT_NAME = 'Simple'

        self.agent_host = agent_host
        self.agent_port = agent_port
        self.mission_seed = mission_seed
        self.mission_type = mission_type
        self.state_space = state_space
        self.solution_report = solution_report  # Python calls by reference !
        self.solution_report.setMissionType(self.mission_type)
        self.solution_report.setMissionSeed(self.mission_seed)

    '''
    Creates a maze graph from state space information and applies astar search to find the shortest path to the goal
    block whose location is known.
    '''

    def _find_solution_path(self, state_space):
        maze_map = UndirectedGraph(state_space.state_actions)
        maze_map_locations = state_space.state_locations
        graph = nx.Graph()

        start_location = maze_map_locations.keys()[maze_map_locations.values().index(state_space.start_loc)]
        goal_location = maze_map_locations.keys()[maze_map_locations.values().index(state_space.goal_loc)]

        maze_problem = GraphProblem(start_location, goal_location, maze_map)

        goal_node = astar_search(problem=maze_problem, h=None)

        solution_path = [goal_node]
        parent_node = goal_node.parent
        solution_path.append(parent_node)

        # Creates the list with actions to be taken
        while parent_node.state != start_location:
            parent_node = parent_node.parent
            solution_path.append(parent_node)

        return solution_path, start_location, goal_location, maze_map_locations

    '''
    Finds the relative turning direction in order to make the movement of agent more realistic. The latter is
    calculated according to previous coordinates and coordinates after the action had been taken
    '''

    def get_turn_direction(self, old_co, new_co, facing_direction):
        dx = new_co[0] - old_co[0]
        dz = new_co[1] - old_co[1]
        new_facing_direction = (dx, dz)

        if old_co == new_co:
            return 0, facing_direction

        if facing_direction == new_facing_direction:
            return 0, new_facing_direction

        if new_facing_direction[0] == 0:
            return new_facing_direction[1] * facing_direction[0], new_facing_direction

        return -new_facing_direction[0] * facing_direction[1], new_facing_direction

    def run_agent(self):
        """ Run the Simple agent and log the performance and resource use """

        # -- Load and init mission --#
        print('Generate and load the ' + self.mission_type + ' mission with seed ' + str(
            self.mission_seed) + ' allowing ' + self.AGENT_MOVEMENT_TYPE + ' movements')
        mission_xml = init_mission(self.agent_host, self.agent_port, self.AGENT_NAME, self.mission_type,
                                   self.mission_seed, self.AGENT_MOVEMENT_TYPE)
        self.solution_report.setMissionXML(mission_xml)
        self.solution_report.start()

        state_t = self.agent_host.getWorldState()

        # Finds the solution path and all other relative information
        (solution_path, start_location, goal_location, maze_map_locations) = self._find_solution_path(self.state_space)

        x_old, z_old = maze_map_locations[start_location]

        # Shifts the teleportation coordinates so that agent does not get stuck
        x_old += 0.5
        z_old += 0.5

        # Initial facing direction, assumption that initially agent is always facing this direction
        facing_direction = (0, 1)

        # -- Main loop checks if there are more actions to execute: --#
        while state_t.is_mission_running and solution_path:

            target_node = solution_path.pop()
            x_new, z_new = maze_map_locations[target_node.state]

            # Shifts the teleportation coordinates so that agent does not get stuck
            x_new = float(x_new) + 0.5
            z_new = float(z_new) + 0.5

            old_co = (x_old, z_old)
            new_co = (x_new, z_new)

            turn_direction, facing_direction = self.get_turn_direction(old_co, new_co, facing_direction)

            self.agent_host.sendCommand("turn " + str(turn_direction))
            time.sleep(0.2)

            # Apparently agent must perform the moving forward command in order for the turn teleportation to work,
            self.agent_host.sendCommand(
                "move " + str(1))  # 1: means: move forward as fast as possible (in direction of sight)

            self.agent_host.sendCommand("tp " + str(x_new) + " " + str(217) + " " + str(z_new))

            x_old = x_new
            z_old = z_new

            # -- Collect the number of rewards and add to reward_cumulative  --#
            # -- Note: Since we only observe the sensors and environment every a number of rewards may have accumulated in the buffer  --#
            for reward_t in state_t.rewards:
                self.solution_report.addReward(reward_t.getValue(), datetime.datetime.now())

            # -- Check if anything went wrong along the way  --#
            for error in state_t.errors:
                print("Error:", error.text)

        print("Mission has ended.either because time has passed or you reached the goal.")
        return


# --------------------------------------------------------------------------------------
# -- This class implements a basic, suboptimal Random Agent --#
class AgentRandom:
    def __init__(self, agent_host, agent_port, mission_type, mission_seed, solution_report, state_space_graph):
        """ Constructor for the Random agent """
        self.AGENT_MOVEMENT_TYPE = 'Continuous'
        self.AGENT_NAME = 'Random'

        self.agent_host = agent_host
        self.agent_port = agent_port
        self.mission_seed = mission_seed
        self.mission_type = mission_type
        self.state_space = state_space
        self.solution_report = solution_report  # Python makes call by reference !
        self.solution_report.setMissionType(self.mission_type)
        self.solution_report.setMissionSeed(self.mission_seed)

    def run_agent(self):
        """ Run the Random agent and log the performance and resource use """

        # -- Load and init mission --#
        print('Generate and load the ' + self.mission_type + ' mission with seed ' + str(
            self.mission_seed) + ' allowing ' + self.AGENT_MOVEMENT_TYPE + ' movements')
        mission_xml, reward_goal, reward_intermediate, n_intermediate_rewards, reward_timeout, reward_sendcommand, timeout = init_mission(
            self.agent_host, self.agent_port, self.AGENT_NAME, self.mission_type, self.mission_seed,
            self.AGENT_MOVEMENT_TYPE)
        self.solution_report.setMissionXML(mission_xml)

        # -- Define local capabilities of the agent (sensors)--#
        self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
        self.agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
        self.agent_host.setRewardsPolicy(MalmoPython.RewardsPolicy.KEEP_ALL_REWARDS)

        time.sleep(0.5)

        self.solution_report.start()

        # -- Get the state of the world along with internal state...  --#
        state_t = self.agent_host.getWorldState()
        # -- Set the randomness of the agent by seeding the random number generator --#
        agent_confusement_level = 0.8

        # -- Main loop: --#
        while state_t.is_mission_running:
            # -- This is a random agent --#
            try:
                # -- Random hardwired moves --#
                self.agent_host.sendCommand("pitch " + str(0))  # 0: look straigh ahead
                self.solution_report.addAction()

                self.agent_host.sendCommand(
                    "move " + str(1))  # 1: means: move forward as fast as possible (in direction of sight)
                self.solution_report.addAction()

                self.agent_host.sendCommand("turn " + str(agent_confusement_level * (
                    random.random() * 2 - 1)))  # start turning in a random direction, rather slowly
                self.solution_report.addAction()
            except RuntimeError as e:
                print("Failed to send command:", e)
                pass

            # -- Wait 0.5 sec --#
            time.sleep(0.5)

            # -- Set the world state --#
            state_t = self.agent_host.getWorldState()

            # -- Stop movement --#
            if state_t.is_mission_running:
                # -- Enforce a simple discrete behavior by stopping any continuous movement in progress --#
                self.agent_host.sendCommand("move " + str(0))
                self.solution_report.addAction()

                self.agent_host.sendCommand("pitch " + str(0))
                self.solution_report.addAction()

                self.agent_host.sendCommand("turn " + str(0))
                self.solution_report.addAction()

            # -- Collect the number of rewards and add to reward_cumulative  --#
            # -- Note: Since we only observe the sensors and environment every a number of rewards may have accumulated in the buffer  --#
            for reward_t in state_t.rewards:
                print("Reward_t:", reward_t.getValue())
                self.solution_report.addReward(reward_t.getValue(), datetime.datetime.now())

            # -- Check if anything went wrong along the way  --#
            for error in state_t.errors:
                print("Error:", error.text)

            # -- Handle the percepts/sensors  --#
            xpos = None
            ypos = None
            zpos = None
            yaw = None
            pitch = None
            grid = None

            # -- Oracle and Internal Sensors--#
            if state_t.number_of_observations_since_last_state > 0:  # Has any Oracle-like and/or internal sensor observations come in?
                msg = state_t.observations[-1].text  # Get the details for the last observed state
                oracle_and_internal = json.loads(msg)  # Parse the Oracle JSON

                # -- Oracle sensor --#
                grid = oracle_and_internal.get(u'grid', 0)  # Demo only, string with the

                # -- GPS-like sensor  --#
                xpos = oracle_and_internal.get(u'XPos', 0)  # Demo only, position in 2D plane, 1st axis
                zpos = oracle_and_internal.get(u'ZPos', 0)  # Demo only, position in 2D plane, 2nd axis (yes Z!)
                ypos = oracle_and_internal.get(u'YPos', 0)  # Demo only, height as measured from surface! (yes Y!)

                # -- Standard "internal" sensory inputs --#
                yaw = oracle_and_internal.get(u'Yaw', 0)
                pitch = oracle_and_internal.get(u'Pitch', 0)

                # -- Vision sensor --#
            if state_t.number_of_video_frames_since_last_state > 0:  # Has any Vision percepts been registred ?
                frame = state_t.video_frames[0]
                # Uncomment this code for gaining access to the vision of the agent
                # img = Image.frombytes('RGB', (frame.width,frame.height), str(frame.pixels) )
                # red, green, blue = img.split()
                # img.show()
                # red.show()
                # green.show()
                # blue.show()
                # Oracle
                # Depth: Your can get a pre-computed depth image the state_t.video_frames[0].pixels

            # -- Print some of the state information --#
            print("video,observations,rewards received:", state_t.number_of_video_frames_since_last_state,
                  state_t.number_of_observations_since_last_state, state_t.number_of_rewards_since_last_state)
            print("\t x,y,z,yaw,pitch:", xpos, ypos, zpos, yaw, pitch)
            # print('\tRadius X surroundings: ' + str(grid))

        print(
            "Mission has ended ... either because time has passed (negative reward) or goal reached (positive reward)")
        return


# --------------------------------------------------------------------------------------
# -- This class implements a helper Agent for deriving the state-space representation ---#
class AgentHelper:
    """ This agent determines the state space for use by the actual problem solving agent. Enabeling do_plot will allow you to visualize the results """

    def __init__(self, agent_host, agent_port, mission_type, mission_seed, solution_report, state_space_graph):
        """ Constructor for the helper agent """
        self.AGENT_NAME = 'Helper'
        self.AGENT_MOVEMENT_TYPE = 'Absolute'  # Note the helper needs absolute movements

        self.agent_host = agent_host
        self.agent_port = agent_port
        self.mission_seed = mission_seed
        self.mission_type = mission_type
        self.state_space = StateSpace()
        self.solution_report = solution_report;  # Python is call by reference !
        self.solution_report.setMissionType(self.mission_type)
        self.solution_report.setMissionSeed(self.mission_seed)

    def run_agent(self):
        """ Run the Helper agent to get the state-space """
        do_plot = False

        # -- Load and init the Helper mission --#
        print('Generate and load the ' + self.mission_type + ' mission with seed ' + str(
            self.mission_seed) + ' allowing ' + self.AGENT_MOVEMENT_TYPE + ' movements')
        mission_xml, reward_goal, reward_intermediate, n_intermediate_rewards, reward_timeout, reward_sendcommand, timeout = init_mission(
            self.agent_host, self.agent_port, self.AGENT_NAME, self.mission_type, self.mission_seed,
            self.AGENT_MOVEMENT_TYPE)
        self.solution_report.setMissionXML(mission_xml)

        # -- Define local capabilities of the agent (sensors)--#
        self.agent_host.setObservationsPolicy(MalmoPython.ObservationsPolicy.LATEST_OBSERVATION_ONLY)
        self.agent_host.setVideoPolicy(MalmoPython.VideoPolicy.LATEST_FRAME_ONLY)
        self.agent_host.setRewardsPolicy(MalmoPython.RewardsPolicy.KEEP_ALL_REWARDS)

        time.sleep(1)

        # -- Get the state of the world along with internal agent state...--#
        state_t = self.agent_host.getWorldState()

        # -- Get a state-space model by observing the Orcale/GridObserver--#
        if state_t.is_mission_running:
            # -- Make sure we look in the right direction when observing the surrounding (otherwise the coordinate system will rotated by the Yaw !) --#
            # Look East (towards +x (east) and +z (south) on the right, i.e. a std x,y coordinate system) yaw=-90
            self.agent_host.sendCommand("setPitch 20")
            time.sleep(1)
            self.agent_host.sendCommand("setYaw -90")
            time.sleep(1)

            # -- Basic map --#
            state_t = self.agent_host.getWorldState()

            if state_t.number_of_observations_since_last_state > 0:
                msg = state_t.observations[-1].text  # Get the details for the last observed state
                oracle_and_internal = json.loads(msg)  # Parse the Oracle JSON
                grid = oracle_and_internal.get(u'grid', 0)
                xpos = oracle_and_internal.get(u'XPos', 0)
                zpos = oracle_and_internal.get(u'ZPos', 0)
                ypos = oracle_and_internal.get(u'YPos', 0)
                yaw = oracle_and_internal.get(u'Yaw', 0)
                pitch = oracle_and_internal.get(u'Pitch', 0)

                # -- Parste the JOSN string, Note there are better ways of doing this! --#
                full_state_map_raw = str(grid)
                full_state_map_raw = full_state_map_raw.replace("[", "")
                full_state_map_raw = full_state_map_raw.replace("]", "")
                full_state_map_raw = full_state_map_raw.replace("u'", "")
                full_state_map_raw = full_state_map_raw.replace("'", "")
                full_state_map_raw = full_state_map_raw.replace(" ", "")
                aa = full_state_map_raw.split(",")
                vocs = list(set(aa))
                for word in vocs:
                    for i in range(0, len(aa)):
                        if aa[i] == word:
                            aa[i] = vocs.index(word)

                X = np.asarray(aa);
                nn = int(math.sqrt(X.size))
                X = np.reshape(X, [nn, nn])  # Note: this matrix/table is index as z,x

                # -- Visualize the discrete state-space --#
                if do_plot:
                    print yaw
                    plt.figure(1)
                    imgplot = plt.imshow(X.astype('float'), interpolation='none')
                    plt.pause(4)
                    # plt.show()

                # -- Define the unique states available --#
                state_wall = vocs.index("stained_hardened_clay")
                state_impossible = vocs.index("stone")
                state_initial = vocs.index("emerald_block")
                state_goal = vocs.index("redstone_block")

                # -- Extract state-space --#
                offset_x = 100 - math.floor(xpos);
                offset_z = 100 - math.floor(zpos);

                state_space_locations = {};  # create a dict

                for i_z in range(0, len(X)):
                    for j_x in range(0, len(X)):
                        if X[i_z, j_x] != state_impossible and X[i_z, j_x] != state_wall:
                            state_id = "S_" + str(int(j_x - offset_x)) + "_" + str(int(i_z - offset_z))
                            state_space_locations[state_id] = (int(j_x - offset_x), int(i_z - offset_z))
                            if X[i_z, j_x] == state_initial:
                                state_initial_id = state_id
                                loc_start = state_space_locations[state_id]
                            elif X[i_z, j_x] == state_goal:
                                state_goal_id = state_id
                                loc_goal = state_space_locations[state_id]

                                # -- Generate state / action list --#
                # First define the set of actions in the defined coordinate system             
                actions = {"west": [-1, 0], "east": [+1, 0], "north": [0, -1], "south": [0, +1]}
                state_space_actions = {}
                for state_id in state_space_locations:
                    possible_states = {}
                    for action in actions:
                        # -- Check if a specific action is possible --#
                        delta = actions.get(action)
                        state_loc = state_space_locations.get(state_id)
                        state_loc_post_action = [state_loc[0] + delta[0], state_loc[1] + delta[1]]

                        # -- Check if the new possible state is in the state_space, i.e., is accessible --#
                        state_id_post_action = "S_" + str(state_loc_post_action[0]) + "_" + str(
                            state_loc_post_action[1])
                        if state_space_locations.get(state_id_post_action) != None:
                            possible_states[state_id_post_action] = 1

                            # -- Add the possible actions for this state to the global dict --#
                    state_space_actions[state_id] = possible_states

                # -- Kill the agent/mission --#
                agent_host.sendCommand("tp " + str(0) + " " + str(0) + " " + str(0))
                time.sleep(2)

                # -- Save the info an instance of the StateSpace class --
                self.state_space.state_actions = state_space_actions
                self.state_space.state_locations = state_space_locations
                self.state_space.start_id = state_initial_id
                self.state_space.start_loc = loc_start
                self.state_space.goal_id = state_goal_id
                self.state_space.goal_loc = loc_goal

            # -- Reward location and values --#
            # OPTIONAL: If you want to account for the intermediate rewards 
            # in the Random/Simple agent (or in your analysis) you can 
            # obtain ground-truth by teleporting with the tp command 
            # to all states and detect whether you recieve recieve a 
            # diamond or not using the inventory field in the oracle variable                        
            #
            # As default the state_space_rewards is just set to contain 
            # the goal state which is found above.
            #                               
            state_space_rewards = {}
            state_space_rewards[state_goal_id] = reward_goal

            # HINT: You can insert your own code for getting 
            # the location of the intermediate rewards
            # and populate the state_space_rewards dict 
            # with more information (optional). 
            # WARNING: This is a bit tricky, please consult tutors before starting

            # -- Set the values in the state_space container --#
            self.state_space.reward_states = state_space_rewards
            self.state_space.reward_states_n = n_intermediate_rewards + 1
            self.state_space.reward_timeout = reward_timeout
            self.state_space.timeout = timeout
            self.state_space.reward_sendcommand = reward_sendcommand
        else:
            self.state_space = None
            # -- End if observations --#

        return


# --------------------------------------------------------------------------------------------
# -- The main entry point if you run the module as a script--#
if __name__ == "__main__":

    # -- Define default arguments, in case you run the module as a script --#
    DEFAULT_STUDENT_GUID = 'template'
    DEFAULT_AGENT_NAME = 'Random'  # HINT: Currently choose between {Random,Simple, Realistic}
    DEFAULT_MALMO_PATH = '/home/laurynas/workspace/ai_mc/Malmo-0.17.0-Linux-Ubuntu-14.04-64bit/'  # HINT: Change this to your own path, forward slash only!
    DEFAULT_AIMA_PATH = '/home/laurynas/workspace/ai_lab/aima'  # HINT: Change this to your own path, forward slash only, should be the 2.7 version from https://www.dropbox.com/s/vulnv2pkbv8q92u/aima-python_python_v27_r001.zip?dl=0)
    DEFAULT_MISSION_TYPE = 'small'  # HINT: Choose between {small,medium,large}
    DEFAULT_MISSION_SEED_MAX = 1  # how many different instances of the given mission (i.e. maze layout)
    DEFAULT_REPEATS = 1
    DEFAULT_PORT = 0
    DEFAULT_SAVE_PATH = './results/'

    # -- Import required modules --#
    import sys
    import time
    import random
    import json
    import argparse
    import pickle
    import datetime
    import math
    import numpy as np
    from copy import deepcopy
    import matplotlib.pyplot as plt
    import networkx as nx

    # from Tkinter import * # only for showing the video input
    # import tkMessageBox  # only for showing the video input
    # from PIL import Image # only for showing the video input
    # from PIL import ImageTk # only for showing the video input

    # -- Define the commandline arguments required to run the agents from comman line --#
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--agentname", type=str, help="path for the malmo pyhton examples",
                        default=DEFAULT_AGENT_NAME)
    parser.add_argument("-t", "--missiontype", type=str, help="mission type (small,medium,large)",
                        default=DEFAULT_MISSION_TYPE)
    parser.add_argument("-s", "--missionseedmax", type=int, help="maximum mission seed value (integer)",
                        default=DEFAULT_MISSION_SEED_MAX)
    parser.add_argument("-n", "--nrepeats", type=int, help="repeat of a specific agent (if stochastic behavior)",
                        default=DEFAULT_REPEATS)
    parser.add_argument("-g", "--studentguid", type=str, help="student guid", default=DEFAULT_STUDENT_GUID)
    parser.add_argument("-p", "--malmopath", type=str, help="path for the malmo pyhton examples",
                        default=DEFAULT_MALMO_PATH)
    parser.add_argument("-x", "--malmoport", type=int, help="special port for the Minecraft client",
                        default=DEFAULT_PORT)
    parser.add_argument("-o", "--aimapath", type=str, help="path for the aima toolbox (optional)",
                        default=DEFAULT_AIMA_PATH)
    parser.add_argument("-r", "--resultpath", type=str, help="the path where the results are saved",
                        default=DEFAULT_SAVE_PATH)
    args = parser.parse_args()

    # -- Add the Malmo path  --#
    print('Add Malmo Python API/lib to the Python environment [' + args.malmopath + '/Python_Examples' + ']')
    sys.path.append(args.malmopath + '/Python_Examples')

    # -- Import the Malmo Python wrapper/module --#
    print('Import the Malmo module...')
    import MalmoPython

    # -- OPTIONAL: Import the AIMA tools (for representing the state-space)--#
    print('Add AIMA lib to the Python environment [' + args.aimapath + ']')
    sys.path.append(args.aimapath + '/')
    from search import *

    # -- Create the command line string for convenience --#
    cmd = 'python myagents.py -a ' + args.agentname + ' -s ' + str(args.missionseedmax) + ' -n ' + str(
        args.nrepeats) + ' -t ' + args.missiontype + ' -g ' + args.studentguid + ' -p ' + args.malmopath + ' -x ' + str(
        args.malmoport)
    print(cmd)

    # -- Run the agent a number of times (it only makes a difference if you agent has some random elemnt to it, initalizaiton, behavior etc) --#
    # -- HINT: It is quite important that you understand the need for the loops (and potentially others) --#

    print('Instantiate an agent interface/api to Malmo')
    agent_host = MalmoPython.AgentHost()

    for i_training_seed in range(0, args.missionseedmax):
        print('Get state-space representation using a AgentHelper regardless of the AgentType...')
        helper_solution_report = SolutionReport()
        helper_agent = AgentHelper(agent_host, args.malmoport, args.missiontype, i_training_seed,
                                   helper_solution_report, None)
        helper_agent.run_agent()

        for i_rep in range(0, args.nrepeats):
            print('Setup the performance log...')
            solution_report = SolutionReport()
            solution_report.setStudentGuid(args.studentguid)

            print(
                'Get an instance of the specific ' + args.agentname + ' agent with the agent_host and load the ' + args.missiontype + ' mission with seed ' + str(
                    i_training_seed))
            agent_name = 'Agent' + args.agentname
            state_space = deepcopy(helper_agent.state_space)

            agent_to_be_evaluated = eval(
                agent_name + '(agent_host,args.malmoport,args.missiontype,i_training_seed,solution_report,state_space)')

            print('Run the agent, time it and log the performance...')
            solution_report.start()  # start the timer (may be overwritten in the agent to provide a fair comparison)
            agent_to_be_evaluated.run_agent()
            solution_report.stop()  # stop the timer

            print("\n---------------------------------------------")
            print("| Solution Report Summary: ")
            print("|\tCumulative reward = " + str(solution_report.reward_cumulative))
            print("|\tDuration (wallclock) = " + str(
                (solution_report.end_datetime_wallclock - solution_report.start_datetime_wallclock).total_seconds()))
            print("|\tNumber of reported actions = " + str(solution_report.action_count))
            print("|\tFinal goal reached = " + str(solution_report.is_goal))
            print("|\tTimeout = " + str(solution_report.is_timeout))
            print("---------------------------------------------\n")

            print('Save the solution report to a specific file for later analysis and reporting...')
            fn_result = args.resultpath + 'solution_' + args.studentguid + '_' + agent_name + '_' + args.missiontype + '_' + str(
                i_training_seed) + '_' + str(i_rep)
            foutput = open(fn_result + '.pkl', 'wb')
            pickle.dump(agent_to_be_evaluated.solution_report,
                        foutput)  # Save the solution information in a specific file, HiNT:  It can be loaded with pickle.load(output) with read permissions to the file
            foutput.close()

            # finput = open(fn_result+'.pkl', 'rb')
            # res =  pickle.load(finput)
            # finput.close()

            print('Sleep a sec to make sure the client is ready for next mission/agent variation...')
            time.sleep(1)
            print("------------------------------------------------------------------------------\n")

    print("Done")
