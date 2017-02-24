from preprocess import normalize
from collections import defaultdict
import argparse

def stratify(sas):
    r = order(sas)
    for i in sas.secondary_var.keys():
        if r[i][i] >= 2:
            raise Exception("not stratified")
    stratification = extract(sas,r)
    for level,inner_set in stratification.items():
        for var in inner_set:
            sas.axiom_layer[var] = level

def order(sas):
    r = defaultdict(dict)
    for i in sas.secondary_var.keys():
        for j in sas.secondary_var.keys():
            r[i][j] = 0
    for axiom in sas.axioms:
        lst = axiom.achievement.items()
        j = lst[0][0]
        for i,val in axiom.requirement.items():
            if i == j:
                continue
            if i in sas.secondary_var:
                if val == 0:
                    r[i][j] =2
                else:
                    r[i][j] =max(1,r[i][j])
    for j in sas.secondary_var.keys():
        for i in sas.secondary_var.keys():
            for k in sas.secondary_var.keys():
                if min(r[i][j],r[j][k] > 0):
                    r[i][k] = max(r[i][j],r[j][k],r[i][k])
    print(r)
    return r

def extract(sas,r):
    stratification = defaultdict(set)
    remaining = set(sas.secondary_var.keys())
    level = 0

    while len(remaining) > 0:
        for j in remaining:
            flag = True
            for i in remaining:
                if r[i][j] >= 2:
                    flag = False
            if flag:
                stratification[level].add(j)
        remaining -= stratification[level]
        level+=1
    print(stratification)
    return stratification
