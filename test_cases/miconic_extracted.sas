begin_version
3
end_version
begin_metric
0
end_metric
7
begin_variable
var0
-1
2
Atom boarded(p0)
NegatedAtom boarded(p0)
end_variable
begin_variable
var1
-1
2
Atom lift-at(f0)
Atom lift-at(f1)
end_variable
begin_variable
var2
-1
2
Atom served(p0)
NegatedAtom served(p0)
end_variable
begin_variable
var3
0
2
NegatedAtom((0, 0), (1, 0))
Atom((0, 0), (1, 0))
end_variable
begin_variable
var4
0
2
NegatedAtom((0, 0), (1, 1))
Atom((0, 0), (1, 1))
end_variable
begin_variable
var5
0
2
NegatedAtom((0, 1), (1, 0))
Atom((0, 1), (1, 0))
end_variable
begin_variable
var6
0
2
NegatedAtom((0, 1), (1, 1))
Atom((0, 1), (1, 1))
end_variable
1
begin_mutex_group
2
1 0
1 1
end_mutex_group
begin_state
1
0
1
0
0
0
0
end_state
begin_goal
1
2 0
end_goal
1
begin_operator
depart f0 p0
1
3 1
3
0 0 -1 1
0 1 -1 0
0 2 -1 0
1
end_operator
9
begin_rule
2
0 0
1 0
3 0 1
end_rule
begin_rule
2
0 0
1 1
4 0 1
end_rule
begin_rule
2
0 1
1 0
5 0 1
end_rule
begin_rule
2
0 1
1 1
6 0 1
end_rule
begin_rule
1
3 1
4 0 1
end_rule
begin_rule
1
4 1
3 0 1
end_rule
begin_rule
1
5 1
6 0 1
end_rule
begin_rule
1
6 1
4 0 1
end_rule
begin_rule
1
6 1
5 0 1
end_rule
3
begin_removed_operator
board f1 p0
1
1 1
1
0 0 -1 0
1
end_removed_operator
begin_removed_operator
down f1 f0
0
1
0 1 1 0
1
end_removed_operator
begin_removed_operator
up f0 f1
0
1
0 1 0 1
1
end_removed_operator
1
begin_remained_operator
depart f0 p0
1
1 0
2
0 0 0 1
0 2 -1 0
1
end_remained_operator
begin_removed_goal
1
2 0
end_removed_goal

