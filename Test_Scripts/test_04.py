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
aGraph.add_edge("T", "G", "abs_proportional", [0.898])
aGraph.add_edge("G", "Y", "abs_proportional", [1])
aGraph.add_edge("T", "YD", "abs_proportional", [-1])
aGraph.add_edge("Y", "YD", "abs_proportional", [1])
aGraph.add_edge("Y", "T", "abs_proportional", [0.2786])
aGraph.add_edge("YD", "C", "abs_proportional", [0.8631])
aGraph.add_edge("C", "Y", "abs_proportional", [1])
aGraph.add_edge("Y", "M", "abs_proportional", [0.1045])
aGraph.add_edge("M", "Y", "abs_proportional", [-1])
aGraph.add_edge("X", "Y", "abs_proportional", [1])
aGraph.add_edge("Y", "PL", "abs_proportional", [0.0159])
aGraph.add_edge("Y", "M2", "abs_proportional", [0.4264])
aGraph.add_edge("I", "Y", "abs_proportional", [1])
aGraph.add_edge("NIR", "RIR", "abs_proportional", [1])
aGraph.add_edge("FX", "X", "per_proportional", [-1.0399])
aGraph.add_edge("NIR", "I", "green", [-9.4487, 32.881])
aGraph.add_edge("RIR", "FX", "green", [1.1934, -0.4887])
aGraph.add_edge("PL", "RIR", "red", [-1, 0])
aGraph.add_edge("Y", "NIR", "red", [0.2122, -1.5666])

iDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "M": -6.2, "Y": 194.4,
          "X": 43, "PL": 5.5, "I": -49.2, "FX": -1.54, "M2": 118.6, "NIR":
          -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 10, iDelta)

deltacalc.output_spreadsheet("test_04_data", output)