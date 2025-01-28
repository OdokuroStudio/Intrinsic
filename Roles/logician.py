# logician.py

import json

class Logician:
    def __init__(self):
        self.nodes = {}
        self.edges = {}
        self.node_values = {}  # Dictionary to store truth values of nodes

    def add_node(self, node_id, label, color="skyblue"):
        """
        Adds nodes to the graph.
        """
        if node_id not in self.nodes:
            self.nodes[node_id] = {"label": label, "color": color}
            self.node_values[node_id] = False

    def add_edge(self, source, target, operator, color, group):
        """
        Adds a directed edge between two nodes.
        """
        if source not in self.edges:
            self.edges[source] = []
        self.edges[source].append({"target": target, "relation": operator, "color": color, "group": group})

    def add_logic(self, conditions, action, operator, group):
        """
        Connects multiple conditions directly to the action, with edges representing the operator.
        """
        operator_colors = {
            "AND": "orange",
            "OR": "purple",
            "IMPLIES": "red",
            "NOT": "blue"
        }
        edge_color = operator_colors.get(operator, "gray")

        # Add each condition as a separate node and connect to the action
        for condition in conditions:
            self.add_node(condition, condition, "skyblue")
            self.add_node(action, action, "lightgreen")
            self.add_edge(condition, action, operator, edge_color, group)

    def load_from_json(self, input_file="../Graphs/graph_data.json"):
        """
        Loads a graph from a JSON file and appends its data to the current graph.
        """
        try:
            with open(input_file, "r") as file:
                graph_data = json.load(file)

            # Append nodes
            for node in graph_data["nodes"]:
                node_id = node["id"]
                self.add_node(node_id, node["label"], node["color"])
                self.node_values[node_id] = node.get("value", False)

            # Append edges
            for edge in graph_data["edges"]:
                self.add_edge(
                    edge["source"],
                    edge["target"],
                    edge["relation"],
                    edge["color"],
                    edge.get("group", [])
                )
            print(f"Graph data loaded and appended from {input_file}")
        except FileNotFoundError:
            print(f"File {input_file} not found. Starting with an empty graph.")

    def propagate(self, updated_nodes):
        """
        Propagates the updated node values through the graph.
        """
        for node_id, node_value in updated_nodes:
            # Check if the node has outgoing edges
            if node_id not in self.edges:
                continue

            # Iterate through edges originating from this node
            for edge in self.edges[node_id]:
                target = edge["target"]
                operator = edge["relation"]
                group = edge.get("group", [])

                # Process based on operator
                if operator == "IMPLIES":
                    self.node_values[target] = not node_value
                elif operator == "NOT":
                    self.node_values[target] = not node_value
                elif operator == "AND":
                    self.node_values[target] = all(self.node_values.get(n, False) for n in group)
                elif operator == "OR":
                    self.node_values[target] = any(self.node_values.get(n, False) for n in group)

        print("Node values after propagation:", self.node_values)

    def update_graph(self, updated_nodes):
        """
        Updates the node values in the graph (without propagation)
        """
        for node in updated_nodes:
            node_id = node[0]
            node_value = node[1]

            if node_id not in self.node_values:
                raise ValueError(f"Node '{node_id}' does not exist.")

            self.node_values[node_id] = node_value

        self.propagate(updated_nodes)

    def export_to_json(self, output_file="../Graphs/graph_data.json"):
        """
        Exports the graph to a JSON file.
        """
        graph_data = {
            "nodes": [
                {
                    "id": node_id,
                    "label": node_data["label"],
                    "color": node_data["color"],
                    "value": self.node_values[node_id],
                }
                for node_id, node_data in self.nodes.items()
            ],
            "edges": [
                {
                    "source": source,
                    **edge
                }
                for source, edges in self.edges.items()
                for edge in edges
            ],
        }
        with open(output_file, "w") as file:
            json.dump(graph_data, file, indent=4)
        print(f"Graph data saved to {output_file}")
