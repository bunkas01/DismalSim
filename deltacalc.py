import graph
from openpyxl import Workbook

"""Algorithms for calculating changes in dynamic graphs.

Functions:
    - gen_data_log
    - log_data
    - manual_delta
    - gc_calc_delta
    - gp_calc_delta
    - multicount_delta
    - exovert_delta
"""


def gen_data_log(aGraph):
    """Creates a dict-of-lists to record data from delta calculations.

    The function creates a new dictionary, in which to store the 'data'
    attributes of vertices at each step in an iterative simulation. The
    dictionary entries are indexed by Vertex, and the associated values
    are lists of the vertices 'data' attribute, intended to be written
    to after each cycle of the simulation.

    Function Arguments:
        - aGraph
    """

    vDataDict = {}
    for vertex in aGraph:
        vName = vertex.get_name()
        vData = [vName]
        vDataDict[vName] = vData
    return vDataDict



def log_data(aGraph, dataLog):
    """Writes data from a graph into a dict-of-lists.

    Function Arguments:
        - aGraph
        - dataLog
    """

    for key in dataLog:
        dataList = dataLog[key]
        vertex = aGraph.get_vertex(key)
        vData = vertex.get_data()
        dataList.append(vData)


def manual_delta(aGraph, deltaDict):
    """Applies predetermined deltas from a user-defined dictionary.

    Function Arguments:
        - aGraph
        - deltaDict
    """

    for key in deltaDict:
        if key in aGraph:
            vTarget = aGraph.get_vertex(key)
            delta = deltaDict[key]
            vTarget.set_delta_float(delta)

def gc_calc_delta(aGraph):
    """Calculates delta values using a greedy-child paradigm.

    Function Arguments:
        - aGraph
    """

    for vertex in aGraph:
        vertex.gc_transform()


def gp_calc_delta(aGraph):
    """Calculates delta values using a generous-parent paradigm.

    Function Arguments:
        -aGraph
    """

    return NotImplemented


def gc_multicount_delta(aGraph, maxCount, initDeltaDict):
    dataLog = gen_data_log(aGraph)
    for count in range(maxCount + 1):
        if count == 0:
            manual_delta(aGraph, initDeltaDict)
        else:
            gc_calc_delta(aGraph)
            aGraph.apply_floating_deltas()
        log_data(aGraph, dataLog)
    return dataLog


def gc_exovert_delta(aGraph, maxCount, exoDeltaDict):
    return NotImplemented


def output_spreadsheet(filename, dataDict):
    filename += ".xlsx"
    dataBook = Workbook()
    dataSheet = dataBook.active

    colCount = 1
    rowCount = 1
    for sublist in dataDict.values():
        for item in sublist:
            cell = dataSheet.cell(column=colCount, row=rowCount)
            cell.value = item
            rowCount += 1
        rowCount = 1
        colCount += 1
    dataBook.save(filename)


def main():
    aGraph = graph.Graph()
    aGraph.add_vertex("A", 10)
    aGraph.add_vertex("B", 10)
    aGraph.add_vertex("C", 10)
    aGraph.add_vertex("D", 10)
    aGraph.add_edge("A", "B", "aa_lin", [2, 2])
    aGraph.add_edge("A", "C", "pp_lin", [10, 15])
    aGraph.add_edge("B", "D", "aa_lin", [1])
    aGraph.add_edge("C", "D", "aa_lin", [1])
    aGraph.add_edge("D", "A", "aa_lin", [2])
    iDelta = {"A": 20}
    print(gc_multicount_delta(aGraph, 5, iDelta))


if __name__ == '__main__':
    main()
