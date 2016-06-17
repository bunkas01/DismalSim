from openpyxl import Workbook

import digraph

__author__ = "Ashleigh"

"""Assorted algorithms for calculating and applying changes to graphs.

The Delta Application Functions are what allows [allow] the directed graph
implementation used in this project to be used as part of an economic
simulation, as they govern how changes spread between Nodes that
represent components of the macroeconomy. There is also another
function intended to enable the output data from the delta application
algorithms to be written to Excel spreadsheets, for ease of use.

Currently, only a single delta application function has been
implemented, though there will be more to come, some of which may just
be modifications or complications of the multicount_delta_application
function initially implemented.

Functions:
    - multicount_delta_application, applies changes from multiple
      sources over time.
    - write_output_to_spreadsheet, takes a list-of-lists containing the
      output data from a delta application, and saves it externally as
      a spreadsheet.
"""


def multicount_delta_application(aGraph, maxCount, initDeltaDict):
    """Multiple-point count-mediated delta application algorithm.

    Given a graph, a maximum system count to run the algorithm for [for which to run the algorithm], and
    a dictionary of initial delta values, the function modifies the
    graph in place, cyclically applying changes to any given Node based
    on the changes that the Node's parent Nodes experienced during the
    previous system count, modified by the transform functions assigned
    to the TransformEdges linking the Nodes. This cyclic delta
    application continues until the maximum count is reached.
    Additionally, the function maintains a log of the values of each
    Node in the graph after each system count, maintained in a list of
    values, and each Node has its own sublist of values. That
    list-of-lists is returned at the end of the function, to provide
    a more accessible log of all the changes that occurred during the
    algorithms [algorithm's] runtime.

    The function arguments are as follows:
        - aGraph, the graph to calculate and apply changes to.
        - maxCount, the maximum number of delta calculation-application
          cycles to complete.
        - initDeltaDict, a dictionary of the initial changes to apply
          to start the simulation, with the names of the Nodes to which
          changes should be applied serving as keys.
        - The function does not support positional or keyword
          arguments.
    """

    nodeDataList = []
    for node in aGraph.get_all_nodes():
        nodeData = []
        nodeData.append(node.get_name())
        nodeData.append(node.get_data())
        nodeDataList.append(nodeData)
    count = 0
    for key in initDeltaDict:
        if key in aGraph:
            targetNode = aGraph.get_node(key)
            initDelta = initDeltaDict[key]
            targetNode.set_delta_new(initDelta)
    aGraph.apply_all_new_deltas()
    i = 0
    for node in aGraph.get_all_nodes():
        nodeDataList[i].append(node.get_data())
        i += 1
    count += 1
    while count <= maxCount:
        for node in aGraph.get_all_nodes():
            for edge in node.get_all_edges():
                edge.transform()
        aGraph.apply_all_new_deltas()
        i = 0
        for node in aGraph.get_all_nodes():
            nodeDataList[i].append(node.get_data())
            i += 1
        count += 1
    return nodeDataList


def write_output_to_spreadsheet(filename, dataList):
    """Writes the data contained in a list to an Excel Spreadsheet.

    This function uses the openpyxl package to create a spreadsheet,
    followed by iterating over the contents of the sublists in the
    dataList, [delete comma] and writing them to the cells of the spreadsheet. Each
    sublist is maintained in a separate column of the spreadhseet.
    After the spreadsheet is fully created, it is saved with the given
    filename as a .xlsx file.

    The function arguments are as follows:
        - filename, the name of the final file after the spreadsheet
          has been created.
        - dataList, the list-of-lists containing the assorted output
          data from a simulation run.
        - The function does not support positional or keyword
          arguments.
    """

    filename += ".xlsx"
    dataBook = Workbook()
    dataSheet = dataBook.active

    colCount = 1
    rowCount = 1
    for sublist in dataList:
        for item in sublist:
            cell = dataSheet.cell(column=colCount, row=rowCount)
            cell.value = item
            rowCount += 1
        rowCount = 1
        colCount += 1
    dataBook.save(filename)


def main():
    """Testing Script for delta application functions.

    A graph is instantiated, and five Nodes (A, B, C, D, E) are added
    to it. Assorted TransformEdges are created, all with the same
    transform type and transform parameters. This graph is printed to
    the screen, [replace comma with semicolon] then the multicount_delta_application function is
    called on it, followed by being printed to the screen again. After
    this, a second, similar graph is instantiated, [delete comma] and has Nodes and
    TransformEdges added. This graph also has the
    multicount_delta_application algorithm used on it, [delete comma] and is printed
    to the screen. Additionally, the list of change data returned by
    the algorithm is also [the combination of "additionally" and "also" is redundant] printed to the screen.

    The change data in the list is [are] then written to a spreadsheet, to
    test the ability to save output.
    """

    aGraph = digraph.DiGraph()
    aGraph.add_node("A", 30)
    aGraph.add_node("B", 30)
    aGraph.add_node("C", 30)
    aGraph.add_node("D", 30)
    aGraph.add_node("E", 30)
    aGraph.add_edge("A", "B", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "C", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("B", "D", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("C", "E", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.25])
    aGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.25])
    print(aGraph)
    print("\n")

    multicount_delta_application(aGraph, 4, {"A": 120, "E": 120})
    print(aGraph)

    bGraph = digraph.DiGraph()
    bGraph.add_node("A", 30)
    bGraph.add_node("B", 30)
    bGraph.add_node("C", 30)
    bGraph.add_node("D", 30)
    bGraph.add_node("E", 30)
    bGraph.add_edge("A", "B", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "C", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("B", "D", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("C", "E", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.5])
    bGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.5])
    print(bGraph)
    print("\n")

    allData = multicount_delta_application(bGraph, 20, {"A": 120, "E": 120})
    print(bGraph)
    for subList in allData:
        print(subList)
    write_output_to_spreadsheet("test", allData)


if __name__ == '__main__':
    main()
