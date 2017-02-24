from __future__ import print_function
import itertools
import argparse
import sys
import os
import subprocess
import opgraph


class OperatorDiGraph():

    def __init__(self, sas=None):
        self.sas = sas
        self.opV = opgraph.OpV()
        for op in sas.operators:
            effect_var = sorted(
                {var for var, value in op.effect.items() if sas.is_essential(var)})
            requirement_var = sorted(
                {var for var, value in op.requirement.items() if sas.is_essential(var)})
            effV = opgraph.IntV(effect_var)
            reqV = opgraph.IntV(requirement_var)
            item = opgraph.Operator(effV, reqV)
            self.opV.push_back(item)

    def axiom_candidates(self):
        res = []
        for num in opgraph.get_candidates(self.opV):
            res.append(self.sas.operators[num])
        return res
