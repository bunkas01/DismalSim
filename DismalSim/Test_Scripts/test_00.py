from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import digraph

aGraph = digraph.DiGraph()
aGraph + digraph.Vertex("G", 1920.2)
aGraph + digraph.Vertex("T", 1712.9)
aGraph + digraph.Vertex("C", 3825.6)
aGraph + digraph.Vertex("YD", 4266.7)
aGraph + digraph.Vertex("M", 629.7)
aGraph + digraph.Vertex("Y", 5979.6)
aGraph + digraph.Vertex("X", 551.9)
aGraph + digraph.Vertex("PL", 130.7)
aGraph + digraph.Vertex("I", 993.5)
aGraph + digraph.Vertex("FX", 91.22)
aGraph + digraph.Vertex("M2", 3223.58)
aGraph + digraph.Vertex("NIR", 8.1)
aGraph + digraph.Vertex("RIR", 2.7)
aGraph.add_edge("T", "G", "aa_lin", [0.898, 12.571])
aGraph.add_edge("G", "Y", "aa_lin", [1])
aGraph.add_edge("T", "YD", "aa_lin", [-1])
aGraph.add_edge("Y", "YD", "aa_lin", [1])
aGraph.add_edge("Y", "T", "aa_lin", [0.2786, 5.5414])
aGraph.add_edge("YD", "C", "aa_lin", [0.8631, 11.281])
aGraph.add_edge("C", "Y", "aa_lin", [1])
aGraph.add_edge("Y", "M", "aa_lin", [0.1045, 2.0599])
aGraph.add_edge("M", "Y", "aa_lin", [-1])
aGraph.add_edge("X", "Y", "aa_lin", [1])
aGraph.add_edge("PL", "M", "aa_lin", [2.7145, 9.8097])
aGraph.add_edge("Y", "PL", "aa_lin", [0.0159, 0.6069])
aGraph.add_edge("PL", "M2", "aa_lin", [16.766, 42.133])
aGraph.add_edge("M2", "PL", "aa_lin", [0.0211, 1.3332])
aGraph.add_edge("Y", "M2", "aa_lin", [0.4264, 24.288])
aGraph.add_edge("I", "Y", "aa_lin", [1])
aGraph.add_edge("NIR", "RIR", "aa_lin", [1])
aGraph.add_edge("FX", "X", "pp_lin", [-1.0399, 9.6864])
aGraph.add_edge("NIR", "M2", "ap_lin", [-0.5897, 8.3919])
aGraph.add_edge("NIR", "I", "ap_lin", [-2.4148, 9.5452])
aGraph.add_edge("RIR", "FX", "ap_lin", [1.1715, -0.3175])
aGraph.add_edge("PL", "RIR", "pa_lin", [-1])
aGraph.add_edge("Y", "NIR", "pa_lin", [0.2122, -1.5666])

iDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "M": -6.2, "Y": 194.4,
          "X": 43, "PL": 5.5, "I": -49.2, "FX": -1.54, "M2": 118.6, "NIR":
          -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 10, iDelta)

deltacalc.output_spreadsheet("test_00_data", output)