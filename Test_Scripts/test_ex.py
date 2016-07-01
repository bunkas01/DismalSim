import graph
import deltacalc

""""Test Script.

naming scheme for test scripts: < test_xx >, where xx is a number, e.g.
01, 23.
"""


# First, build the graph, adding all requisite vertices and edges, with
# the appropriate relationships.
aGraph = graph.Graph()
aGraph.add_vertex("A", 10)
aGraph.add_vertex("B", 10)
aGraph.add_vertex("C", 10)
aGraph.add_vertex("D", 10)
aGraph.add_edge("A", "B", "abs_linear", [2, 2])
aGraph.add_edge("A", "C", "per_linear", [10, 15])
aGraph.add_edge("B", "D", "def_proportional", [1])
aGraph.add_edge("C", "D", "def_proportional", [1])
aGraph.add_edge("D", "A", "abs_proportional", [2])

# Next, define the initial changes, in a dictionary. Use the names of
# the vertices as the dictionary keys, and the changes as the values.
iDelta = {"A": 20, "B": 5}

# Now, run the sim itself, for a specified number of cycles.
output = deltacalc.gc_multicount_delta(aGraph, 10, iDelta)

# Finally, write the output to a spreadsheet to make using it easier.
deltacalc.output_spreadsheet("test_ex_data", output)

# When writing your script, don't forget to use module names where
# necessary!