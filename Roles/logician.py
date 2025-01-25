import json

class Logician:
    def __init__(self):
        self.nodes = []  # List of nodes
        self.edges = []  # List of edges

    def add_node(self, node_id, label, color="skyblue"):
        """
        Adds a unique node to the graph.
        """
        if not any(node["id"] == node_id for node in self.nodes):
            self.nodes.append({"id": node_id, "label": label, "color": color})

    def add_edge(self, source, target, operator, color):
        """
        Adds a directed edge between two nodes.
        """
        self.edges.append({"source": source, "target": target, "relation": operator, "color": color})

    def add_logic(self, conditions, action, operator="AND"):
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
            self.add_edge(condition, action, operator, edge_color)

    def export_to_json(self, output_file="../Graphs/graph_data.json"):
        """
        Exports the graph to a JSON file.
        """
        graph_data = {"nodes": self.nodes, "edges": self.edges}
        with open(output_file, "w") as file:
            json.dump(graph_data, file, indent=4)
        print(f"Graph data saved to {output_file}")
