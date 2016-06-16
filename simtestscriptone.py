import digraph
from deltafunctions import multicount_delta_application
from deltafunctions import write_output_to_spreadsheet

__author__ = "Ashleigh"

"""Placeholder Docstring."""


def main():
    miniMacro = digraph.DiGraph()
    miniMacro.add_node("T", 1712.9)
    miniMacro.add_node("G", 1920.2)
    miniMacro.add_node("C", 3825.6)
    miniMacro.add_node("Y", 5979.6)
    miniMacro.add_node("B", -78.969)
    miniMacro.add_node("X", 535.234)
    miniMacro.add_edge("T", "G", "proportional", ["coefficient"], [1])
    miniMacro.add_edge("G", "Y", "proportional", ["coefficient"], [1])
    miniMacro.add_edge("C", "Y", "proportional", ["coefficient"], [1])
    miniMacro.add_edge("B", "Y", "proportional", ["coefficient"], [1])
    miniMacro.add_edge("X", "B", "proportional", ["coefficient"], [1])
    miniMacro.add_edge("Y", "T", "proportional", ["coefficient"], [.29])
    miniMacro.add_edge("T", "C", "proportional", ["coefficient"], [-.64])
    miniMacro.add_edge("Y", "C", "proportional", ["coefficient"], [.64])
    miniMacro.add_edge("Y", "B", "proportional", ["coefficient"], [-.1])
    print(miniMacro)
    print("\n")

    initChanges = {"G": 114.4, "T": 50.4, "C": 134.6, "Y": 194.4, "B": 81.866,
                   "X": 43.109}
    simOutput = multicount_delta_application(miniMacro, 100, initChanges)
    write_output_to_spreadsheet("Sim_test_data_001", simOutput)


if __name__ == '__main__':
    main()