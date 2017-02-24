from collections import defaultdict
from sas import State
from stratification import stratify
import argparse
import sas
import copy


def evaluate_axioms(sas,state,axioms):
    for var in sas.secondary_var.keys():
        state.assignment[var] = sas.initial_assignment[var]

    axiom_by_layer = defaultdict(set)
    for axiom in axioms:
        lst = list(axiom.achievement.items())
        j,v = lst[0]
        axiom_by_layer[sas.axiom_layer[j]].add(axiom)

    for layer,axioms_in_layer in sorted(axiom_by_layer.items()):
#         print(layer)
        while True:
            prev = copy.copy(state)
            for axiom in axioms_in_layer:
                if axiom.is_applicable(state):
                    state.apply(axiom)
            if state == prev:
                break

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("sas_file")
    args = parser.parse_args()
    sas = sas.SAS()
    sas.read_file(args.sas_file)
    s = State(sas.initial_assignment)
    for k,v in s.assignment.items():
        print((k,v))
    evaluate_axioms(sas,s,sas.axioms)
    for k,v in s.assignment.items():
        if k in sas.secondary_var:
            print(sas.secondary_var[k][v])
