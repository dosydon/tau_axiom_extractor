from sas import Operator
def encode_operator(original_op, primary2secondary, original_secondary_var, eff_var):
    '''
    >>> op = Operator('op',0)
    >>> primary2secondary = {((0,1),):2}
    >>> original_secondary_var = set()
    >>> eff_var = {0}
    >>> op.from_requirement({0:1,1:0},{0:0})
    begin_operator
    op
    1
    1 0
    1
    0 0 1 0
    0
    end_operator
    <BLANKLINE>
    >>> encode_operator(op, primary2secondary, original_secondary_var, eff_var)
    begin_operator
    op
    2
    1 0
    2 1
    1
    0 0 -1 0
    0
    end_operator
    <BLANKLINE>
    '''

    op = OperatorExtended(original_op.name, original_op.cost)

    primary_req = {(var,value) for var,value in original_op.requirement.items() if not var in original_secondary_var}
    secondary_req = {(var,value) for var,value in original_op.requirement.items() if var in original_secondary_var}
    inner_req = {(var,value) for (var,value) in primary_req if var in eff_var}
    inner_ach = {(var,value) for (var,value) in original_op.achievement.items() if var in eff_var}
    prop = tuple(sorted(inner_req))

    outer_req = {var:value for (var,value) in primary_req if not var in eff_var}
    outer_req[primary2secondary[prop]] = 1
    outer_req.update({var:value for (var,value) in secondary_req})

    achievement = original_op.achievement.copy()
    for var,value in inner_req:
        achievement[var] = value
    for var,value in inner_ach:
        achievement[var] = value

    op.from_requirement(outer_req,achievement)
    return op

class OperatorExtended(Operator):
    def __init__(self,name,cost):
        Operator.__init__(self,name,cost)

    def substitute(self,sas,original_secondary_var,eff_var):
        primary_req = {(var,value) for var,value in self.requirement.items() if not var in original_secondary_var}
        secondary_req = {(var,value) for var,value in self.requirement.items() if var in original_secondary_var}
        inner_req = {(var,value) for (var,value) in primary_req if var in eff_var}
        inner_ach = {(var,value) for (var,value) in self.achievement.items() if var in eff_var}
        prop = tuple(sorted(inner_req))
        print(prop)

        outer_req = {var:value for (var,value) in primary_req if not var in eff_var}
        outer_req[sas.primary2secondary[prop]] = 1
        outer_req.update({sas.prop2under[prop][var]:value for (var,value) in secondary_req})

        for var,value in inner_req:
            self.achievement[var] = value
        for var,value in inner_ach:
            self.achievement[var] = value
        self.from_requirement(outer_req,self.achievement)
