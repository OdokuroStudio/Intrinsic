from Roles.logician import Logician
import os
import json

GRAPH_FILE = "graph_state.json"  # File to persist graph state


def save_graph_to_file(graph):
    """
    Saves the current graph state to a file.
    """
    graph_data = {
        "nodes": [
            {
                "id": node_id,
                "label": node_data["label"],
                "color": node_data["color"],
                "value": graph.node_values[node_id],
            }
            for node_id, node_data in graph.nodes.items()
        ],
        "edges": [
            {
                "source": source,
                **edge,
            }
            for source, edges in graph.edges.items()
            for edge in edges
        ],
    }
    with open(GRAPH_FILE, "w") as file:
        json.dump(graph_data, file, indent=4)
    print(f"Graph saved to {GRAPH_FILE}.")


def load_graph_from_file():
    """
    Loads the graph state from a file.
    """
    if not os.path.exists(GRAPH_FILE):
        return Logician()  # Return an empty graph if the file doesn't exist

    with open(GRAPH_FILE, "r") as file:
        data = json.load(file)

    graph = Logician()

    # Recreate nodes
    for node in data["nodes"]:
        graph.add_node(node["id"], node["label"], node["color"])
        graph.node_values[node["id"]] = node["value"]

    # Recreate edges
    for edge in data["edges"]:
        graph.add_edge(
            edge["source"],
            edge["target"],
            edge["relation"],
            edge["color"],
            edge["group"],
        )

    print(f"Graph loaded from {GRAPH_FILE}.")
    return graph


def append_logic(graph, conditions, action, operator, group):
    """
    Appends new logic to the existing graph.
    """
    graph.add_logic(conditions, action, operator, group)
    save_graph_to_file(graph)
    print(f"Added logic: {conditions} {operator} -> {action}")


def main():
    # Load existing graph or create a new one
    graph = load_graph_from_file()

    # Append new logic to the graph
    append_logic(graph, ["A", "B"], "C", "AND", "AB")
    append_logic(graph, ["C"], "D", "IMPLIES", "C")
    append_logic(graph, ["D"], "E", "NOT", "D")
    append_logic(graph, ["A", "E"], "F", "OR", "AE")

    # Evaluate graph with updates
    updates = [["A", True], ["B", True]]  # Set A and B to True
    graph.update_graph(updates)

    # Print final truth values
    print("Final truth values:", graph.node_values)

    # Export final graph structure
    graph.export_to_json()


if __name__ == "__main__":
    main()
