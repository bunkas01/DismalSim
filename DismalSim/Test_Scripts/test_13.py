from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import digraph

"""Scripting the model from 1990-1999, with concurrent regressions.

The script constructs a graph corresponding to a modified version of
the base economic model, and runs it through the time period of
1990-1999; modifications to the model were the removal of edges linking
the Imports and Exports vertices to the Foreign-Exchange Vertex, as well
as the complete removal of the Nominal Interest rate Vertex.
Additionally, regressions were recalculated without these edges
present. The regressions used to calculate edge relationships were
performed over the same time period, in order to test the fundamental
robustness of the model.
"""

aGraph = digraph.DiGraph()
aGraph + digraph.Vertex("G", 1920.2, deltaInherent=-73.5)
aGraph + digraph.Vertex("T", 1712.9, deltaInherent=30.9)
aGraph + digraph.Vertex("YD", 4266.7)
aGraph + digraph.Vertex("C", 3825.6, deltaInherent=40.1)
aGraph + digraph.Vertex("IM", 629.7, deltaInherent=30.3)
aGraph + digraph.Vertex("Y", 5979.6)
aGraph + digraph.Vertex("EX", 551.9, deltaInherent=72.0)
aGraph + digraph.Vertex("PL", 66.77, deltaInherent=-4.22)
aGraph + digraph.Vertex("I", 993.5, deltaInherent=57.0)
aGraph + digraph.Vertex("FX", 71.41, deltaInherent=79.7)
aGraph + digraph.Vertex("M2", 3223.58, deltaInherent=-248)
aGraph + digraph.Vertex("RIR", 4.4, deltaInherent=0.139)

aGraph.add_edge("T", "G", "aa_lin", [1.29])
aGraph.add_edge("Y", "T", "aa_lin", [0.292])
aGraph.add_edge("Y", "YD", "aa_lin", [1])
aGraph.add_edge("T", "YD", "aa_lin", [-1])
aGraph.add_edge("YD", "C", "aa_lin", [0.937])
aGraph.add_edge("RIR", "C", "aa_lin", [-4.63])
aGraph.add_edge("Y", "IM", "aa_lin", [0.0475])
aGraph.add_edge("FX", "IM", "aa_lin", [5.76])
aGraph.add_edge("PL", "IM", "aa_lin", [-1.18])
aGraph.add_edge("C", "Y", "aa_lin", [1])
aGraph.add_edge("I", "Y", "aa_lin", [1])
aGraph.add_edge("G", "Y", "aa_lin", [1])
aGraph.add_edge("EX", "Y", "aa_lin", [1])
aGraph.add_edge("IM", "Y", "aa_lin", [-1])
aGraph.add_edge("FX", "EX", "aa_lin", [-2.61])
aGraph.add_edge("PL", "EX", "aa_lin", [-2.16])
aGraph.add_edge("M2", "PL", "aa_lin", [-0.008])
aGraph.add_edge("Y", "PL", "aa_lin", [0.0165])
aGraph.add_edge("RIR", "I", "aa_lin", [3.49])
aGraph.add_edge("Y", "I", "aa_lin", [0.153])
aGraph.add_edge("RIR", "FX", "aa_lin", [137])
aGraph.add_edge("RIR", "M2", "aa_lin", [-19.4])
aGraph.add_edge("Y", "M2", "aa_lin", [1.19])
aGraph.add_edge("PL", "M2", "aa_lin", [-54.8])
aGraph.add_edge("Y", "RIR", "aa_lin", [0.000679])
aGraph.add_edge("PL", "RIR", "aa_lin", [-0.0379])

initDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "IM": -6.2,
             "Y": 194.4, "EX": 43, "PL": 5.5, "I": -49.2, "FX": 2.94,
             "M2": 118.6, "NIR": -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 8, initDelta)
deltacalc.output_spreadsheet("test_13_data", output)
