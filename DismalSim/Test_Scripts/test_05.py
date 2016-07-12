from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import graph

"""Multiple Linear Regressions 1955-1989, T Causes G.

A test script using the transmittances gained from multiple linear
regressions on the period 1955-1989, assuming that taxes determine
government spending.
"""

aGraph = graph.Graph()
aGraph + graph.Vertex("G", 1920.2, deltaInherent=3.59)
aGraph + graph.Vertex("T", 1712.9, deltaInherent=1.11)
aGraph + graph.Vertex("YD", 4266.7)
aGraph + graph.Vertex("C", 3825.6, deltaInherent=-1.37)
aGraph + graph.Vertex("IM", 629.7, deltaInherent=36.14)
aGraph + graph.Vertex("Y", 5979.6)
aGraph + graph.Vertex("EX", 551.9, deltaInherent=62.03)
aGraph + graph.Vertex("PL", 66.77, deltaInherent=0.54)
aGraph + graph.Vertex('I', 993.5, deltaInherent=0.77)
aGraph + graph.Vertex("FX", 71.41, deltaInherent=3)
aGraph + graph.Vertex("M2", 3223.58, deltaInherent=10.65)
aGraph + graph.Vertex("NIR", 8.1, deltaInherent=0.38)
aGraph + graph.Vertex("RIR", 4.4)
aGraph.add_edge("T", "G", "aa_lin", [1.15])
aGraph.add_edge("Y", "T", "aa_lin", [0.31])
aGraph.add_edge("G", "Y", "aa_lin", [1])
aGraph.add_edge("T", "YD", "aa_lin", [-1])
aGraph.add_edge("Y", "YD", "aa_lin", [1])
aGraph.add_edge("YD", "C", "aa_lin", [0.98])
aGraph.add_edge("C", "Y", "aa_lin", [1])
aGraph.add_edge("IM", "Y", "aa_lin", [-1])
aGraph.add_edge("Y", "IM", "aa_lin", [0.08])
aGraph.add_edge("EX", "Y", "aa_lin", [1])
aGraph.add_edge("PL", "IM", "aa_lin", [-9.14])
aGraph.add_edge("Y", "PL", "aa_lin", [0.03])
aGraph.add_edge("PL", "EX", "aa_lin", [-12.05])
aGraph.add_edge("Y", "I", "aa_lin", [0.11])
aGraph.add_edge("I", "Y", "aa_lin", [1])
aGraph.add_edge("IM", "FX", "aa_lin", [0.03])
aGraph.add_edge("FX", "IM", "aa_lin", [-0.6])
aGraph.add_edge("FX", "EX", "aa_lin", [-4.11])
aGraph.add_edge("EX", "FX", "aa_lin", [-0.09])
aGraph.add_edge("PL", "I", "aa_lin", [8.6])
aGraph.add_edge("Y", "M2", "aa_lin", [0.43])
aGraph.add_edge("M2", "PL", "aa_lin", [-0.03])
aGraph.add_edge("PL", "M2", "aa_lin", [11.4])
aGraph.add_edge("NIR", "M2", "aa_lin", [-14.97])
aGraph.add_edge("PL", "NIR", "aa_lin", [0.37])
aGraph.add_edge("PL", "RIR", "pa_lin", [-1])
aGraph.add_edge("NIR", "RIR", "aa_lin", [1])
aGraph.add_edge("RIR", "I", "aa_lin", [-4.92])
aGraph.add_edge("RIR", "FX", "aa_lin", [0.79])
aGraph.add_edge("RIR", "C", "aa_lin", [-6.22])

iDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "M": -6.2, "Y": 194.4,
         "X": 43, "PL": 5.5, "I": -49.2, "FX": -1.54, "M2": 118.6, "NIR":
         -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 10, iDelta)

deltacalc.output_spreadsheet("test_05_data", output)