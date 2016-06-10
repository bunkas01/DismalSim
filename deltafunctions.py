import digraph
import graphtestingalgorithms

__author__ = "Ashleigh"

"""Placeholder Docstring"""


def count_sinpo_dap(aGraph, startNodeName, startDelta):
    """Single-Point Floating-Delta Application, mediated by a counter."""
    count = 0
    startNode = aGraph.get_node(startNodeName)
    startNode += startDelta

    while count <= aGraph.get_max_distance():
        for node in aGraph.get_all_nodes():
            if node.get_distance() == count:
                for edge in node.get_all_edges():
                    edge.transform()
        count += 1
    for node in aGraph.get_all_nodes():
        node.apply_delta()


def colour_sinpo_dap(aGraph, startNodeName):
    """Single-Point Floating-Delta Application, mediated by Node colour."""
    pass


def main():
    """Testing Script for delta application functions."""

    aGraph = digraph.DiGraph()
    aGraph.add_node("A", 30)
    aGraph.add_node("B", 30)
    aGraph.add_node("C", 30)
    aGraph.add_node("D", 30)
    aGraph.add_node("E", 30)
    aGraph.add_edge("A", "B", "proportional", ["coefficient"], [1])
    aGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.5])
    aGraph.add_edge("B", "C", "proportional", ["coefficient"], [1])
    aGraph.add_edge("B", "D", "proportional", ["coefficient"], [1])
    aGraph.add_edge("C", "E", "proportional", ["coefficient"], [1])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.5])
    aGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.5])
    print(aGraph)
    print("\n")

    graphtestingalgorithms.basic_breadth_first_traversal(aGraph, "A")
    # print(aGraph.get_max_distance())
    # print(aGraph)
    # for edge in aGraph.get_all_edges():
    #     print(edge)
    # print("\n")
    count_sinpo_dap(aGraph, "A", 15)
    print(aGraph)
    graphtestingalgorithms.reset_nodes(aGraph)

    # graphtestingalgorithms.basic_breadth_first_traversal(aGraph, "D")
    # print(aGraph.get_max_distance())
    # print(aGraph)
    # print("\n")
    # count_sinpo_dap(aGraph, "D", 15)
    # print(aGraph)
    # graphtestingalgorithms.reset_nodes(aGraph)


if __name__ == '__main__':
    main()
