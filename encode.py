#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import itertools
import time
import os
import psutil
import copy
from collections import defaultdict
from encode_observable_operator import encode_observable_operator
from preprocess import normalize
from extract_tau_operators_opgraph import extract_tau_operators_opgraph
from extract_tau_operators_top import extract_tau_operators_top
from sas3_extended import SAS3Extended
from sas import Operator, Axiom, State

class ConditionalException(Exception):
    pass

def encode(sas,tau_operators):
    eff_var = {var for op in tau_operators for var,to in op.achievement.items() if sas.is_essential(var)}
    inner_goal = {(var,value) for var,value in sas.goal.items() if var in eff_var}
    outer_goal = {var:value for var,value in sas.goal.items() if not var in eff_var}

    primary_var = copy.deepcopy(sas.primary_var)
    secondary_var = defaultdict(dict)
    prop2under = defaultdict(dict)
    primary2secondary = {}
    initial_assignment = sas.initial_assignment.copy()
    goal = outer_goal
    removed_goal = sas.goal.copy()
    axiom_layer = sas.axiom_layer.copy()
    metric = sas.metric
    mutex_group = sas.mutex_group.copy()
    axioms = set()
    operators = []
    removed_operators = set(tau_operators)
    remained_operators = set()

    pre_existing_secondary_vars = sas.secondary_var.keys()
    max_layer = max([layer for layer in sas.axiom_layer.values()]) + 1
    observable_operators = [op for op in sas.operators if not op in tau_operators]

    introduce_new_goal_var(primary_var,secondary_var, axiom_layer, goal, initial_assignment, inner_goal, max_layer)

    introduce_base_axioms(primary_var, secondary_var, primary2secondary, initial_assignment, axiom_layer, axioms, eff_var,inner_goal,max_layer)
    copy_secondary_vars(secondary_var, initial_assignment, prop2under, axiom_layer, axioms, goal, eff_var,pre_existing_secondary_vars)

    introduce_reachability_axioms(primary_var, axiom_layer, primary2secondary ,eff_var, tau_operators, axioms)

    introduce_encoded_observable_operators(observable_operators, primary2secondary, eff_var, operators, remained_operators)

    return SAS3Extended(primary_var=primary_var, secondary_var = secondary_var, initial_assignment = initial_assignment, axiom_layer = axiom_layer, removed_goal = removed_goal, goal=goal, metric = metric, mutex_group = mutex_group, axioms = axioms, operators = operators, removed_operators = removed_operators, remained_operators = remained_operators)

def copy_secondary_vars(secondary_var, initial_assignment, prop2under, axiom_layer, axioms, goal, eff_var,pre_existing_secondary_vars):
    for index in pre_existing_secondary_vars:
        for prop in itertools.product(*[[(var,value) for value in primary_var[var]] for var in eff_var]):
            values = secondary_var[index]
            new_index = add_secondary({0:values[0] + " under " + str(prop),1:values[1] + " under " + str(prop)},axiom_layer[index])
            prop2under[prop][index] = new_index
            initial_assignment[new_index] = initial_assignment[index]
            if index in goal:
                oraxiom = Axiom()
                new_requirement = {prop2under[prop][index]:(2 - initial_assignment[prop2under[prop][index]]) // 2}
                for var,value in prop:
                    new_requirement[var] = value
                new_requirement[index] = initial_assignment[index]
                oraxiom.from_requirement(new_requirement,{index:(2 -initial_assignment[index])//2})
                axioms.add(oraxiom)

def introduce_encoded_observable_operators(observable_operators, primary2secondary, eff_var, operators, remained_operators):
    for op in observable_operators:
        remained_op = Operator(op.name,op.cost)
        remained_op.from_prevail(op.prevail.copy(),op.effect.copy())
        remained_operators.add(remained_op)
        operators.append(encode_observable_operator(op, primary2secondary, set(), eff_var))

def introduce_reachability_axioms(primary_var,axiom_layer,primary2secondary,eff_var,tau_operators, axioms):
    for prop in itertools.product(*[[(var,value) for value in primary_var[var]] for var in sorted(eff_var)]):
        assignment = {var:value for (var,value) in prop}
        state = State(assignment)
        for op in tau_operators:
            if op.is_applicable(state):
                new_assignment = {var:value for (var,value) in prop}
                res = State(new_assignment)
                res.apply(op)
                new_prop = tuple(((var,value) for (var,value) in res.assignment.items() if axiom_layer[var] == -1))
                if not prop == new_prop:
                    fr = primary2secondary[prop]
                    to = primary2secondary[new_prop]

                    outer_req = {var:value for (var,value) in op.requirement.items() if not var in eff_var}
                    outer_req[fr] = 1
                    axiom = Axiom()
                    axiom.from_prevail(outer_req,{to:(0,1)})
                    axioms.add(axiom)

def introduce_new_goal_var(primary_var, secondary_var, axiom_layer, goal, initial_assignment, inner_goal, max_layer):
    if inner_goal:
        goal_var = len(primary_var)
        values = {0:str(tuple(inner_goal))+"=False",1:str(tuple(inner_goal))+"=True"}

        secondary_var[goal_var] = values
        axiom_layer[goal_var] = max_layer
        goal[goal_var] = 1
        initial_assignment[goal_var] = 0

def introduce_base_axioms(primary_var, secondary_var, primary2secondary, initial_assignment, axiom_layer, axioms, eff_var,inner_goal,max_layer):
    for prop in itertools.product(*[[(var,value) for value in primary_var[var]] for var in sorted(eff_var)]):
        second = len(primary_var) + len(secondary_var)
        secondary_var[second] = {0:"NegatedAtom" + str(prop),1:"Atom" + str(prop)}
        axiom_layer[second] = max_layer
        primary2secondary[prop] = second
        initial_assignment[second] = 0

        axiom = Axiom()
        axiom.from_prevail({x:y for (x,y) in prop},{second:(0,1)})
        axioms.add(axiom)

        if inner_goal and set(inner_goal) <= set(prop):
            goal_axiom = Axiom()
            goal_axiom.from_prevail({second:1},{goal_var:(0,1)})
            axioms.add(goal_axiom)

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
        candidate_gen_table = {
                'opgraph': extract_tau_operators_opgraph, 'top':extract_tau_operators_top
                }
        candidate_gen = candidate_gen_table[args.candidate_gen]
        start = time.time()
        try:
            tau_operators = candidate_gen(sas)
        finally:
            end = time.time()
            print("Candidate Time: {}s".format(end-start))
        print("# of removed operators : {}".format(len(tau_operators)))
        sas = encode(sas,tau_operators)

        normalize(sas)
        with open(args.output,"w") as f:
            print(sas,file=f)
    except Exception as e:
        raise e
    finally:
        end = time.time()
        print("Encode Time: {}s".format(end-start))
        process = psutil.Process(os.getpid())
        print("Encode Peak Memory: {} KB".format(process.memory_info().rss / 1024))
