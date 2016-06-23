import digraph
from deltafunctions import exonode_delta_application
from deltafunctions import write_output_to_spreadsheet

__author__ = "Ashleigh"

"""Testing script for another improved version of the model.

The script generates a graph with all Nodes of the current model,
though some of the edges have yet to be added. The model covers the
90's specifically, and the initial changes provided for the delta
application algorithm are the changes in Node value between 1990 and
1991. The primary difference between this script, and the script in
simtest.py, is that this one makes use of the exonode_delta_application
function, which supports some variables being exogenized. The exogenous
variables in the case of this particular script are GDP (Y), Real
Interest Rate (R), and Trade-Weighted Exchange Rate (FX).
"""

exoMacro = digraph.DiGraph()
exoMacro.add_node("G", 1920.2)
exoMacro.add_node("T", 1712.9)
exoMacro.add_node("C", 3825.6)
exoMacro.add_node("Y", 5979.6)
exoMacro.add_node("M", 616.098)
exoMacro.add_node("X", 535.234)
exoMacro.add_node("FX", 91.22)
exoMacro.add_node("R", 2)
exoMacro.add_node("M2", 3223.583)
exoMacro.add_edge("G", "Y", "proportional", ["coefficient"], [1])
exoMacro.add_edge("T", "G", "proportional", ["coefficient"], [1])
exoMacro.add_edge("T", "C", "propcount", ["gradient", "constant"],
                  [-.0034, -.9637])
exoMacro.add_edge("C", "Y", "proportional", ["coefficient"], [1])
exoMacro.add_edge("Y", "T", "propcount", ["gradient", "constant"],
                  [.0023, .3091])
exoMacro.add_edge("Y", "C", "propcount", ["gradient", "constant"],
                  [.0034, .9637])
exoMacro.add_edge("Y", "M", "propcount", ["gradient", "constant"],
                  [.0044, .1613])
exoMacro.add_edge("Y", "M2", "linear", ["gradient", "constant"],
                  [.6169, 2.9469])
exoMacro.add_edge("M", "Y", "proportional", ["coefficient"], [-1])
exoMacro.add_edge("X", "Y", "proportional", ["coefficient"], [1])
exoMacro.add_edge("FX", "X", "linear", ["gradient", "constant"],
                  [-9.2416, 61.125])
exoMacro.add_edge("R", "M2", "proportional", ["coefficient"], [-500])
print(exoMacro, "\n")

dict0 = {"G": 114.4, "T": 50.4, "C": 134.6, "Y": 194.4, "M": -6.619,
         "X": 43.11, "FX": -1.54, "R": .59, "M2": 118.6}
dict1 = {"Y": 365.3, "R": -1.97, "FX": -1.89}
dict2 = {"Y": 339.4, "R": -.03, "FX": 1.34}
dict3 = {"Y": 430.1, "R": 1.19, "FX": -.017}
dict4 = {"Y": 355.3, "R": 1.82, "FX": -2.45}
dict5 = {"Y": 436.1, "R": -1.33, "FX": 2}
dict6 = {"Y": 508.3, "R": 1.76, "FX": 4.76}
dict7 = {"Y": 480.7, "R": -.01, "FX": 7.93}
dict8 = {"Y": 571.4, "R": -1.48, "FX": -.89}
dict9 = {"Y": 624.2, "R": .57, "FX": 3.85}
changeDict = {0: dict0, 1: dict1, 2: dict2, 3: dict3, 4: dict4, 5: dict5,
              6: dict6, 7: dict7, 8: dict8, 9: dict9}
simOutput = exonode_delta_application(exoMacro, 9, changeDict)
write_output_to_spreadsheet("sim_test_data_003", simOutput)
print(exoMacro)
