from applicable import Applicable

class Operator(Applicable):
    def __init__(self,name,cost):
        Applicable.__init__(self,name)
        self.cost = cost
        self.is_necessary = True
    def substitute(self,sas,original_secondary_var,eff_var):
        primary_req = {(var,value) for var,value in self.requirement.items() if not var in original_secondary_var}
        secondary_req = {(var,value) for var,value in self.requirement.items() if var in original_secondary_var}
        inner_req = {(var,value) for (var,value) in primary_req if var in eff_var}
        inner_ach = {(var,value) for (var,value) in self.achievement.items() if var in eff_var}
        prop = tuple(sorted(inner_req))

        outer_req = {var:value for (var,value) in primary_req if not var in eff_var}
        outer_req[sas.primary2secondary[prop]] = 1
        outer_req.update({sas.prop2under[prop][var]:value for (var,value) in secondary_req})

        for var,value in inner_req:
            self.achievement[var] = value
        for var,value in inner_ach:
            self.achievement[var] = value
        self.from_requirement(outer_req,self.achievement)




if __name__ == '__main__':
    op = Operator("temp",0)
    op.from_requirement({0:1,1:1},{1:2,2:1})
    print(op.prevail)
    print(op.effect)
    op.substitute({(0,1):3})
    print(op.requirement)
    print(op.prevail)
    print(op.effect)
