# Allen Bronshtein 206228751
from Components import Learner

""" This part of our executive holds all the things he knows"""

NAME_OF_FIRST_ARGUMENT = "my_executive.py"
NAME_OF_SECOND_ARGUMENT1 = "-L"
NAME_OF_SECOND_ARGUMENT2 = "-E"
POLICY_FILE_NAME = "Files/POLICY"
QTABLE_FILE_NAME = "Files/QTABLE"
PLANS_FILE_NAME = "Files/PLANS"
EXPLORECONST_FILE_NAME = "Files/ExploreConst"
NUMBER_OF_ARGUMENTS_REQUIRED = 4
NUMBER_OF_ARGUMENTS_GIVEN = 0
TOO_LITTLE_ARGUMENTS = True
TOO_MUCH_ARGUMENTS = False
ARGUMENTS_OK = False
FIRST_ARGUMENT_OK = False
SECOND_ARGUMENT_OK = False
THIRD_ARGUMENT_OK = False
FOURTH_ARGUMENT_OK = False
REQUESTED_TO_LEARN = False
REQUESTED_TO_EXECUTE = False

POLICY_FILE_EXISTS = False
QTABLE_FILE_EXISTS = False
PLANS_FILE_EXISTS = False
EXPLORECONST_FILE_EXISTS = False

DETERMINISTIC = True
DOMAIN_NAME = ""
PROBLEM_NAME = ""

RANDOM_EXE = None
PLAN_EXE = None
DUMMY_EXE = None

HAS_LEARNED = False

SHOULD_REMEMBER_GOALS = False
BEST_REMEMBERED_GOALS = []  # [(state,how many times reached)]

GOAL = None

COUNTED_STEPS = 0

VISITED_STATE_AND_ACTION_TAKEN = []

NUMBER_OF_DISCOVERIES = 0

FIND_GOAL_TIMEOUT = 1

ACTIONS_TAKEN = []

MEMORY = ()

BEEN_HERE_BEFORE = []
STOP = 0

alpha = 0.5
gama = 0.99
living_age = 120


def ArgumentsOK():
    return (FIRST_ARGUMENT_OK and SECOND_ARGUMENT_OK and THIRD_ARGUMENT_OK and FOURTH_ARGUMENT_OK
            and not TOO_LITTLE_ARGUMENTS and not TOO_MUCH_ARGUMENTS)


def FilesOK():
    return POLICY_FILE_EXISTS and QTABLE_FILE_EXISTS


def BeenHereAndDoneThat(state, action):
    entry = (state, action)
    if entry in VISITED_STATE_AND_ACTION_TAKEN:
        return True
    return False


def RememberStateAndAction(state, action):
    VISITED_STATE_AND_ACTION_TAKEN.append((state, action))


def ClearMemoryOfStatesAndActions():
    global VISITED_STATE_AND_ACTION_TAKEN
    VISITED_STATE_AND_ACTION_TAKEN = []


def MemorySave(item):
    global MEMORY
    MEMORY = item


def MemoryLoad():
    return MEMORY


def bellmanCalc(state, actions, reward):
    key = MEMORY
    prev_state_quality = 0
    if key is not None:
        prev_state_quality = Learner.get_action_quality(key)
    current_state_qualities = Learner.get_Qualities(state, actions)
    max_val = getMax(current_state_qualities)
    new_state_quality = prev_state_quality
    try:
        new_state_quality += alpha * (reward + gama * max_val - prev_state_quality)
    except:
        print "exception!"
    return new_state_quality


def getMax(my_list):
    max_var = None
    size = len(my_list)
    if size == 0:
        return 0
    if size == 1:
        max_var = my_list[0]
        return max_var
    elif size != 0:
        max_var = my_list[0]
        for i in range(1, size):
            if my_list[i] > max_var:
                max_var = my_list[i]
    return max_var
