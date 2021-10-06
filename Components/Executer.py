# Allen Bronshtein 206228751
from Utilities import Actions
import Data
import FileManager
from pddlsim.local_simulator import LocalSimulator
from Learner import LearnExecuter
from Executers.BestPlanExe import PlanDispatcher


def Run():
    if Data.DETERMINISTIC:
        print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, PlanDispatcher())
        actions = Data.ACTIONS_TAKEN
        FileManager.PlansFileManager.AddPlan(Data.DOMAIN_NAME, Data.PROBLEM_NAME, actions)
        Data.ACTIONS_TAKEN = []
        return
    if FileManager.QtableFileManager.ExistsInQtable(Data.DOMAIN_NAME.replace(".pddl", ''),
                                                    Data.PROBLEM_NAME.replace(".pddl", '')):
        trueConstValue = FileManager.ExploreConstFileManager.getValue(Data.DOMAIN_NAME, Data.PROBLEM_NAME)
        FileManager.ExploreConstFileManager.setValue(Data.DOMAIN_NAME, Data.PROBLEM_NAME, 0)
        print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, LearnExecuter())
        FileManager.ExploreConstFileManager.setValue(Data.DOMAIN_NAME, Data.PROBLEM_NAME, trueConstValue)
        return
    Actions.TalkOnly("No policy found , please run learning first .")
