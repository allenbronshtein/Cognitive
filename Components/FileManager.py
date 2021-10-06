# Allen Bronshtein 206228751

from os import path
import Data
import pickle


def FormatPlans(plan_str):
    plan_str = plan_str[:-1].replace('[', '').replace(']', '').replace('\'', '')
    plan_list = plan_str.split(",")
    return plan_list


def CheckFiles():
    if path.exists(Data.POLICY_FILE_NAME):
        Data.POLICY_FILE_EXISTS = True
    if path.exists(Data.QTABLE_FILE_NAME):
        Data.QTABLE_FILE_EXISTS = True
    if path.exists(Data.PLANS_FILE_NAME):
        Data.PLANS_FILE_EXISTS = True
    if path.exists(Data.EXPLORECONST_FILE_NAME):
        Data.EXPLORECONST_FILE_EXISTS = True


class QtableFileManager(object):
    @staticmethod
    def ExistsInQtable(domain, problem):
        key = str(domain) + "," + str(problem)
        path_name = "Qtables/" + str(key) + ".pickle"
        return path.exists(path_name)

    @staticmethod
    def GetQtable(domain, problem):
        key = str(domain) + "," + str(problem)
        path_name = "Qtables/" + str(key) + ".pickle"
        with open(path_name, 'rb') as handle:
            unserialized_data = pickle.load(handle)
            return unserialized_data

    @staticmethod
    def AddQtable(domain, problem, qtable):
        path_name = "Qtables/" + str(domain) + "," + str(problem) + ".pickle"
        with open(path_name, 'wb') as handle:
            pickle.dump(qtable, handle, protocol=pickle.HIGHEST_PROTOCOL)


class PlansFileManager(object):
    @staticmethod
    def ExistsInPlans(domain, problem):
        key = str(domain) + "," + str(problem)
        with open(Data.PLANS_FILE_NAME, 'r') as read_obj:
            for line in read_obj:
                if key in line:
                    return True
        return False

    @staticmethod
    def GetPlan(domain, problem):
        entry = []
        key = str(domain) + "," + str(problem)
        with open(Data.PLANS_FILE_NAME, 'r') as read_obj:
            for line in read_obj:
                if key in line:
                    entry = FormatPlans(line.split("$")[1])
                    break
        read_obj.close()
        return entry

    @staticmethod
    def AddPlan(domain, problem, plan):
        key = str(domain) + "," + str(problem)
        with open(Data.PLANS_FILE_NAME, 'r+') as f:
            t = f.read()
            to_delete = key
            f.seek(0)
            for line in t.split('\n'):
                if line.split("$")[0] != to_delete and line != "":
                    f.write(line + '\n')
            f.truncate()
        f.close()
        with open(Data.PLANS_FILE_NAME, 'a') as write_obj:
            entry = str(domain) + "," + str(problem) + "$" + str(plan) + "\n"
            write_obj.write(entry)
        write_obj.close()

    @staticmethod
    def ClearFile():
        open(Data.PLANS_FILE_NAME, 'w').close()

    @staticmethod
    def DeletePlan(domain, problem):
        key = str(domain) + "," + str(problem)
        with open(Data.PLANS_FILE_NAME, 'r+') as f:
            t = f.read()
            to_delete = key
            f.seek(0)
            for line in t.split('\n'):
                if line.split("$")[0] != to_delete and line != "":
                    f.write(line + '\n')
            f.truncate()
        f.close()


class ExploreConstFileManager(object):
    @staticmethod
    def getValue(domain, problem):
        entry = None
        key = str(domain) + "," + str(problem)
        with open(Data.EXPLORECONST_FILE_NAME, 'r') as read_obj:
            for line in read_obj:
                if key in line:
                    entry = line.split("$")[1].replace('\n', '')
                    break
        read_obj.close()
        if entry is None:
            return 1
        return float(entry)

    @staticmethod
    def setValue(domain, problem, value):
        key = str(domain) + "," + str(problem)
        with open(Data.EXPLORECONST_FILE_NAME, 'r+') as f:
            t = f.read()
            to_delete = key
            f.seek(0)
            for line in t.split('\n'):
                if line.split("$")[0] != to_delete and line != "":
                    f.write(line + '\n')
            f.truncate()
        f.close()
        with open(Data.EXPLORECONST_FILE_NAME, 'a') as write_obj:
            entry = str(domain) + "," + str(problem) + "$" + str(value) + "\n"
            write_obj.write(entry)
        write_obj.close()
