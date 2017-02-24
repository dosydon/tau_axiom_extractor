#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import copy
import itertools
import os
from sas3_extended import SAS3Extended
from sas import State
from solver import FD
from utils import plan_from_file
from axiom_evaluator import evaluate_axioms


def decode(sas, partial_plan):
    complete_plan = []
    state = State(copy.deepcopy(sas.initial_assignment))
    evaluate_axioms(sas, state, sas.removed_axioms)
    count = 0
    statistics = {"peak_memory": [], "search_time": []}
    for op in partial_plan:
        if op.is_applicable(state):
            state.apply(op)
            evaluate_axioms(sas, state, sas.removed_axioms)
        else:
            print("Not Applicable:{}".format(op.name))
            init = state.assignment.copy()
            for var in sas.secondary_var.keys():
                init[var] = sas.initial_assignment[var]
            goal = op.requirement
            subsas = sas.sub(init, goal)
            fd = FD()
            plan, propeties = fd.solve(subsas, sas)
            if not plan:
                raise Exception
            for k, v in propeties.items():
                statistics[k].append(v)
            complete_plan += plan
            for item in plan:
                state.apply(item)
            state.apply(op)
            evaluate_axioms(sas, state, sas.removed_axioms)
            count += 1
        complete_plan += [op]
    if not state.is_goal(sas.removed_goal):
        init = state.assignment.copy()
        goal = sas.removed_goal
        subsas = sas.sub(init, goal)
        fd = FD()
        plan, propeties = fd.solve(subsas, sas)
        if not plan:
            raise Exception
        for k, v in propeties.items():
            statistics[k].append(v)
        complete_plan += plan
        for item in plan:
            state.apply(item)
    return complete_plan, statistics


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument("sas_plan")
    args = parser.parse_args()

    sas = SAS3Extended.from_file(args.sas_file)

    complete_plan, statistics = decode(sas, plan_from_file(sas, args.sas_plan))
    with open(args.sas_plan, "w") as f:
        for op in complete_plan:
            print("(" + op.name + ")")
            print("(" + op.name + ")", file=f)
        print(";cost={}".format(len(complete_plan)), file=f)
    print("Decode Peak Memory: {} KB".format(
        max(statistics["peak_memory"] + [0])))
    print("Decode Search Time: {} s".format(
        sum(statistics["search_time"] + [0])))
