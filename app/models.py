from collections import namedtuple

# The dimensions used for the grid
dimension = namedtuple("dimension", ["width", "height"])
# The grids dimensions and living cells
Grid = namedtuple("grid", ["dim", "cells"])
# The status of the neighbouring cells. Alive or dead.
neighbours = namedtuple("neighbours", ["alive", "dead"])
# The x and y coordinates of the cell
cell = namedtuple("cell", ["x", "y"])
