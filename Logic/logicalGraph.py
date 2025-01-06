# logicalGraph.py

import networkx as nx
from logicalExpressions import (
    Expression, Var, Not, And, Or, Implies
)


def build_logic_graph(expr: Expression, final_var: str, graph=None, op_label=""):

    if graph is None:
        graph = nx.DiGraph()

    # Make sure the final_var is in the graph as a node
    graph.add_node(final_var)

    # Case 1: if expr is just a Var, link it directly to final_var
    if isinstance(expr, Var):
        var_name = expr.name
        graph.add_node(var_name)
        # Clean up the operator label (remove leading/trailing spaces)
        edge_label = op_label.strip() or None
        graph.add_edge(var_name, final_var, operator=edge_label)
        return graph

    # Case 2: Operator-based expressions
    # We'll combine the local operator with whatever we had so far
    # so that we get something like "AND NOT" for nested logic.
    if isinstance(expr, Not):
        new_label = (op_label + " NOT").strip()
        build_logic_graph(expr.child, final_var, graph, new_label)

    elif isinstance(expr, And):
        new_label = (op_label + " AND").strip()
        build_logic_graph(expr.left, final_var, graph, new_label)
        build_logic_graph(expr.right, final_var, graph, new_label)

    elif isinstance(expr, Or):
        new_label = (op_label + " OR").strip()
        build_logic_graph(expr.left, final_var, graph, new_label)
        build_logic_graph(expr.right, final_var, graph, new_label)

    elif isinstance(expr, Implies):
        new_label = (op_label + " IMPLIES").strip()
        build_logic_graph(expr.left, final_var, graph, new_label)
        build_logic_graph(expr.right, final_var, graph, new_label)

    return graph
