# 206228751 Allen Bronshtein
import random
from Components import FileManager
import Data
from Utilities.valid_actions import PythonValidActions

max_goals_reached = 0
best_action = None
best_state = None
min_steps = None
k = None
REMEMBER_STATES = []
route = []
run_existing_plan = False


class PlanKExecuter(object):
    def __init__(self):
        self.successor = None

    def initialize(self, services):
        global k, route, run_existing_plan
        self.services = services
        if FileManager.PlansFileManager.ExistsInPlans(Data.DOMAIN_NAME, Data.PROBLEM_NAME):
            _input = raw_input("Found existing plan - use? y/n\n")
            if _input.lower() == 'y':
                route = FileManager.PlansFileManager.GetPlan(Data.DOMAIN_NAME, Data.PROBLEM_NAME)
                run_existing_plan = True
        else:
            k = int(raw_input("Input number of steps to look forward\n"))

    def recursive_check_for_k(self, current_state, prev_action, steps_done):
        global k, best_action, max_goals_reached, best_state, min_steps
        actions = PythonValidActions.get(PythonValidActions(self.services.parser, self.services.perception),
                                         current_state)
        if len(actions) == 0:
            goals_reached = 0
            uncompleted_goals = self.services.goal_tracking.uncompleted_goals
            for goal in uncompleted_goals:
                if self.services.parser.test_condition(goal, current_state):
                    goals_reached = goals_reached + 1
            if goals_reached > max_goals_reached and min_steps is None:
                max_goals_reached = goals_reached
                best_action = prev_action
                best_state = current_state
                min_steps = steps_done
            elif goals_reached >= max_goals_reached and steps_done < min_steps:
                max_goals_reached = goals_reached
                best_action = prev_action
                best_state = current_state
                min_steps = steps_done
            return

        else:
            if steps_done < k:
                goals_reached = 0
                for goal in self.services.goal_tracking.uncompleted_goals:
                    if self.services.parser.test_condition(goal, current_state):
                        goals_reached = goals_reached + 1
                if goals_reached > max_goals_reached:
                    max_goals_reached = goals_reached
                    best_action = prev_action
                    best_state = current_state
                for action in actions:
                    new_state = self.services.parser.copy_state(current_state)
                    self.services.parser.apply_action_to_state(action, new_state, check_preconditions=False)
                    self.recursive_check_for_k(new_state, action, steps_done + 1)
                    if best_action is not None:
                        temp_state = self.services.parser.copy_state(current_state)
                        self.services.parser.apply_action_to_state(best_action, temp_state, check_preconditions=False)
                        if temp_state == best_state and prev_action is not None:
                            best_state = current_state
                            best_action = prev_action

            else:
                goals_reached = 0
                uncompleted_goals = self.services.goal_tracking.uncompleted_goals
                for goal in uncompleted_goals:
                    if self.services.parser.test_condition(goal, current_state):
                        goals_reached = goals_reached + 1
                if goals_reached > max_goals_reached:
                    max_goals_reached = goals_reached
                    best_action = prev_action
                    best_state = current_state
                return

    def next_action(self):
        global max_goals_reached, route
        if run_existing_plan:
            if len(route) > 0:
                action = route.pop(0).lower().strip()
                Data.ACTIONS_TAKEN.append(action)
                return action
        steps_done = 0
        global best_action, best_state, max_goals_reached, min_steps
        best_action = None
        best_state = None
        min_steps = None
        if self.services.goal_tracking.reached_all_goals():
            return None
        current_state = self.services.perception.get_state()
        REMEMBER_STATES.append(current_state)
        actions = self.services.valid_actions.get()
        new_state = self.services.parser.copy_state(current_state)
        self.recursive_check_for_k(new_state, None, steps_done)
        if best_action is None and len(actions) != 0:
            best_action = random.choice(actions)
        REMEMBER_STATES.append((current_state, best_action))
        Data.ACTIONS_TAKEN.append(best_action)
        return best_action
