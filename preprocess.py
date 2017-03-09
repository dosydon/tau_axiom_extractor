#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from sas3_extended import SAS3Extended
from sas import Operator, Axiom
import argparse
import itertools
import sys

def get_flipped(value):
    return (2 - value) // 2

def flip_initial_assignment(vars_to_flip, initial_assignment):
    for var in vars_to_flip:
        initial_assignment[var] = get_flipped(initial_assignment[var])

def flip_goals(vars_to_flip, goal):
    for var in goal:
        if var in vars_to_flip:
            goal[var] = get_flipped(goal[var])

def flip_operators(vars_to_flip, sas):
    original_operators = sas.operators.copy()
    sas.operators = []
    for op in original_operators:
        sas.operators.append(op.get_flipped(vars_to_flip))

def flip_axioms(vars_to_flip, sas):
    original_axioms = sas.axioms.copy()
    sas.axioms = set()
    for axiom in original_axioms:
        req = axiom.requirement
        ach = axiom.achievement
        for var in req:
            if var in vars_to_flip:
                req[var] = get_flipped(req[var])
        for var in ach:
            if var in vars_to_flip:
                ach[var] = get_flipped(ach[var])
                assert(ach[var] == 1)
        sas.axioms.add(Axiom.from_requirement("axiom", req, ach))

def flip_mutex_group(vars_to_flip, sas):
    for mutex in sas.mutex_group:
        for item in mutex:
            var, value = item
            if var in vars_to_flip:
                item[1] = get_flipped(value)

def get_vars_to_flip(secondary_var, initial_assignment):
    return {var for var in secondary_var.keys() if initial_assignment[var] == 1}

def normalize(sas):
    vars_to_flip = get_vars_to_flip(sas.secondary_var, sas.initial_assignment)
    flip_initial_assignment(vars_to_flip, sas.initial_assignment)
    flip_goals(vars_to_flip, sas.goal)
    flip_operators(vars_to_flip, sas)
    flip_axioms(vars_to_flip, sas)
    flip_mutex_group(vars_to_flip, sas)

    for var in vars_to_flip:
        inner = sas.secondary_var[var]
        zero = inner[0]
        first = inner[1]
        inner[0] = first
        inner[1] = zero


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output', default='output.sas')
    args = parser.parse_args()

    sas = SAS3Extended.from_file(args.sas_file)
    normalize(sas)
    with open(args.output, "w") as f:
        print(str(sas), file=f)
