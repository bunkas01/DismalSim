from DismalSim.deltagraph import deltacalc
from DismalSim.deltagraph import digraph

"""Scripting the model from 1990-1999, without edges.

The script constructs a graph corresponding to the base economic model,
and runs it through the time period of 1990-1999. However, there are
almost no edges (only NIR->RIR and PL->RIR), and everything increases
by a constant 5% per year, except for the nominal interest rate, which
is a random value between 0 and 10; this is for the purpose of
hopefully proving the point that the regressions are at least somewhat
worthwhile.
"""

G = digraph.Vertex("G", 1920.2, deltaInherent=5, percentFlag=True)
T = digraph.Vertex("T", 1712.9, deltaInherent=5, percentFlag=True)
YD = digraph.Vertex("YD", 4266.7, deltaInherent=5, percentFlag=True)
C = digraph.Vertex("C", 3825.6, deltaInherent=5, percentFlag=True)
IM = digraph.Vertex("IM", 629.7, deltaInherent=5, percentFlag=True)
Y = digraph.Vertex("Y", 5979.6, deltaInherent=5, percentFlag=True)
EX = digraph.Vertex("EX", 551.9, deltaInherent=5, percentFlag=True)
PL = digraph.Vertex("PL", 66.77, deltaInherent=5, percentFlag=True)
I = digraph.Vertex("I", 993.5, deltaInherent=5, percentFlag=True)
FX = digraph.Vertex("FX", 71.41, deltaInherent=5, percentFlag=True)
M2 = digraph.Vertex("M2", 3223.58, deltaInherent=5, percentFlag=True)
NIR = digraph.Vertex("NIR", 8.1, randomValFlag=True, randomInfo=(0, 10))
RIR = digraph.Vertex("RIR", 4.4)
aGraph = digraph.DiGraph(G, T, YD, C, IM, Y, EX, PL, I, FX, M2, NIR, RIR)

aGraph.add_edge("NIR", "RIR", "aa_lin", [1])
aGraph.add_edge("PL", "RIR", "pa_lin", [-1])

initDelta = {"G": 114.4, "T": 50.4, "C": 134.6, "YD": 144, "IM": -6.2,
             "Y": 194.4, "EX": 43, "PL": 5.5, "I": -49.2, "FX": 2.94,
             "M2": 118.6, "NIR": -2.41, "RIR": -1.21}

output = deltacalc.gc_multicount_delta(aGraph, 8, initDelta)
deltacalc.output_spreadsheet("test_16_data", output)
