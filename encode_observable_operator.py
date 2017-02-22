from sas import Operator
def encode_observable_operator(original_op, primary2secondary, prop2under, original_secondary_var, eff_var):

    primary_req = {(var,value) for var,value in original_op.requirement.items() if not var in original_secondary_var}
    secondary_req = {(var,value) for var,value in original_op.requirement.items() if var in original_secondary_var}
    inner_req = {(var,value) for (var,value) in primary_req if var in eff_var}
    inner_ach = {(var,value) for (var,value) in original_op.achievement.items() if var in eff_var}
    prop = tuple(sorted(inner_req))

    outer_req = {var:value for (var,value) in primary_req if not var in eff_var}
    outer_req[primary2secondary[prop]] = 1
    outer_req.update({prop2under[prop][var]:value for (var,value) in secondary_req})

    achievement = original_op.achievement.copy()
    for var,value in inner_req:
        achievement[var] = value
    for var,value in inner_ach:
        achievement[var] = value

    return Operator.from_requirement(original_op.name, original_op.cost, outer_req, achievement)
