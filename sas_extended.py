import copy
import argparse
import itertools
from collections import defaultdict
from abc import ABC, abstractmethod
from sas import Axiom, Operator


class SASExtended(ABC):

    def __init__(self, **kwargs):
        prop_defaults = {
            "primary_var": defaultdict(dict),
            "secondary_var": defaultdict(dict),
            "prop2under": defaultdict(dict),
            "primary2secondary": {},
            "initial_assignment": {},
            "goal": {},
            "removed_goal": {},
            "axiom_layer": defaultdict(int),
            "metric": True,
            "version": 3,
            "mutex_group": [],
            "axioms": set(),
            "removed_axioms": set(),
            "operators": [],
            "removed_operators": set(),
            "remained_operators": set()
        }
        for (prop, default) in prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

    def parse_removed_goal(self, lines):
        for line in (lines[1:]):
            nums = [int(num) for num in line.split(' ')]
            self.removed_goal[nums[0]] = nums[1]

    def parse_mutex_group(self, lines):
        group = []
        for line in (lines[1:]):
            nums = [int(num) for num in line.split(' ')]
            group.append((nums))
        self.mutex_group.append(group)

    def parse_operator(self, lines):
        prevail = {}
        effect = {}

        name = lines[0]
        num_prevail = int(lines[1])
        num_effect = int(lines[num_prevail + 2])
        for line in lines[2:2 + num_prevail]:
            (var, value) = [int(num) for num in line.split(' ')]
            prevail[var] = value
        for line in lines[num_prevail + 3:num_prevail + num_effect + 3]:
            num_conditions = int(line[0])
            rest = [int(num) for num in line.split(' ')][1:]
            for i in range(0, num_conditions):
                var, val = rest[:2]
                rest = rest[2:]
            (var, fr, to) = rest
            effect[var] = (fr, to)

        cost = int(lines[-1])
        new_operator = Operator.from_prevail(name, cost, prevail, effect)
        self.operators.append(new_operator)

    def parse_removed_rule(self, lines):
        prevail = {}
        effect = {}

        num_prevail = int(lines[0])
        for line in lines[1:1 + num_prevail]:
            (var, value) = [int(num) for num in line.split(' ')]
            prevail[var] = value

        for line in lines[num_prevail + 1:num_prevail + 2]:
            (var, fr, to) = [int(num) for num in line.split(' ')]
            if var in prevail and (not prevail[var] == fr):
                return
            effect[var] = (fr, to)

        axiom = Axiom.from_prevail('axiom', prevail, effect)
        self.removed_axioms.add(axiom)

    def parse_removed_operator(self, lines):
        prevail = {}
        effect = {}

        name = lines[0]
        num_prevail = int(lines[1])
        for line in lines[2:2 + num_prevail]:
            (var, value) = [int(num) for num in line.split(' ')]
            prevail[var] = value

        num_effect = int(lines[num_prevail + 2])
        for line in lines[num_prevail + 3:num_prevail + num_effect + 3]:
            (flag, var, fr, to) = [int(num) for num in line.split(' ')]
            effect[var] = (fr, to)

        cost = int(lines[-1])
        new_operator = Operator.from_prevail(name, cost, prevail, effect)
        self.removed_operators.add(new_operator)

    def parse_remained_operator(self, lines):
        prevail = {}
        effect = {}

        name = lines[0]
        num_prevail = int(lines[1])
        for line in lines[2:2 + num_prevail]:
            (var, value) = [int(num) for num in line.split(' ')]
            prevail[var] = value

        num_effect = int(lines[num_prevail + 2])
        for line in lines[num_prevail + 3:num_prevail + num_effect + 3]:
            (flag, var, fr, to) = [int(num) for num in line.split(' ')]
            effect[var] = (fr, to)

        cost = int(lines[-1])
        new_operator = Operator.from_prevail(name, cost, prevail, effect)
        self.remained_operators.add(new_operator)

    def removed_operator2str(self):
        res = '{}\n'.format(len(self.removed_operators))
        for op in sorted(self.removed_operators):
            res += ("begin_removed_operator\n" + "{}\n".format(op.name) + "{}\n".format(len(op.prevail)))
            for (var, value) in sorted(op.prevail.items(), key=lambda x: x[0]):
                res += "{} {}\n".format(var, value)
            res += "{}\n".format(len(op.effect))
            for (var, (fr, to)) in sorted(op.effect.items(), key=lambda x: x[0]):
                res += "0 {} {} {}\n".format(var, fr, to)
            res += "{}\n".format(op.cost)
            res += "end_removed_operator\n"
        return '' if res == '0\n' else res

    def remained_operator2str(self):
        res = '{}\n'.format(len(self.remained_operators))
        for op in sorted(self.remained_operators):
            res += ("begin_remained_operator\n" + "{}\n".format(op.name) + "{}\n".format(len(op.prevail)))
            for (var, value) in sorted(op.prevail.items(), key=lambda x: x[0]):
                res += "{} {}\n".format(var, value)
            res += "{}\n".format(len(op.effect))
            for (var, (fr, to)) in sorted(op.effect.items(), key=lambda x: x[0]):
                res += "0 {} {} {}\n".format(var, fr, to)
            res += "{}\n".format(op.cost)
            res += "end_remained_operator\n"
        return '' if res == '0\n' else res

    def removed_rule2str(self):
        res = '{}\n'.format(len(self.removed_axioms))
        for rule in sorted(self.removed_axioms):
            res += "begin_removed_rule\n"
            res += "{}\n".format(len(rule.prevail))
            for (var, value) in sorted(rule.prevail.items(), key=lambda x: x[0]):
                res += "{} {}\n".format(var, value)
            for (var, (fr, to)) in sorted(rule.effect.items(), key=lambda x: x[0]):
                res += "{} {} {}\n".format(var, fr, to)
            res += "end_removed_rule\n"
        return '' if res == '0\n' else res

    def removed_goal2str(self):
        res = "begin_removed_goal\n"
        res += "{}\n".format(len(self.removed_goal))
        for index, value in sorted(self.removed_goal.items(), key=(lambda x: x[0])):
            res += "{} {}\n".format(index, value)
        res += "end_removed_goal\n"
        return '' if len(self.removed_goal) <= 0 else res
