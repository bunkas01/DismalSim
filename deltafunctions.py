import digraph

__author__ = "Ashleigh"

"""Assorted algorithms for calculating and applying changes to graphs.

The Delta Application Functions are what allows the directed graph
implementation used in this project to be used as part of an economic
simulation, as they govern how changes spread between Nodes that
represent components of the macroeconomy.

Currently, only a single delta application function has been
implemented, though there will be more to come, some of which may just
be modifications or complications of the multicount_delta_application
function initially implemented. Additionally, helper functions to write
function output to text files may be added.

Functions:
    - multicount_delta_application, applies changes from multiple
      sources over time.
"""


def multicount_delta_application(aGraph, maxCount, initDeltaDict):
    """Multiple-point count-mediated delta application algorithm.

    Given a graph, a maximum system count to run the algorithm for, and
    a dictionary of initial delta values, the function modifies the
    graph in place, cyclically applying changes to any given Node based
    on the changes that the Node's parent Nodes experienced during the
    previous system count, modified by the transform functions assigned
    to the TransformEdges linking the Nodes. This cyclic delta
    application continues until the maximum count is reached.
    Additionally, the function maintains a log of the values of each
    Node in the graph after each system count, maintained in a list of
    values, and each Node has its own sublist of values. That
    list-of-lists is returned at the end of the function, to provide
    a more accessible log of all the changes that occurred during the
    algorithms runtime.

    The function arguments are as follows:
        - aGraph, the graph to calculate and apply changes to.
        - maxCount, the maximum number of delta calculation-application
          cycles to complete.
        - initDeltaDict, a dictionary of the initial changes to apply
          to start the simulation, with the names of the Nodes to which
          changes should be applied serving as keys.
        - the function does not support positional or keyword
          arguments.
    """

    nodeDataList = []
    for node in aGraph.get_all_nodes():
        nodeData = []
        nodeData.append(node.get_name())
        nodeData.append(node.get_data())
        nodeDataList.append(nodeData)
    count = 0
    for key in initDeltaDict:
        if key in aGraph:
            targetNode = aGraph.get_node(key)
            initDelta = initDeltaDict[key]
            targetNode.set_delta_new(initDelta)
    aGraph.apply_all_new_deltas()
    i = 0
    for node in aGraph.get_all_nodes():
        nodeDataList[i].append(node.get_data())
        i += 1
    count += 1
    while count <= maxCount:
        for node in aGraph.get_all_nodes():
            for edge in node.get_all_edges():
                edge.transform()
        aGraph.apply_all_new_deltas()
        i = 0
        for node in aGraph.get_all_nodes():
            nodeDataList[i].append(node.get_data())
            i += 1
        count += 1
    return nodeDataList


def main():
    """Testing Script for delta application functions.

    A graph is instantiated, and five Nodes (A, B, C, D, E) are added
    to it. Assorted TransformEdges are created, all with the same
    transform type and transform parameters. This graph is printed to
    the screen, then the multicount_delta_application function is
    called on it, followed by being printed to the screen again. After
    this, a second, similar graph is instantiated, and has Nodes and
    TransformEdges added. This graph also has the
    multicount_delta_application algorithm used on it, and is printed
    to the screen. Additionally, the list of change data returned by
    the algorithm is also printed to the screen.
    """

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

    bGraph = digraph.DiGraph()
    bGraph.add_node("A", 30)
    bGraph.add_node("B", 30)
    bGraph.add_node("C", 30)
    bGraph.add_node("D", 30)
    bGraph.add_node("E", 30)
    bGraph.add_edge("A", "B", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "C", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "D", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("C", "E", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.5])
    print(bGraph)
    print("\n")

    allData = multicount_delta_application(bGraph, 20, {"A": 120, "E": 120})
    print(bGraph)
    for subList in allData:
        print(subList)


if __name__ == '__main__':
    main()
