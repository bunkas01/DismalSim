import digraph
from deltafunctions import multicount_delta_application
from deltafunctions import write_output_to_spreadsheet

__author__ = "Ashleigh"

"""Testing script for an improved version of the model."""

mostlyMacro = digraph.DiGraph()
mostlyMacro.add_node("G", 1920.2)
mostlyMacro.add_node("T", 1712.9)
mostlyMacro.add_node("C", 3825.6)
mostlyMacro.add_node("Y", 5979.6)
mostlyMacro.add_node("M", 616.098)
mostlyMacro.add_node("X", 535.234)
mostlyMacro.add_node("FX", 91.22)
mostlyMacro.add_node("R", 2)
mostlyMacro.add_node("M2", 3223.583)
mostlyMacro.add_edge("G", "Y", "proportional", ["coefficient"], [1])
mostlyMacro.add_edge("T", "G", "proportional", ["coefficient"], [1])
mostlyMacro.add_edge("T", "C", "propcount", ["gradient", "constant"],
                     [-.0034, -.9637])
mostlyMacro.add_edge("C", "Y", "proportional", ["coefficient"], [1])
mostlyMacro.add_edge("Y", "T", "propcount", ["gradient", "constant"],
                     [.0023, .3091])
mostlyMacro.add_edge("Y", "C", "propcount", ["gradient", "constant"],
                     [.0034, .9637])
mostlyMacro.add_edge("Y", "M", "propcount", ["gradient", "constant"],
                     [.0044, .1613])
mostlyMacro.add_edge("Y", "M2", "linear", ["gradient", "constant"],
                     [.6169, 2.9469])
mostlyMacro.add_edge("M", "Y", "proportional", ["coefficient"], [-1])
mostlyMacro.add_edge("X", "Y", "proportional", ["coefficient"], [1])
mostlyMacro.add_edge("FX", "X", "linear", ["gradient", "constant"],
                     [-9.2416, 61.125])
mostlyMacro.add_edge("R", "M2", "proportional", ["coefficient"], [-500])
print(mostlyMacro, "\n")

initChanges = {"G": 114.4, "T": 50.4, "C": 134.6, "Y": 194.4, "M": -6.619,
               "X": 43.11, "FX": -1.54, "R": 2.59, "M2": 118.6}
simOutput = multicount_delta_application(mostlyMacro, 9, initChanges)
write_output_to_spreadsheet("sim_test_data_002", simOutput)
print(mostlyMacro)
