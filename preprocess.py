#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from collections import defaultdict
from sas3_extended import SAS3Extended
from sas import Operator, Axiom
import argparse
import itertools
import sys
def flip(sas,flip_var):
    assert(sas.initial_assignment[flip_var] <= 1)
    sas.initial_assignment[flip_var] = (2 - sas.initial_assignment[flip_var])//2

    if flip_var in sas.goal:
        sas.goal[flip_var] = (2 - sas.goal[flip_var])//2

    original_operators = sas.operators.copy()
    sas.operators = []
    for op in original_operators:
        pre = op.prevail
        eff = op.effect
        if flip_var in pre:
            pre[flip_var] = (2 - pre[flip_var]) //2 
        if flip_var in eff:
            fr,to = eff[flip_var]
            eff[flip_var]= (to,fr)
        sas.operators.append(Operator.from_prevail(op.name,op.cost,pre,eff))

    original_axioms = sas.axioms.copy()
    sas.axioms = set()
    for axiom in original_axioms:
        req = axiom.requirement
        ach = axiom.achievement
        if flip_var in req:
            req[flip_var] = (2 - req[flip_var]) //2 
        if flip_var in ach:
            ach[flip_var] = (2 - ach[flip_var]) //2 
            assert(ach[flip_var] == 1)
        sas.axioms.add(Axiom.from_requirement("axiom",req,ach))

    for mutex in sas.mutex_group:
        for item in mutex:
            var,value = item
            if var == flip_var:
                item[1] = (2 - value) //2

def normalize(sas):
    for var,inner in sas.secondary_var.items():
        if sas.initial_assignment[var] ==1:
            zero = inner[0]
            first = inner[1]
            inner[0] = first
            inner[1] = zero
            flip(sas,var)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    parser.add_argument('--output',default='output.sas')
    args = parser.parse_args()


    sas = SAS3Extended.from_file(args.sas_file)
    normalize(sas)
    with open(args.output,"w") as f:
        print(str(sas), file=f)
