import argparse
import sas
class State:
    def __init__(self,assignment):
        self.assignment=assignment
    def __repr__(self):
        return str(sorted(self.assignment.items()))
    def apply(self,operator):
        for var,value in operator.achievement.items():
            self.assignment[var] = value
    def is_goal(self,goal):
        for (var,value) in goal.items():
            if not self.assignment[var] == value:
                return False
        return True
    def __eq__(self,other):
        for k,v in self.assignment.items():
            if not other.assignment[k] == v:
                return False
        return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    args = parser.parse_args()
    sas = sas.SAS()
    sas.read_file(args.sas_file)

    s = State(sas.initial_assignment)
    for operator in sas.operators:
        if operator.is_applicable(s):
            print(operator)
    print(s.is_goal(sas.goal))
