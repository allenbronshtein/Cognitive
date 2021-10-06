# Allen Bronshtein 206228751
from pddlsim.executors.executor import Executor
import pddlsim.planner as planner

from Components import FileManager
import Data


class PlanDispatcher(Executor):
    def __init__(self):
        super(PlanDispatcher, self).__init__()
        self.steps = []

    def initialize(self, services):
        if FileManager.PlansFileManager.ExistsInPlans(Data.DOMAIN_NAME, Data.PROBLEM_NAME):
            self.steps = FileManager.PlansFileManager.GetPlan(Data.DOMAIN_NAME, Data.PROBLEM_NAME)
        else:
            self.steps = planner.make_plan(services.pddl.domain_path, services.pddl.problem_path)

    def next_action(self):
        if len(self.steps) > 0:
            action = self.steps.pop(0).lower().strip()
            Data.ACTIONS_TAKEN.append(action)
            return action
        return None
