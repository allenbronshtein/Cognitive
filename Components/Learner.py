# Allen Bronshtein 206228751
import base64
import random
from pddlsim.local_simulator import LocalSimulator

import Data
import FileManager
import hashlib


def make_hash_sha256(o):
    hasher = hashlib.sha256()
    hasher.update(repr(make_hashable(o)).encode())
    return base64.b64encode(hasher.digest()).decode()


def make_hashable(o):
    if isinstance(o, (tuple, list)):
        return tuple((make_hashable(e) for e in o))

    if isinstance(o, dict):
        return tuple(sorted((k, make_hashable(v)) for k, v in o.items()))

    if isinstance(o, (set, frozenset)):
        return tuple(sorted(make_hashable(e) for e in o))

    return o


stop_learning = False
Qtable = {}
FirstAction = True
explore_const = 1
steps = 1
KnownStates = {}
overall_reached_goals = 0
prev_state = None


def inQtable((state, action)):
    key = (make_hash_sha256(state), action)
    return key in Qtable.keys()


def set_action_quality((state, action), value):
    key = (make_hash_sha256(state), action)
    if key in Qtable.keys():
        del Qtable[key]
    Qtable[key] = value


def get_action_quality((state, action)):
    key = (make_hash_sha256(state), action)
    quality = 0
    if key in Qtable.keys():
        quality = Qtable[key]
        if quality is None:
            quality = 0
    else:
        Qtable[key] = 0
    if quality is None:
        print "Bad"
    return quality


class LearnExecuter(object):
    def __init__(self):
        self.successor = None

    def initialize(self, services):
        global Qtable, explore_const, prev_state, stop_learning
        prev_state = None
        self.services = services
        explore_const = float(
            FileManager.ExploreConstFileManager.getValue(Data.DOMAIN_NAME, Data.PROBLEM_NAME))
        if explore_const < 0:
            stop_learning = True
        if FileManager.QtableFileManager.ExistsInQtable(Data.DOMAIN_NAME.replace(".pddl", ''),
                                                        Data.PROBLEM_NAME.replace(".pddl", '')):
            Qtable = FileManager.QtableFileManager.GetQtable(Data.DOMAIN_NAME.replace(".pddl", ''),
                                                             Data.PROBLEM_NAME.replace(".pddl", ''))

    def next_action(self):
        global FirstAction, steps, prev_state
        if stop_learning:
            exit(128)
        state = self.services.perception.get_state()
        actions = self.services.valid_actions.get()
        if self.services.goal_tracking.reached_all_goals():
            Data.GOAL = state
            state_and_action = Data.MemoryLoad()
            value = Data.bellmanCalc(state, actions, self.GetReward())
            set_action_quality(state_and_action, value)
            Data.MemorySave(None)
            prev_state = None
            return None

        action = self.choose_action(state, actions)
        if not inQtable((state, action)):
            set_action_quality((state, action), 0)
        if FirstAction:
            Data.MemorySave((state, action))
            FirstAction = False
        else:
            state_and_action = Data.MemoryLoad()
            value = Data.bellmanCalc(state, actions, self.GetReward())
            set_action_quality(state_and_action, value)
            Data.MemorySave((state, action))
        steps += 1
        prev_state = state
        return action

    def choose_action(self, state, actions):
        global explore_const
        choose_randomly = False
        if len(actions) == 0:
            return None
        elif len(actions) == 1:
            return actions[0]
        number = random.uniform(0, 1)
        if number <= explore_const:
            choose_randomly = True
        if choose_randomly:
            # Explore
            return random.choice(actions)
        else:
            # Exploit
            action = None
            action_quality = float('-inf')
            for option in actions:
                quality = get_action_quality((state, option))
                new_state = self.services.parser.copy_state(state)
                self.services.parser.apply_action_to_state(option, new_state, check_preconditions=False)
                if quality > action_quality and new_state != prev_state:
                    action = option
                    action_quality = quality
            if action is None:
                action = random.choice(actions)
            return action

    def GetReward(self):
        global overall_reached_goals
        # Reached all goals
        if len(self.services.goal_tracking.uncompleted_goals) == 0:
            return 1

        # Reached no goals
        completed_goals = len(self.services.goal_tracking.completed_goals)
        currently_reached_goals = completed_goals - overall_reached_goals
        overall_reached_goals = completed_goals
        number_of_actions = float(len(self.services.valid_actions.get()))
        if currently_reached_goals <= 0:
            if number_of_actions == 0:
                return -1
            return - 1 / number_of_actions

        # Reached some goals
        if currently_reached_goals != 0:
            if number_of_actions != 0:
                return -(1 / float(currently_reached_goals) * float(number_of_actions))
            else:
                return -1


def Run():
    global Qtable, explore_const
    print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, LearnExecuter())
    value = (float(explore_const) - float(1) / float(Data.living_age))
    FileManager.QtableFileManager.AddQtable(Data.DOMAIN_NAME.replace(".pddl", ''),
                                            Data.PROBLEM_NAME.replace(".pddl", ''), Qtable)
    FileManager.ExploreConstFileManager.setValue(Data.DOMAIN_NAME, Data.PROBLEM_NAME, value)
    Qtable = {}


def get_Qualities(state, actions):
    _list = []
    for action in actions:
        key = str((state, action))
        key = key.replace('\'', '').replace('\"', '').replace('\n', '').replace('{', '').replace('}', '')
        if key in Qtable.keys():
            _list.append(Qtable[key])
        else:
            _list.append(0)
    return _list
