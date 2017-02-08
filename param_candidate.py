from sas import SAS
from collections import defaultdict
import argparse

def check_devisible(var,ops):
    dominant = []
    presumed = []
    for op in ops:
        eff_var = {var for var,to in op.achievement.items()}
        pre_var = {var for var,to in op.requirement.items()}

        if eff_var <= var:
            presumed.append(op)
        elif var <= pre_var:
            dominant.append(op)
        else:
            return False,dominant,[]
    return True,dominant,presumed

def axiom_candidates_var(sas):
    for var in sas.primary_var.keys():
        flag,dominant,presumed = check_devisible({var},sas.operators)
        if flag:
            break
    return presumed

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output',default='output.sas')
    args = parser.parse_args()

    sas = SAS()
    sas.read_file(args.sas_file)


