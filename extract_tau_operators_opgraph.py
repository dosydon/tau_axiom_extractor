from operator_digraph_lemon import OperatorDiGraph


def extract_tau_operators_opgraph(sas):
    G = OperatorDiGraph(sas)
    return G.axiom_candidates()
