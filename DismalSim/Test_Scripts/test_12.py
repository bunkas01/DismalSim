from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import digraph

"""Scripting the model from 1990-1999, with concurrent regressions.

The script constructs a graph corresponding to the base economic model,
and runs it through the time period of 1990-1999; the regressions used
to calculate edge relationships were performed on the same time period,
in order to test the fundamental robustness of the model. In this test
script, the initial delta is set equal to the inherent delta rather
than being the actual change from 1990 to 1991.
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
aGraph + digraph.Vertex("FX", 71.41, deltaInherent=-11.3)
aGraph + digraph.Vertex("M2", 3223.58, deltaInherent=-249)
aGraph + digraph.Vertex("NIR", 8.1, deltaInherent=-0.467)
aGraph + digraph.Vertex("RIR", 4.4)

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
aGraph.add_edge("M2", "PL", "aa_lin", [-0.00823])
aGraph.add_edge("Y", "PL", "aa_lin", [0.0165])
aGraph.add_edge("RIR", "I", "aa_lin", [3.49])
aGraph.add_edge("Y", "I", "aa_lin", [0.153])
aGraph.add_edge("RIR", "FX", "aa_lin", [-13.4])
aGraph.add_edge("EX", "FX", "aa_lin", [0.396])
aGraph.add_edge("IM", "FX", "aa_lin", [0.703])
aGraph.add_edge("NIR", "M2", "aa_lin", [-14.4])
aGraph.add_edge("Y", "M2", "aa_lin", [1.17])
aGraph.add_edge("PL", "M2", "aa_lin", [-52.5])
aGraph.add_edge("Y", "NIR", "aa_lin", [0.00195])
aGraph.add_edge("PL", "NIR", "aa_lin", [-0.104])
aGraph.add_edge("NIR", "RIR", "aa_lin", [1])
aGraph.add_edge("PL", "RIR", "pa_lin", [-1])

initDelta = {"G": 73.5, "T": 30.9, "C": 40.1, "IM": 30.3,
             "EX": 72, "PL": 4.22, "I": 57, "FX": 11.3,
             "M2": 249, "NIR": 0.467}

output = deltacalc.gc_multicount_delta(aGraph, 8, initDelta)
deltacalc.output_spreadsheet("test_12_data", output)