def plan_from_file(sas, file_name):
    res = []
    name2op = {}
    for op in sas.remained_operators:
        name2op[op.name] = op
    for op in sas.removed_operators:
        name2op[op.name] = op
    for line in open(file_name).readlines():
        if line.startswith(";") or line.startswith("-"):
            continue
        line = line.strip('\n')
        line = line.strip('(')
        line = line.strip(')')
        op = name2op[line]
        res.append(op)
    return res
