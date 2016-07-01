import graph
import deltacalc

aGraph = graph.Graph()
aGraph.add_vertex("G", 1920.2)
aGraph.add_vertex("T", 1712.9)
aGraph.add_vertex("C", 3825.6)
aGraph.add_vertex("YD", 4266.7)
aGraph.add_vertex("M", 629.7)
aGraph.add_vertex("Y", 5979.6)
aGraph.add_vertex("X", 551.9)
aGraph.add_vertex("PL", 130.7)
aGraph.add_vertex("I", 993.5)
aGraph.add_vertex("FX", 91.22)
aGraph.add_vertex("M2", 3223.58)
aGraph.add_vertex("NIR", 8.1)
aGraph.add_vertex("RIR", 2.7)
aGraph.add_edge("T", "G", "abs_linear", [0.898, 12.571])
aGraph.add_edge("G", "Y", "def_proportional", [1])
aGraph.add_edge("T", "YD", "def_proportional", [-1])
aGraph.add_edge("Y", "YD", "def_proportional", [1])
aGraph.add_edge("Y", "T", "abs_linear", [0.2786, 5.5414])
aGraph.add_edge("YD", "C", "abs_linear", [0.8631, 11.281])
aGraph.add_edge("C", "Y", "def_proportional", [1])
aGraph.add_edge("Y", "M", "abs_linear", [0.1045, 2.0599])
aGraph.add_edge("M", "Y", "def_proportional", [-1])
aGraph.add_edge("X", "Y", "def_proportional", [1])
aGraph.add_edge("PL", "M", "abs_linear", [2.7145, 9.8097])
aGraph.add_edge("Y", "PL", "abs_linear", [0.0159, 0.6069])
aGraph.add_edge("PL", "M2", "abs_linear", [16.766, 42.133])
aGraph.add_edge("M2", "PL", "abs_linear", [0.0211, 1.3332])
aGraph.add_edge("Y", "M2", "abs_linear", [0.4264, 24.288])
aGraph.add_edge("I", "Y", "def_proportional", [1])
aGraph.add_edge("NIR", "RIR", "def_proportional", [1])
aGraph.add_edge("FX", "X", "per_linear", [-1.0399, 9.6864])
aGraph.add_edge("NIR", "M2", "green", [-9.5003, 96.288])
aGraph.add_edge("NIR", "I", "green", [-9.4487, 32.881])
aGraph.add_edge("RIR", "FX", "green", [1.1934, -0.4887])
aGraph.add_edge("PL", "RIR", "def_red", [-1])
aGraph.add_edge("Y", "NIR", "red", [0.2122, -1.5666])

iDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "M": -6.2, "Y": 194.4,
          "X": 43, "PL": 5.5, "I": -49.2, "FX": -1.54, "M2": 118.6, "NIR":
          -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 10, iDelta)

deltacalc.output_spreadsheet("test_00_data", output)