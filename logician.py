from pyvis.network import Network


class MinecraftLogicGraph:
    def __init__(self):
        self.graph = {}
        self.network = Network(height="750px", width="100%", notebook=False, directed=True)

    def add_condition(self, condition):
        """
        Adds a condition node to the graph.

        """
        if condition not in self.graph:
            self.graph[condition] = []
            self.network.add_node(condition, label=condition, color="skyblue", shape="ellipse")

    def add_action(self, action):
        """
        Adds an action node to the graph.

        """
        if action not in self.graph:
            self.graph[action] = []
            self.network.add_node(action, label=action, color="lightgreen", shape="box")

    def add_logic(self, conditions, action, description, operator="AND"):
        """
        Add a logical rule to the graph.

        :param conditions: List of condition nodes.
                           For "IMPLIES", it should be [A] where A implies the action.
                           For other operators, this can be multiple conditions.
        :param action: The action (node) resulting from the conditions.
        :param description: Description of the logical relationship.
        :param operator: Logical operator ("AND", "OR", "IMPLIES", "NOT").
        """
        operator_node = None

        if operator == "IMPLIES":
            if len(conditions) != 1:
                raise ValueError("IMPLIES operator requires exactly one condition [A] where A implies the action.")
            condition = conditions[0]
            operator_node = f"(IMPLIES): {condition} → {action}"
            self.add_condition(condition)
            self.add_action(action)

            # Add operator node and connect it
            self.network.add_node(operator_node, label="IMPLIES", color="orange", shape="diamond")
            self.graph[condition] = self.graph.get(condition, []) + [operator_node]
            self.graph[operator_node] = [action]
            self.network.add_edge(condition, operator_node, title="If True, Implies")
            self.network.add_edge(operator_node, action, title=description)

        elif operator in {"AND", "OR"}:
            operator_node = f"({operator}): " + (" ∧ ".join(conditions) if operator == "AND" else " ∨ ".join(conditions))
            self.network.add_node(operator_node, label=operator, color="orange", shape="diamond")
            self.graph[operator_node] = []
            for condition in conditions:
                self.add_condition(condition)
                self.graph[condition] = self.graph.get(condition, []) + [operator_node]
                self.network.add_edge(condition, operator_node, title=f"Part of {operator}")

            self.add_action(action)
            self.graph[operator_node].append(action)
            self.network.add_edge(operator_node, action, title=description)

        elif operator == "NOT":
            if len(conditions) != 1:
                raise ValueError("NOT operator requires exactly one condition.")
            condition = conditions[0]
            operator_node = f"(NOT): ¬{condition}"
            self.add_condition(condition)
            self.add_action(action)  # Ensure the action node is added
            self.network.add_node(operator_node, label="NOT", color="orange", shape="diamond")
            self.graph[condition] = self.graph.get(condition, []) + [operator_node]
            self.graph[operator_node] = [action]
            self.network.add_edge(condition, operator_node, title="Negates")
            self.network.add_edge(operator_node, action, title=description)

        else:
            raise ValueError(f"Unsupported operator: {operator}")

    def visualize(self, output_file="logic_graph.html"):
        """
        Generates and saves an interactive visualization of the graph with a dark theme.

        """
        self.network.write_html(output_file)

        with open(output_file, "r") as file:
            html = file.read()

        dark_theme = """
        <style>
            body { background-color: #1e1e2f; color: #c0c0c0; }
            .vis-network { background-color: #1e1e2f; }
            .node { color: #f1f1f1; }
        </style>
        """
        html = html.replace("</head>", dark_theme + "</head>")

        with open(output_file, "w") as file:
            file.write(html)

        print(f"Graph visualization saved as {output_file} with a dark theme.")


# Example usage
if __name__ == "__main__":
    logic_graph = MinecraftLogicGraph()

    # Adding logic rules
    logic_graph.add_logic(["Hungry", "Has Food"], "Eat Food", "Restores hunger", operator="AND")
    logic_graph.add_logic(["Has Sword", "Enemy Nearby"], "Attack Enemy", "Fight enemies when armed", operator="AND")
    logic_graph.add_logic(["Low Health", "Enemy Nearby"], "Retreat", "Avoid combat when weak", operator="OR")
    logic_graph.add_logic(["Daylight"], "Safety", "Daylight implies safety from hostile mobs", operator="IMPLIES")
    logic_graph.add_logic(["Lava Nearby"], "Avoid Lava", "Lava is dangerous", operator="IMPLIES")
    logic_graph.add_logic(["Lava Nearby"], "Safe to Proceed", "No lava means it's safe", operator="NOT")

    # Visualize
    logic_graph.visualize("minecraft_logic_graph.html")

