import argparse
import itertools
from sas3_extended import SAS3Extended
from collections import defaultdict

def bottom_up_candidates(sas,k=1):
    candidates = {var for var in sas.primary_var.keys()}
    new_candidates = set()
    new_candidates.add(())
    for j in range(1,k+1):
        for item in itertools.combinations(candidates,j):
            if check_devisible({var for var in item},sas.operators):
                new_candidates.add(item)
    return from_var(sas,set(max(new_candidates,key=len)))

def check_devisible(item,ops):
    for op in ops:
        eff_var = {var for var,to in op.achievement.items()}
        pre_var = {var for var,to in op.requirement.items()}
        if eff_var <= item:
            continue
        if pre_var >= item:
            continue
        return False
    return True

def from_var(sas,candidate_vars):
    res = []
    for op in sas.operators:
        eff_var = {var for var,to in op.achievement.items()}
        pre_var = {var for var,to in op.requirement.items()}
        if eff_var <= candidate_vars:
            res.append(op)
    return res

def top_down_candidates(sas):
    candidate_vars = set()
    for op in sas.operators:
        pre_var = frozenset({var for var,to in op.requirement.items()})
        if len(pre_var) > 0:
            candidate_vars.add(pre_var)

    for op in sas.operators:
        new_vars = set()
        eff_var = frozenset({var for var,to in op.achievement.items()})
        pre_var = frozenset({var for var,to in op.requirement.items()})
        for item in candidate_vars:
            print(item)
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
        return from_var(sas,max(candidate_vars,key=len))
    else:
        return set()

#
# def get_relevant_vars(ops):
#     res = set()
#     for op in ops:
#         pre_var = {var for var,to in op.requirement.items()}
#         res.update((pre_var))
#     return sorted(res)
#
# def pre2key(precondition,relevant_vars):
#     res = []
#     for var in relevant_vars:
#         if var in precondition:
#             res.append(precondition[var])
#         else:
#             res.append(-1)
#     return res
#
# def get_candidates_var_trie(sas):
#     relevant_vars = get_relevant_vars(sas.operators)
#     t = Trie()
#     for op in sas.operators:
#         s = pre2key(op.requirement,relevant_vars)
#         t.add(s)
#     for op in sas.operators:
#
#         pre_s = pre2key(op.requirement,relevant_vars)
#         eff_s = pre2key(op.achievement,relevant_vars)
#         eff_var = ({var for var,to in op.achievement.items()})
#         pre_var = ({var for var,to in op.requirement.items()})
#
#         if not (pre_s in t or eff_s in t):
#             if not pre_var < eff_var:
#                 t.trim(pre_s)
#             if not eff_var < pre_var:
#                 t.trim(eff_s)



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output',default='output.sas')
    args = parser.parse_args()

    sas = SAS()
    sas.read_file(args.sas_file)
    candidate_vars = get_candidates_var(sas)
    print(candidate_vars)


