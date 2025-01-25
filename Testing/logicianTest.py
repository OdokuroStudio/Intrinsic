from Roles.logician import *

def main():
    graph = Logician()

    # Add nodes and logic
    graph.add_logic(["A", "B"], "C", "AND")
    graph.add_logic(["A", "D"], "F", "OR")
    graph.add_logic(["C"], "D", "IMPLIES")
    graph.add_logic(["D"], "E", "NOT")

    # Export to JSON
    graph.export_to_json()


if __name__ == "__main__":
    main()
