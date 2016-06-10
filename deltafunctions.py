import digraph

__author__ = "Ashleigh"

"""Placeholder Docstring"""


def count_sinpo_dap(aGraph, startNodeName):
    """Single-Point Floating-Delta Application, mediated by a counter."""
    pass


def colour_sinpo_dap(aGraph, startNodeName):
    """Single-Point Floating-Delta Application, mediated by Node colour."""
    pass


def main():
    aGraph = digraph.DiGraph()
    aGraph.add_node("A", 10)
    aGraph.add_node("B", 20)
    aGraph.add_node("C", 30)
    aGraph.add_node("D", 40)
    aGraph.add_node("E", 50)
    aGraph.add_edge("A", "B", "proportional", ["coefficient"], [1])
    aGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.5])
    aGraph.add_edge("B", "C", "proportional", ["coefficient"], [1])
    aGraph.add_edge("B", "D", "proportional", ["coefficient"], [1])
    aGraph.add_edge("C", "E", "proportional", ["coefficient"], [1])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.5])
    aGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.5])
    print(aGraph)


if __name__ == '__main__':
    main()
