import sys

from Depreciated_Modules import digraph

"""Assorted algorithms for testing DiGraph Functionality.

Three of the functions in the module are representative of the actual
testing algorithms; the rest are assorted helper functions. The
wyatt_cauasality_reversal function is named in reference to the
causality reversal procedure used by Geoffrey Wyatt in the text that
serves as the basis for the economic simulations for which this project
is intended to be used. The other two testing algorithms are just
basic breadth-first and depth-first traversals.

Functions:
    - wyatt_causality_reversal, reverses causal relationship between
      two given Nodes.
    - find_node_path, given a list of edges between two given Nodes,
      determines all Nodes traversed along that path.
    - adjust_covnerging_edges, adjusts edges during causality reversal.
    - brute_find_path, performs a modified depth-first search.
    - basic_breadth_first_traversal, traverses the graph from a
      designated start Node.
    - reset_nodes, resets traversal data associated with the graph's
      Nodes.
    - basic_depth_first_traversal, traverses the graph from a
      designated start Node.
    - depth_first_visit, called recursively in a depth-first traversal.
"""


def wyatt_causality_reversal(aGraph, startNodeName, endNodeName):
    """Reverses causality between two Nodes, modifies graph.

    The graph is modified in place, with the directionality reversal
    occurring within the function proper, but the adjustment of
    converging edges is done by a helper function. The other helper
    functions are primarily focused on pathfinding. This function
    mutates the graph in place and has no return value.

    The function arguments are as follows:
        - aGraph, the graph for which causality is to be reversed.
        - startNodeName, the name of one of the Nodes between which
          causality is to be reversed. More specifically, it represents
          the initial 'source' of the flow of causality.
        - endNodeName, the name of the other Node between which
          causality is to be reversed. More specifically, it represents
          the initial 'sink' of the flow of causality.
        - The function does not support positional or keyword
          arguments.
    """

    emptyPath = []
    startNode = aGraph.get_node(startNodeName)
    endNode = aGraph.get_node(endNodeName)
    edgePath = brute_find_path(aGraph, startNode, endNode, emptyPath)
    nodePath = find_node_path(edgePath)
    for edge in edgePath:
        edge.reverse()
        edge.change_invert()
    adjust_converging_edges(aGraph, edgePath, nodePath)
    reset_nodes(aGraph)



def find_node_path(edgePath):
    """Helper function for wyatt_causality_reversal.

    This function takes the list of edges between two Nodes and
    generates a list of all Nodes that would be traversed between the
    start and end points. This list is returned.

    The function arguments are as follows:
        - edgePath, the list of edges between the start and end Nodes
          in the causality reversal.
        - the function does not support positional or keyword
          arguments.
    """

    nodePath = []
    nodePath.append(edgePath[0].get_parent_node())
    for edge in edgePath:
        nodePath.append(edge.get_child_node())
    return nodePath


def adjust_converging_edges(aGraph, edgePath, nodePath):
    """Helper function for wyatt_causality_reversal.

    This function takes a list of edges and Nodes traversed between two
    points on a graph, finds all edges that converge onto Nodes in the
    path (and also aren't part of the path), and adjusts them 'down'
    the causality flow, as outlined in Wyatt's text. This modification
    occurs in place, and the function has no return value.

    The function arguments are as follows:
        - aGraph, the graph to be modified.
        - edgePath, the list of edges traversed between a 'source' and
          'sink' Node.
        - nodePath, the list of Nodes traversed when following the
          edgePath.
        - the function does not support positional or keyword
          arguments.
    """

    allEdges = aGraph.get_all_edges()
    for edge in allEdges:
        if edge not in edgePath and edge.get_child_node() in nodePath:
            oldChild = edge.get_child_node()
            newChildIndex = nodePath.index(oldChild) - 1
            if newChildIndex >= 0:
                edge.set_child_node(nodePath[newChildIndex])
                edge.change_negation()
                edge *= oldChild.get_edge_by_child(nodePath[newChildIndex])


def brute_find_path(aGraph, startNode, endNode, edgePath):
    """Helper function for wyatt_causality_reversal.

    This function takes a graph, start and end Nodes, and an empty list
    for the path. From here, it uses a modified depth-first search to
    locate the end position from the start position and traces back the
    path taken by the branch of the depth-first tree, adding the
    edges traversed to the edge path, before returning the list of
    edges. Since the algorithm will explore all possible paths if
    necessary, the search is a brute-force one.

    The function arguments are as follows:
        - aGraph, the graph to be brute-force searched.
        - startNode, the Node at which the search will start.
        - endNode, the Node being searched for.
        - edgePath, the empty list to which to add edges in the path.
        - the function does not support positional or keyword
          arguments.
    """

    for edge in startNode.get_all_edges():
        targetNode = edge.get_child_node()
        targetNode.set_searched_edge(edge)
        if targetNode != endNode:
            brute_find_path(aGraph, targetNode, endNode, edgePath)
        elif targetNode == endNode:
            edgePath.insert(0, edge)
            for pathEdge in reversed(edgePath):
                if pathEdge.get_parent_node().get_searched_edge() is not None:
                    nextEdge = pathEdge.get_parent_node().get_searched_edge()
                    edgePath.insert(0, nextEdge)
    return edgePath


