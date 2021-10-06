# Allen Bronshtein 206228751
from sys import argv
from Components import Executer, Learner, FileManager
from Utilities import Actions, ErrorHandler
from pddlsim.local_simulator import LocalSimulator
import Data
from Executers.RandomExe import RandomExecutorBasic
from Executers.RandomExeExtended import RandomExecutor
from Executers.PlanKExe import PlanKExecuter

# "<-----------For Debug----------->"
# argv[0] = "my_executive.py"
# argv.append("-E")
# argv.append("domain.pddl")
# argv.append("problem2.pddl")
# "<-------------Tests------------->"

"<------------------------------->"
""" Main part of our executive"""
if argv[1] == "-T":
    Actions.CheckArguments()
    FileManager.CheckFiles()
    _input = raw_input("1 for Random, 2 for Random+, 3 for k planner")
    if _input == '1':
        print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, RandomExecutorBasic())
    elif _input == '2':
        print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, RandomExecutor())
    elif _input == '3':
        print LocalSimulator().run(Data.DOMAIN_NAME, Data.PROBLEM_NAME, PlanKExecuter())
else:
    Actions.CheckArguments()
    FileManager.CheckFiles()
    if not Data.ArgumentsOK():
        ErrorHandler.BadArgumentsHandler()
    Actions.PrepareExe()
    if Data.REQUESTED_TO_LEARN:
        Learner.Run()
    if Data.REQUESTED_TO_EXECUTE:
        Executer.Run()
    Actions.RemoveGarbageFiles()
