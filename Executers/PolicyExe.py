# Allen Bronshtein 206228751
from Components import FileManager
import Data


def actionName(action):
    return action.split(" ")[0][1:]


def actionName_to_pddlAction(action_name, actions):
    for action in actions:
        if action_name == actionName(action):
            return action
    return None


class PolicyExecuter(object):
    def __init__(self):
        self.successor = None

    def initialize(self, services):
        self.services = services

    def next_action(self):
        action = None
        policy = FileManager.PolicyFileManager.GetPolicy(Data.DOMAIN_NAME, Data.PROBLEM_NAME)
        state = self.services.perception.get_state()
        if self.services.goal_tracking.reached_all_goals():
            return None
        actions = self.services.valid_actions.get()
        if str(state) in policy.keys():
            action = policy[str(state)].strip('\'')
            action = actionName_to_pddlAction(action, actions)
        return action