def basic_breadth_first_traversal(aGraph, startNodeName):
    """A simple breadth-first traversal algorithm for the DiGraph.

    The traversal takes a graph to traverse and a given start Node. It
    uses the colour of the Nodes to determine whether they are valid
    targets for exploration, as well as setting the distance from the
    start Node as it runs. It simply traverses the graph and does not
    search or significantly modify it; it has no return value.

    The function arguments are as follows:
        - aGraph, the graph to be traversed.
        - startNodeName, the name of the Node from which to begin
          traversing.
        - the function does not support positional or keyword
          arguments.
    """

    searchQueue = []
    startNode = aGraph.get_node(startNodeName)
    startNode.set_distance(0)
    startNode.set_colour("grey")
    searchQueue.append(startNode)

    for node in searchQueue:
        for edge in node.get_all_edges():
            targetNode = edge.get_child_node()
            if targetNode.get_colour() == "white":
                targetNode.set_distance(node.get_distance() + 1)
                aGraph.set_max_distance(targetNode.get_distance())
                targetNode.set_colour("grey")
                targetNode.set_searched_edge(edge)
                searchQueue.append(targetNode)
        node.set_colour("black")


def reset_nodes(aGraph):
    """Resets traversal-related data for all Nodes in a graph.

    The function takes a graph and modifies it in place by calling the
    reset_traversal_data method for Nodes within the graph. After this,
    it resets the graph's maximum distance to the default value of the
    system's maximum integer. Since it modifies the graph in place, the
    function has no return value.

    The function arguments are as follows:
        - aGraph, the graph in need of having its traversal data reset.
        - the function does not support positional or keyword
          arguments.
    """

    for node in aGraph.get_all_nodes():
        node.reset_traversal_data()
    aGraph.set_max_distance(sys.maxsize)


def basic_depth_first_traversal(aGraph, startNodeName):
    """A simple depth-first traversal algorithm for the DiGraph.

    Given the name of a start Node within a graph, the function
    traverses the graph along a depth-first tree, setting discovery and
    finishing times as appropriate. Most of the traversal is done by a
    helper function, with this serving primarily as a wrapper function.
    Part of this includes initializing a timer, to be passed to the
    depth_first_visit function during the actual traversal.

    The function arguments are as follows:
        - aGraph, the graph to be traversed.
        - startNodeName, the name of the Node from which to begin the
          traversal.
        - the function does not support positional or keyword
          arguments.
    """

    startNode = aGraph.get_node(startNodeName)
    timer = 0
    depth_first_visit(startNode, timer)

def depth_first_visit(startNode, timer):
    """Helper function for basic_depth_first_traversal.

    The function calls itself recursively, visiting the first
    undiscovered Node (indicated by the default discovery time of 0)
    available to the current function call's startNode. The timer is
    returned between calls of the function, to keep the discovery and
    finishing times from colliding between branches of the depth-first
    tree.

    The function arguments are as follows:
        - startNode, the Node from which to search for adjacent Nodes.
        - timer, the timer keeping track of discovery and finish times
          across recursive calls of the function.
        - the function does not support positional or keyword
          arguments.
    """

    timer += 1
    startNode.set_discovered_time(timer)
    for edge in startNode.get_all_edges():
        nextNode = edge.get_child_node()
        if nextNode.get_discovered_time() == 0:
            timer = depth_first_visit(nextNode, timer)
    timer += 1
    startNode.set_finished_time(timer)
    return timer


def main():
    """Test script for the assorted graph testing functions.

    A graph is instantiated, and five Nodes (A, B, C, D, E) are added
    to it. Four edges are added, and then the graph, as well as all
    edges contained within the graph, are printed to the screen. Next,
    the wyatt_causality_reversal function is called, modifying the
    graph. The modified graph is printed to the screen, and then yet
    another edge is added, to make all Nodes discoverable from E in the
    traversals. Finally, both breadth-first and depth-first traversals
    of the graph are completed, with the graph printed after each one
    to demonstrate their effects.
    """

    aGraph = digraph.DiGraph()
    aGraph.add_node("A")
    aGraph.add_node("B")
    aGraph.add_node("C")
    aGraph.add_node("D")
    aGraph.add_node("E")
    aGraph.add_edge("A", "D", "proportional", ["coefficient"], [2])
    aGraph.add_edge("C", "D", "proportional", ["coefficient"], [2])
    aGraph.add_edge("D", "B", "proportional", ["coefficient"], [2])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [2])

    print("This is the initial graph: \n")
    print(aGraph)
    for edge in aGraph.get_all_edges():
        print(edge)
    print("Performing Wyatt Causality Reversal: \n")
    wyatt_causality_reversal(aGraph, "A", "E")
    print(aGraph)
    for edge in aGraph.get_all_edges():
        print(edge)

    aGraph.add_edge("E", "C", "proportional", ["coefficient"], [2])
    basic_breadth_first_traversal(aGraph, "E")
    print("\n", "this is the graph after a breadth first traversal", "\n",
          aGraph)
    reset_nodes(aGraph)
    basic_depth_first_traversal(aGraph, "E")
    print("\n", "this is the graph after a depth first traversal", "\n", aGraph)
    reset_nodes(aGraph)


if __name__ == '__main__':
    main()
