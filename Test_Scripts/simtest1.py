import digraph

from Depreciated_Modules.deltafunctions import multicount_delta_application
from Depreciated_Modules.deltafunctions import write_output_to_spreadsheet

"""Early testing script making use of delta application functions.

The script generates a simplified version of the macroeconomic DiGraph
that this project is intended to use for simulations. The relationships
of the Nodes are similarly simplified, as all are assumed to have
proportional transforms. The coefficients used for the TransformEdges
are based on relatively early calculations of assorted marginal
propensities.
"""

miniMacro = digraph.DiGraph()
miniMacro.add_node("T", 1712.9)
miniMacro.add_node("G", 1920.2)
miniMacro.add_node("C", 3825.6)
miniMacro.add_node("Y", 5979.6)
miniMacro.add_node("B", -78.969)
miniMacro.add_node("X", 535.234)
miniMacro.add_edge("T", "G", "proportional", ["coefficient"], [1])
miniMacro.add_edge("G", "Y", "proportional", ["coefficient"], [1])
miniMacro.add_edge("C", "Y", "proportional", ["coefficient"], [1])
miniMacro.add_edge("B", "Y", "proportional", ["coefficient"], [1])
miniMacro.add_edge("X", "B", "proportional", ["coefficient"], [1])
miniMacro.add_edge("Y", "T", "proportional", ["coefficient"], [.29])
miniMacro.add_edge("T", "C", "proportional", ["coefficient"], [-.93])
miniMacro.add_edge("Y", "C", "proportional", ["coefficient"], [.93])
miniMacro.add_edge("Y", "B", "proportional", ["coefficient"], [-.1])
print(miniMacro, "\n")

initChanges = {"G": 9.53, "T": 4.2, "C": 11.22, "Y": 16.2, "B": 6.82,
               "X": 3.6}
simOutput = multicount_delta_application(miniMacro, 100, initChanges)
write_output_to_spreadsheet("sim_test_data_001", simOutput)
print(miniMacro)
