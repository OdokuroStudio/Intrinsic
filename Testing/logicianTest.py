from logician import *

def main():
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


if __name__ == "__main__":
    main()
