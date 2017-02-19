#! /usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from state import State
from encode_observable_operator import encode_observable_operator
from preprocess import normalize
from stratification import stratify
from candidate import bottom_up_candidates,top_down_candidates
import argparse
import itertools
import time
import os
import psutil
import copy
from sas3_extended import SAS3Extended
from sas import Operator, Axiom

class ConditionalException(Exception):
    pass

# changes sas in place
def encode(sas,candidates):
    eff_var = {var for op in candidates for var,to in op.achievement.items() if sas.is_essential(var)}
    inner_goal = {(var,value) for var,value in sas.goal.items() if var in eff_var}
    outer_goal = {var:value for var,value in sas.goal.items() if not var in eff_var}

    primary_var = copy.deepcopy(sas.primary_var)
    initial_assignment = copy.copy(sas.initial_assignment)
    removed_goal = copy.copy(sas.goal)
    goal = outer_goal
    mutex_group = copy.copy(sas.mutex_group)
    axiom_layer = sas.axiom_layer.copy()
    metric = sas.metric
    operators = [op for op in sas.operators if not op in candidates]

    encoded = SAS3Extended(primary_var=primary_var, initial_assignment = initial_assignment, axiom_layer = axiom_layer, removed_goal = removed_goal, goal=goal, metric = metric, mutex_group = mutex_group)

    max_layer = max([layer for layer in sas.axiom_layer.values()]) + 1

    introduce_base_axioms(encoded,eff_var,inner_goal,max_layer)

    introduce_reachability_axioms(encoded,eff_var,set(),candidates)

    encoded.removed_operators = set(candidates)
    for op in operators:
        remained_op = Operator(op.name,op.cost)
        remained_op.from_prevail(op.prevail.copy(),op.effect.copy())
        encoded.remained_operators.add(remained_op)
        encoded.operators.append(encode_observable_operator(op, encoded.primary2secondary, set(), eff_var))
    return encoded

def introduce_reachability_axioms(sas,eff_var,pre_existing_secondary_vars,candidates):
    for prop in itertools.product(*[[(var,value) for value in sas.primary_var[var]] for var in sorted(eff_var)]):
        assignment = {var:value for (var,value) in prop}
        state = State(assignment)
        for op in candidates:
            if op.is_applicable(state):
                new_assignment = {var:value for (var,value) in prop}
                res = State(new_assignment)
                res.apply(op)
                new_prop = tuple(((var,value) for (var,value) in res.assignment.items() if sas.is_essential(var)))
                if not prop == new_prop:
                    fr = sas.primary2secondary[prop]
                    to = sas.primary2secondary[new_prop]

                    outer_req = {var:value for (var,value) in op.requirement.items() if not var in eff_var}
                    outer_req[fr] = 1
                    axiom = Axiom()
                    axiom.from_prevail(outer_req,{to:(0,1)})
                    sas.axioms.add(axiom)

def introduce_base_axioms(sas,eff_var,inner_goal,max_layer):
    if inner_goal:
        values = {0:str(tuple(inner_goal))+"=False",1:str(tuple(inner_goal))+"=True"}
        goal_var = sas.add_secondary(values,max_layer)
        sas.goal[goal_var] = 1
        sas.initial_assignment[goal_var] = 0

    for prop in itertools.product(*[[(var,value) for value in sas.primary_var[var]] for var in sorted(eff_var)]):
        second = sas.add_secondary({0:"NegatedAtom" + str(prop),1:"Atom" + str(prop)},max_layer)
        sas.primary2secondary[prop] = second
        sas.initial_assignment[second] = 0

        axiom = Axiom()
        axiom.from_prevail({x:y for (x,y) in prop},{second:(0,1)})
        sas.axioms.add(axiom)


        if inner_goal and set(inner_goal) <= set(prop):
            goal_axiom = Axiom()
            goal_axiom.from_prevail({second:1},{goal_var:(0,1)})
            sas.axioms.add(goal_axiom)

# def copy_secondary_vars(sas,eff_var,pre_existing_secondary_vars):
#     for index in pre_existing_secondary_vars:
#         for prop in itertools.product(*[[(var,value) for value in sas.primary_var[var]] for var in eff_var]):
#             values = sas.secondary_var[index]
#             new_index = sas.add_secondary({0:values[0] + " under " + str(prop),1:values[1] + " under " + str(prop)},sas.axiom_layer[index])
#             sas.prop2under[prop][index] = new_index
#             sas.initial_assignment[new_index] = sas.initial_assignment[index]
#             if index in sas.goal:
#                 oraxiom = Axiom()
#                 new_requirement = {sas.prop2under[prop][index]:(2 - sas.initial_assignment[sas.prop2under[prop][index]]) // 2}
#                 for var,value in prop:
#                     new_requirement[var] = value
#                 new_requirement[index] = sas.initial_assignment[index]
#                 oraxiom.from_requirement(new_requirement,{index:(2 -sas.initial_assignment[index])//2})
#                 sas.axioms.add(oraxiom)

# def copy_axioms(sas,eff_var,pre_existing_secondary_vars):
#     for axiom in sas.removed_axioms:
#         for prop in itertools.product(*[[(var,value) for value in sas.primary_var[var]] for var in eff_var]):
#             new_axiom = (axiom.get_under_prop(sas,prop,pre_existing_secondary_vars,eff_var))
#             if new_axiom:
#                 sas.axioms.add(new_axiom)
#                 for eff_var,eff_val in axiom.achievement.items():
#                     oraxiom = Axiom()
#                     new_requirement = {sas.prop
#                     oraxiom.from_requirement(new_requirement,{eff_var:eff_val})
#                     print(eff_var)
#                     print(sas.prop2under[prop][eff_var])


def main(sas,args):
    candidate_gen_table = {
            'bottom':bottom_up_candidates,'top':top_down_candidates}
    candidate_gen = candidate_gen_table[args.candidate_gen]
    start = time.time()
    try:
        candidates = candidate_gen(sas)
    finally:
        end = time.time()
        print("Candidate Time: {}s".format(end-start))
    print("# of removed operators : {}".format(len(candidates)))
#     if len(candidates) > 0:
    return(encode(sas,candidates))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output',default='output.sas')
    parser.add_argument("--candidate_gen",default='opgraph')
    args = parser.parse_args()


    start = time.time()
    try:
        sas = SAS3Extended.from_file(args.sas_file)
    except ConditionalException as e:
        print("conditional input")
        raise e
    except Exception as e:
        print("invalid input")
        raise e


    try:
        sas = main(sas,args)
        normalize(sas)
        with open(args.output,"w") as f:
            print(sas,file=f)
#             sas.write(f)
    except Exception as e:
        raise e
    finally:
        end = time.time()
        print("Encode Time: {}s".format(end-start))
        process = psutil.Process(os.getpid())
        print("Encode Peak Memory: {} KB".format(process.memory_info().rss / 1024))
