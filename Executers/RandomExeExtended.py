# Allen Bronshtein 206228751
import random
import Data
from Utilities.valid_actions import PythonValidActions


def signal_handler(signum, frame):
    Data.STOP = True


class RandomExecutor(object):

    def __init__(self):
        self.successor = None

    def initialize(self, services):
        self.services = services
        Data.BEEN_HERE_BEFORE = []

    def next_action(self):
        if Data.STOP:
            return None
        Data.COUNTED_STEPS += 1
        # When Reached All goals , Count how many steps have done
        if self.services.goal_tracking.reached_all_goals():
            if Data.SHOULD_REMEMBER_GOALS:
                found = False
                goal = self.services.perception.get_state()
                for saved_goal in Data.BEST_REMEMBERED_GOALS:
                    if goal == saved_goal[0]:
                        found = True
                        if Data.COUNTED_STEPS < saved_goal[1]:
                            steps = Data.COUNTED_STEPS
                            Data.BEST_REMEMBERED_GOALS.remove(saved_goal)
                            Data.BEST_REMEMBERED_GOALS.append((goal, steps))
                        break
                if not found:
                    Data.BEST_REMEMBERED_GOALS.append((goal, Data.COUNTED_STEPS))
                Data.COUNTED_STEPS = 0
                return None

        # Part of acting
        state = self.services.perception.get_state()
        options = self.services.valid_actions.get()
        if len(options) == 0:
            Data.BEEN_HERE_BEFORE.append(state)
            return None
        if len(options) == 1:
            Data.BEEN_HERE_BEFORE.append(state)
            return options[0]
        else:
            chosen_action = None
            max_opertunities = 0
            for action in options:
                if not Data.BeenHereAndDoneThat(state, action):
                    copy_state = self.services.parser.copy_state(state)
                    self.services.parser.apply_action_to_state(action, copy_state, check_preconditions=False)
                    if copy_state != state:
                        if copy_state in Data.BEEN_HERE_BEFORE:
                            continue
                        opertunities = len(
                            PythonValidActions.get(PythonValidActions(self.services.parser, self.services.perception),
                                                   copy_state))
                        if opertunities > max_opertunities:
                            max_opertunities = opertunities
                            chosen_action = action
            if chosen_action is not None:
                Data.NUMBER_OF_DISCOVERIES += 1
                Data.RememberStateAndAction(state, chosen_action)
                Data.BEEN_HERE_BEFORE.append(state)
                return chosen_action
            else:
                Data.BEEN_HERE_BEFORE.append(state)
                return self.pick_from_many(options)

    def pick_from_many(self, options):
        chosen = random.choice(options)
        return chosen
