# demo_pyvis.py

import networkx as nx
from pyvis.network import Network

# Import your existing logic code
from logicalExpressions import Var, And, Implies
from logicalGraph import build_logic_graph


def main():
    # ------------------------------------------------------------------
    # 1. Build some logic expressions (Minecraft-like)
    # ------------------------------------------------------------------
    hasWood = Var("hasWood")
    canMakePlanks = Var("canMakePlanks")
    hasSticks = Var("hasSticks")
    canCraftTable = Var("canCraftTable")
    canCraftPickaxe = Var("canCraftPickaxe")

    # If you have wood => you can make planks
    exprA = Implies(hasWood, canMakePlanks)
    # If you can make planks => you can craft table
    exprB = Implies(canMakePlanks, canCraftTable)
    # If (planks AND sticks) => you can craft pickaxe
    exprC = Implies(And(canMakePlanks, hasSticks), canCraftPickaxe)

    # ------------------------------------------------------------------
    # 2. Build a single NetworkX graph from the expressions
    # ------------------------------------------------------------------
    G = None
    G = build_logic_graph(exprA, "canMakePlanks", G)  # merges into G
    G = build_logic_graph(exprB, "canCraftTable", G)
    G = build_logic_graph(exprC, "canCraftPickaxe", G)

    # ------------------------------------------------------------------
    # 3. Convert the NetworkX graph to a PyVis Network
    # ------------------------------------------------------------------
    net = Network(height="750px", width="100%", directed=True)

    # Optional: Improve layout physics for large graphs
    net.force_atlas_2based(gravity=-50)

    # Add all the nodes from the NetworkX graph
    for node in G.nodes():
        # Here, 'label' is what you see on-screen
        net.add_node(str(node), label=str(node), title=str(node))

    # Add all the edges from the NetworkX graph
    for u, v, data in G.edges(data=True):
        operator_label = data.get("operator", "")
        # We'll color edges differently based on the operator, if you want:
        edge_color = "blue"  # default
        if operator_label and "AND" in operator_label:
            edge_color = "green"
        elif operator_label and "IMPLIES" in operator_label:
            edge_color = "red"
        elif operator_label and "OR" in operator_label:
            edge_color = "purple"
        elif operator_label and "NOT" in operator_label:
            edge_color = "orange"

        # Add edge to PyVis
        net.add_edge(
            str(u),
            str(v),
            label=operator_label,  # shows up on hover or middle-of-edge
            color=edge_color,  # you can style edges by operator
            arrows="to"  # show arrowheads from child -> parent
        )

    # ------------------------------------------------------------------
    # 4. Generate the interactive HTML file
    # ------------------------------------------------------------------
    net.write_html("minecraft_logic.html")
    print("Open 'minecraft_logic.html' in your browser to see the graph!")


if __name__ == "__main__":
    main()
