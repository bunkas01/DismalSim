from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import digraph

"""Scripting the model from 1990-1999, with regressions 1980-1989.

The script constructs a graph exogenizes G with a percent increase,
and runs it through the time period of 1990-1999; the regressions used
to calculate edge relationships were performed on the time period 1980-
1989. This graph does not include feedback from EX and IM to FX.
"""

aGraph = digraph.DiGraph()
aGraph + digraph.Vertex("G", 1920.2, deltaInherent=8.17, percentFlag=True)
aGraph + digraph.Vertex("T", 1712.9, deltaInherent=3.57)
aGraph + digraph.Vertex("YD", 4266.7)
aGraph + digraph.Vertex("C", 3825.6, deltaInherent=-3.61)
aGraph + digraph.Vertex("IM", 629.7, deltaInherent=4.62)
aGraph + digraph.Vertex("Y", 5979.6)
aGraph + digraph.Vertex("EX", 551.9, deltaInherent=27.0)
aGraph + digraph.Vertex("PL", 66.77, deltaInherent=-3.71)
aGraph + digraph.Vertex("I", 993.5, deltaInherent=-25.3)
aGraph + digraph.Vertex("FX", 71.41, deltaInherent=4.63)
aGraph + digraph.Vertex("M2", 3223.58, deltaInherent=-66.0)
aGraph + digraph.Vertex("NIR", 8.1, deltaInherent=-0.567)
aGraph + digraph.Vertex("RIR", 4.4)

aGraph.add_edge("G", "T", "aa_lin", [0.942])
aGraph.add_edge("Y", "YD", "aa_lin", [1])
aGraph.add_edge("T", "YD", "aa_lin", [-1])
aGraph.add_edge("YD", "C", "aa_lin", [0.989])
aGraph.add_edge("RIR", "C", "aa_lin", [-23.4])
aGraph.add_edge("Y", "IM", "aa_lin", [0.132])
aGraph.add_edge("FX", "IM", "aa_lin", [-1.20])
aGraph.add_edge("PL", "IM", "aa_lin", [-1.00])
aGraph.add_edge("C", "Y", "aa_lin", [1])
aGraph.add_edge("I", "Y", "aa_lin", [1])
aGraph.add_edge("G", "Y", "aa_lin", [1])
aGraph.add_edge("EX", "Y", "aa_lin", [1])
aGraph.add_edge("IM", "Y", "aa_lin", [-1])
aGraph.add_edge("FX", "EX", "aa_lin", [-7.98])
aGraph.add_edge("PL", "EX", "aa_lin", [12.3])
aGraph.add_edge("M2", "PL", "aa_lin", [0.0178])
aGraph.add_edge("Y", "PL", "aa_lin", [0.00794])
aGraph.add_edge("RIR", "I", "aa_lin", [-18.1])
aGraph.add_edge("Y", "I", "aa_lin", [0.247])
aGraph.add_edge("RIR", "FX", "aa_lin", [7.35])
aGraph.add_edge("NIR", "M2", "aa_lin", [-8.01])
aGraph.add_edge("Y", "M2", "aa_lin", [0.716])
aGraph.add_edge("PL", "M2", "aa_lin", [-27.7])
aGraph.add_edge("Y", "NIR", "aa_lin", [0.00181])
aGraph.add_edge("PL", "NIR", "aa_lin", [0.951])
aGraph.add_edge("NIR", "RIR", "aa_lin", [1])
aGraph.add_edge("PL", "RIR", "pa_lin", [-1])

initDelta = {"T": 50.4, "C": 134.6, "YD": 144, "IM": -6.2, "Y": 194.4,
             "EX": 43, "PL": 5.5, "I": -49.2, "FX": 2.94,  "M2": 118.6,
             "NIR": -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 8, initDelta)
deltacalc.output_spreadsheet("test_30_data", output)