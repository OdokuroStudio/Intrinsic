import torch
from collections import defaultdict
import json
from logician import Logician


class Philosopher:
    def __init__(self, graph: Logician, hidden_space_size: int):
        """
        Initializes the Philosopher, which maps logical nodes to neural network hidden layer activations
        and tracks their correlations.

        :param graph: An instance of the Logician class.
        :param hidden_space_size: The number of nodes in the hidden layers of the neural network.
        """
        self.graph = graph  # Reference to the Logician graph
        self.hidden_space_size = hidden_space_size

        # Track mappings between logical nodes and neural nodes
        self.node_correlation_map = defaultdict(list)  # {node_id: [hidden_indices]}

        # Track activation values for correlation analysis
        self.node_tracker = defaultdict(lambda: torch.zeros(hidden_space_size))  # {node_id: tensor(hidden_space_size)}

    def map_node_to_hidden(self, node_id, hidden_indices):
        """
        Maps a logical node to one or more neural network hidden layer nodes.

        :param node_id: The ID of the logical node.
        :param hidden_indices: A list of indices corresponding to hidden layer nodes.
        """
        if node_id not in self.graph.nodes:
            raise ValueError(f"Node '{node_id}' does not exist in the graph.")

        self.node_correlation_map[node_id].extend(hidden_indices)
        print(f"Mapped node '{node_id}' to hidden nodes {hidden_indices}.")

    def observe_hidden_activations(self, node_states, hidden_activations):
        """
        Observes which symbolic nodes are active and records their correlation with hidden layer activations.

        :param node_states: A dictionary of current node truth values (from Logician).
        :param hidden_activations: A tensor of hidden layer activation values.
        """
        for node_id, is_true in node_states.items():
            if is_true:
                self.node_tracker[node_id] += hidden_activations

        print(f"Observed activations: Node states={node_states}, Hidden activations={hidden_activations.tolist()}")

    def get_correlations(self):
        """
        Returns a summary of the correlations between symbolic nodes and hidden layer activations.

        :return: A dictionary of correlations {node_id: [normalized_hidden_correlations]}.
        """
        correlations = {}
        for node_id, activation_totals in self.node_tracker.items():
            total_activations = torch.sum(activation_totals)
            if total_activations > 0:
                correlations[node_id] = (activation_totals / total_activations).tolist()
            else:
                correlations[node_id] = [0] * self.hidden_space_size

        return correlations

    def export_correlations_to_json(self, output_file="correlations.json"):
        """
        Exports the current correlations to a JSON file.

        :param output_file: The file to save the correlations.
        """
        correlations = self.get_correlations()
        with open(output_file, "w") as file:
            json.dump(correlations, file, indent=4)
        print(f"Correlations saved to {output_file}")
