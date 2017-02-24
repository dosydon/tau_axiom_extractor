from sas_extended import SASExtended
from sas import SAS3
import copy


class SAS3Extended(SASExtended, SAS3):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def __repr__(self):
        res = ''
        res += self.version2str()
        res += self.metric2str()
        res += self.variables2str()
        res += self.mutex_group2str()
        res += self.state2str()
        res += self.goal2str()
        res += self.operators2str()
        res += self.rules2str()
        res += self.removed_rule2str()
        res += self.removed_operator2str()
        res += self.remained_operator2str()
        res += self.removed_goal2str()
        return res

    def sub(self, init, goal):
        params = {}
        params["primary_var"] = copy.deepcopy(self.primary_var)
        params["secondary_var"] = copy.deepcopy(self.secondary_var)
        params["goal"] = copy.deepcopy(goal)
        params["mutex_group"] = copy.deepcopy(self.mutex_group)
        params["operators"] = copy.deepcopy(self.removed_operators)
        params["initial_assignment"] = copy.deepcopy(init)
        params["axioms"] = copy.deepcopy(self.removed_axioms)
        params["axiom_layer"] = copy.deepcopy(self.axiom_layer)

        return SAS3Extended(**params)
