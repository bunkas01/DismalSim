import graph

"""Algorithms for calculating changes in dynamic graphs.

Functions:
    - gen_data_log
    - log_data
    - manual_delta
    - gc_calc_delta
    - gp_calc_delta
    - def_calc_delta
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
        vData = [vertex.get_data()]
        vDataDict[vName] = vData
    return vDataDict



def log_data(aGraph, dataLog):
    """Writes data from a graph into a dict-of-lists.

    Function Arguments:
        - aGraph
        - dataLog
    """

    pass


def manual_delta(aGraph, deltaDict):
    """Applies predetermined deltas from a user-defined dictionary.

    Function Arguments:
        - aGraph
        - deltaDict
    """

    pass

def gc_calc_delta(aGraph):
    """Calculates and applies deltas using a greedy-child paradigm.

    Function Arguments:
        - aGraph
    """

    pass


def gp_calc_delta(aGraph):
    """Calculates and applies deltas using a generous-parent paradigm.

    Function Arguments:
        -aGraph
    """

    pass


def def_calc_delta(aGraph):
    """Calculates and applies definitional delta values.

    Function Arguments:
        - aGraph
    """

    pass


def main():
    aGraph = graph.Graph()


if __name__ == '__main__':
    main()
