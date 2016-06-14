import digraph

__author__ = "Ashleigh"

"""Placeholder Docstring"""


# def count_sinpo_dap(aGraph, startNodeName, startDelta):
#     """Single-Point Floating-Delta Application, mediated by a counter."""
#     count = 0
#     startNode = aGraph.get_node(startNodeName)
#     startNode += startDelta
#
#     while count <= aGraph.get_max_distance():
#         for node in aGraph.get_all_nodes():
#             if node.get_distance() == count:
#                 for edge in node.get_all_edges():
#                     edge.transform()
#         count += 1
#     for node in aGraph.get_all_nodes():
#         node.apply_delta()
#
#
# def colour_sinpo_dap(aGraph, startNodeName):
#     """Single-Point Floating-Delta Application, mediated by Node colour."""
#     pass


def multicount_delta_application(aGraph, maxCount, initDeltaDict):
    """Multi-point count-mediated delta application algorithm."""
    count = 0
    for key in initDeltaDict:
        if key in aGraph:
            targetNode = aGraph.get_node(key)
            initDelta = initDeltaDict[key]
            targetNode.set_delta_new(initDelta)
    aGraph.apply_all_new_deltas()
    count += 1
    while count <= maxCount:
        for node in aGraph.get_all_nodes():
            for edge in node.get_all_edges():
                edge.transform()
        aGraph.apply_all_new_deltas()
        count += 1


def main():
    """Testing Script for delta application functions."""

    aGraph = digraph.DiGraph()
    aGraph.add_node("A", 30)
    aGraph.add_node("B", 30)
    aGraph.add_node("C", 30)
    aGraph.add_node("D", 30)
    aGraph.add_node("E", 30)
    aGraph.add_edge("A", "B", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "C", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "D", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("C", "E", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.25])
    print(aGraph)
    print("\n")

    multicount_delta_application(aGraph, 4, {"A": 120, "E": 120})
    print(aGraph)


if __name__ == '__main__':
    main()
