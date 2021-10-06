# Allen Bronshtein 206228751
import Data


class Dummy(object):

    def __init__(self):
        self.successor = None

    def initialize(self, services):
        self.services = services
        actions = self.services.parser.actions
        for action in actions:
            type_str = str(type(actions.get(action)))
            if type_str != "<class 'pddlsim.parser_independent.Action'>":
                Data.DETERMINISTIC = False
                break

    def next_action(self):
        return None
