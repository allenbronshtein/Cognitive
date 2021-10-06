# Allen Bronshtein 206228751
import random
import Data


class RandomExecutorBasic(object):

    def __init__(self):
        self.successor = None

    def initialize(self, services):
        self.services = services

    def next_action(self):
        if Data.STOP:
            return None
        if self.services.goal_tracking.reached_all_goals():
            Data.BEST_REMEMBERED_GOALS = []
            Data.GOAL = self.services.perception.get_state()
            return None
        options = self.services.valid_actions.get()
        if len(options) == 0:
            return None
        if len(options) == 1:
            return options[0]
        else:
            return self.pick_from_many(options)

    def pick_from_many(self, options):
        chosen = random.choice(options)
        return chosen
