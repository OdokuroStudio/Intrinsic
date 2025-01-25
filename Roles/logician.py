import json

class Logician:
    def __init__(self):
        # TODO: tree for these or search time is gonna become a big ol problem when propagating frequently

        self.nodes = []  # List of nodes
        self.edges = []  # List of edges
        self.node_values = {}  # Dictionary to store truth values of nodes

    def add_node(self, node_id, label, color="skyblue"):
        """
        Adds a unique node to the graph.
        """
        if not any(node["id"] == node_id for node in self.nodes):
            self.nodes.append({"id": node_id, "label": label, "color": color})
            self.node_values[node_id] = False  # Initialize node value as False

    def add_edge(self, source, target, operator, color, group):
        """
        Adds a directed edge between two nodes.
        """
        self.edges.append({"source": source, "target": target, "relation": operator, "color": color, "group": group})

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

        print(self.nodes)
        print(self.edges)

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

            print(f"Updated node '{node_id}' to {'True' if node_value else 'False'}")



    def propagate(self):
        """
        Propagates the updated node values to nodes that have no direct input
        """
        for node in self.node_values:
            node_id = node.key
            node_value = node.value

    def export_to_json(self, output_file="../Graphs/graph_data.json"):
        """
        Exports the graph to a JSON file.
        """
        graph_data = {
            "nodes": [{"id": node["id"], "label": node["label"], "color": node["color"], "value": self.node_values[node["id"]]} for node in self.nodes],
            "edges": self.edges,
        }
        with open(output_file, "w") as file:
            json.dump(graph_data, file, indent=4)
        print(f"Graph data saved to {output_file}")
