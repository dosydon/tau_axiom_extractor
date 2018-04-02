import argparse
import itertools
from sas3_extended import SAS3Extended
from collections import defaultdict


def from_var(sas, candidate):
    res = []
    for op in sas.operators:
        eff_var = {var for var, to in op.achievement.items()}
        pre_var = {var for var, to in op.requirement.items()}
        if eff_var <= candidate:
            res.append(op)
        elif pre_var >= candidate:
            pass
        else:
            return []
    return res


def extract_tau_operators_top(sas):
    candidate_vars = set()
    for op in sas.operators:
        pre_var = frozenset({var for var, to in op.requirement.items()})
        if len(pre_var) > 0:
            candidate_vars.add(pre_var)

    max_candidate = max(candidate_vars, key=lambda x:len(x))
    print("candidate_max:{}".format(len(max_candidate)))

    for op in sas.operators:
        new_vars = set()
        eff_var = frozenset({var for var, to in op.achievement.items()})
        pre_var = frozenset({var for var, to in op.requirement.items()})
        for item in candidate_vars:
            if pre_var >= item:
                new_vars.add(item)
            elif eff_var <= item:
                new_vars.add(item)
            else:
                pre_intersection = pre_var & item
                eff_intersection = eff_var & item
                if len(pre_intersection) > 0 and not pre_intersection < eff_intersection:
                    new_vars.add(pre_intersection)
                if len(eff_intersection) > 0 and not eff_intersection < pre_intersection:
                    new_vars.add(eff_intersection)

        candidate_vars = new_vars

        if len(candidate_vars) <= 0:
            return candidate_vars

    if len(candidate_vars) > 0:
        print("candidate_vars:{}".format(len(candidate_vars)))
        candidate = max(candidate_vars, key=len)
        res = from_var(sas, candidate)
        return res
    else:
        return []


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output', default='output.sas')
    args = parser.parse_args()

    sas = SAS()
    sas.read_file(args.sas_file)
    candidate_vars = get_candidates_var(sas)
    print(candidate_vars)
