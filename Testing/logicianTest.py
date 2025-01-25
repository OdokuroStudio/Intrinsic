from Roles.logician import *

def main():
    graph = Logician()

    # Define nodes and logic
    graph.add_logic(["A", "B"], "C", "AND", "ABC")  # C is true if A AND B are true
    graph.add_logic(["C"], "D", "IMPLIES", "CD")  # D is true if C is true
    graph.add_logic(["D"], "E", "NOT", "DE")      # E is true if D is false

    # Evaluate graph with initial updates
    updates = [["A", True], ["B", True]]  # Set A and B to True
    final_state = graph.update_graph(updates)

    # Print final truth values
    print("Final truth values:", final_state)

    # Export graph
    graph.export_to_json()


if __name__ == "__main__":
    main()
