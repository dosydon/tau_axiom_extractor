from sas import Axiom

class AxiomExtended(Axiom):
    def __init__(self, name="axiom", cost=0):
        Axiom.__init__(self, name, cost)

    def substitute(self, primary2secondary):
        if self.is_converted:
            for (primary_var, value), secondary_var in primary2secondary.items():
                if primary_var in self.requirement and self.requirement[primary_var] == value:
                    del self.requirement[primary_var]
                    self.requirement[secondary_var] = 1
            self.from_requirement(self.requirement, self.achievement)

    def is_applicable_under_prop(self, prop):
        for var, value in prop:
            if var in self.requirement and self.requirement[var] != value:
                return False
        return True

    def get_under_prop(self, sas, prop, original_second_var, eff_var):
        if not self.is_applicable_under_prop(prop):
            return None

        new_requirement = {}
#         flag = False
        for var, value in self.requirement.items():
            if var in original_second_var:
                new_requirement[sas.prop2under[prop][var]] = value
            elif var in eff_var:
                pass
            else:
                new_requirement[var] = value
#         if flag:
#             new_requirement[sas.primary2secondary[prop]] = 1
        for eff_var, eff_val in self.achievement.items():
            axiom = Axiom()
            if eff_var in original_second_var:
                axiom.from_requirement(new_requirement, {sas.prop2under[prop][eff_var]:eff_val})
            else:
                axiom.from_requirement(new_requirement, {eff_var:eff_val})
            return axiom

    def axiom2op(self):
        assert self.is_converted
        op = Operator(self.name, self.cost)
        op.from_prevail(self.prevail, self.effect)
        return op


if __name__ == '__main__':
    op = Axiom("temp")
    op.from_requirement({0:1, 1:1}, {1:2, 2:1})
    op.substitute({(0, 1):3})
