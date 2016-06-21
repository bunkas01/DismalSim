from openpyxl import Workbook

import digraph

__author__ = "Ashleigh"

"""Assorted algorithms for calculating and applying changes to graphs.

The Delta Application Functions are what allow the directed graph
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
    - exocount_delta_application, applies changes over time, and
      supports applying user-defined changes at arbitrary system
      counts.
    - write_output_to_spreadsheet, takes a list-of-lists containing the
      output data from a delta application, and saves it externally as
      a spreadsheet.
"""


def multicount_delta_application(aGraph, maxCount, initDeltaDict):
    """Multiple-point count-mediated delta application algorithm.

    Given a graph, a maximum system count for which to run the
    algorithm, and a dictionary of initial delta values, the function
    modifies the graph in place, cyclically applying changes to any
    given Node based on the changes that the Node's parent Nodes
    experienced during the previous system count, modified by the
    transform functions assigned to the TransformEdges linking the
    Nodes. This cyclic delta application continues until the maximum
    count is reached. Additionally, the function maintains a log of the
    values of each Node in the graph after each system count,
    maintained in a list of values, and each Node has its own sublist
    of values. That list-of-lists is returned at the end of the
    function, to provide a more accessible log of all the changes that
    occurred during the algorithm's runtime.

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
        nodeData = [node.get_name(), node.get_data()]
        nodeDataList.append(nodeData)
    count = 0
    i = 0

    for key in initDeltaDict:
        if key in aGraph:
            targetNode = aGraph.get_node(key)
            initDelta = initDeltaDict[key]
            targetNode.add_to_delta_new(initDelta)
    aGraph.apply_all_new_deltas()

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


def exocount_delta_application(aGraph, maxCount, countFeedDict):
    """Delta application algorithm with support for additional changes.

    This delta application algorithm is similar to the algorithm in the
    multicount_delta_application function, but also includes support
    for making changes to any Node at any time while the algorithm is
    running. This can be used both to allow for the existence of non-
    constant orphan Nodes (Nodes with no parents, though children are
    allowed), and to model changes to the economy not accounted for
    directly within the model, such as changes in fiscal or economic
    policy related to political change. This is done through the use of
    a dict-in-dict structure as one of the function arguments, with the
    keys of the outer dictionary corresponding to system counts, and
    the keys of the inner dictionary corresponding to Nodes, with the
    value of the inner dictionary key-value pairs being the change to
    apply. It should be noted that the algorithm assumes that the
    arbitrary changes introduced by the dictionary occur alongside the
    'normal' changes produced through the edge transforms.

    The function arguments are as follows:
        - aGraph, the graph to calculate and apply changes to.
        - maxCount, the maximum number of cycles for which to run the
          algorithm.
        - countFeedDict, the dict-in-dict containing the relevant
          changes for a given system count.
        - The function does not support positional or keyword
          arguments.
    """

    nodeDataList = []
    for node in aGraph.get_all_nodes():
        nodeData = [node.get_name(), node.get_data()]
        nodeDataList.append(nodeData)
    count = 0

    while count <= maxCount:
        if count in countFeedDict:
            deltaDict = countFeedDict[count]
            for key in deltaDict:
                targetNode = aGraph.get_node(key)
                aDelta = deltaDict[key]
                targetNode.add_to_delta_new(aDelta)
        if count != 0:
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


def exonode_delta_application(aGraph, maxCount, countFeedDict):
    """Delta application function with exogenized variables.

    This delta application function is a minor modification of the
    exocount_delta_application function; the order in which external
    changes are applied and edge transforms are calculated is
    reversed, and the application of external changes is deliberately
    structured to override the changes produced by edge transforms on
    the relevant Nodes. This overriding of 'normal' changes is what
    allows the function to support Nodes being exogenized. A useful
    implication of this change is that it allows system counts within
    the algorithm to maintain parity with the real changes in time seen
    in the empirical data to which the sim is being compared.

    The function arguments are as follows:
        - aGraph, the graph to calculate and apply changes to.
        - maxCount, the maximum number of cycles for which to run the
          algorithm.
        - countFeedDict, the dict-in-dict containing the relevant
          changes for a given system count.
        - The function does not support positional or keyword
          arguments.
    """

    nodeDataList = []
    for node in aGraph.get_all_nodes():
        nodeData = [node.get_name(), node.get_data()]
        nodeDataList.append(nodeData)
    count = 0

    while count <= maxCount:
        if count != 0:
            for node in aGraph.get_all_nodes():
                for edge in node.get_all_edges():
                    edge.transform()
        if count in countFeedDict:
            deltaDict = countFeedDict[count]
            for key in deltaDict:
                targetNode = aGraph.get_node(key)
                aDelta = deltaDict[key]
                targetNode.set_delta_new(aDelta)
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
    dataList and writing them to the cells of the spreadsheet. Each
    sublist is maintained in a separate column of the spreadsheet.
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
    the screen; then the exocount_delta_application function is
    called on it, followed by being printed to the screen again.
    Additionally, the list of change data returned by the algorithm is
    printed to the screen. After this, a second, similar graph is
    instantiated and has Nodes and TransformEdges added. This graph
    has the multicount_delta_application algorithm used on it and is
    printed to the screen. Again, the list of change data returned by
    the algorithm is printed to the screen.

    The change data in the list are then written to a spreadsheet, to
    test the ability to save output. The spreadsheet is saved in .xlsx
    format.

    Finally, the first graph has its data reset to the starting values
    and is then used to test the exonode_delta_application function.
    """

    aGraph = digraph.DiGraph()
    aGraph.add_node("A", 30)
    aGraph.add_node("B", 30)
    aGraph.add_node("C", 30)
    aGraph.add_node("D", 30)
    aGraph.add_node("E", 30)
    aGraph.add_edge("A", "B", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("B", "A", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("B", "C", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("B", "D", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("C", "E", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("D", "E", "proportional", ["coefficient"], [0.75])
    aGraph.add_edge("E", "B", "proportional", ["coefficient"], [0.75])
    print(aGraph, "\n")
    aDict = {"A": 50, "B": 50}
    bDict = {"A": 30, "E": 30}
    cDict = {"B": 40}
    exoDict = {0: aDict, 2: bDict, 3: cDict}
    graphData = exocount_delta_application(aGraph, 4, exoDict)
    print(aGraph)
    for subList in graphData:
        print(subList)

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
    print(bGraph, "\n")
    allData = multicount_delta_application(bGraph, 20, {"A": 120, "E": 120})
    print(bGraph)
    for subList in allData:
        print(subList)
    # write_output_to_spreadsheet("test", allData)

    for node in aGraph.get_all_nodes():
        node.set_data(30)
    print(aGraph, "\n")
    dictA = {"A": 120, "B": 120, "E": 120}
    dictB = {"B": 120}
    dictC = {"B": 120}
    dictD = {"B": 120}
    dictE = {"B": 120}
    edict = {0: dictA, 1: dictB, 2: dictC, 3: dictD, 4: dictE}
    moreData = exonode_delta_application(aGraph, 4, edict)
    print(aGraph)
    for subList in moreData:
        print(subList)



if __name__ == '__main__':
    main()
