#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file is part of the PyRat library.
    It is meant to be used as a library, and not to be executed directly.
    Please import necessary elements using the following syntax:
        from pyrat import <element_name>
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import scipy.sparse as sparse
import scipy.sparse.csgraph as csgraph
import random
import math

# PyRat imports
from pyrat.src.RandomMaze import RandomMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class AdditiveRandomMaze (RandomMaze):

    """
        This class inherits from the RandomMaze class.
        Therefore, it has the attributes and methods defined in the RandomMaze class in addition to the ones defined below.

        An additive random maze is a random maze where the cells are added one by one.
        The maze is created by adding cells to an empty maze, and connecting them to the existing cells.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:     Self,
                   *args:    Any,
                   **kwargs: Any
                 ) ->        Self:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * args:   Arguments to pass to the parent constructor.
                * kwargs: Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self: Self,
                     ) ->    None:
        
        """
            This method redefines the abstract method of the parent class.
            It creates a random maze using the parameters given at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Initialize an empty maze, and add cells until it reaches the asked density
        maze_sparse = sparse.lil_matrix((self.width * self.height, self.width * self.height), dtype=int)
        cells = [(self.height // 2, self.width // 2)]
        while len(cells) / maze_sparse.shape[0] * 100 < self._cell_percentage:
            row, col = self._rng.choice(cells)
            neighbor_row, neighbor_col = self._rng.choice([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
            if 0 <= neighbor_row < self.height and 0 <= neighbor_col < self.width:
                maze_sparse[self.rc_to_i(row, col), self.rc_to_i(neighbor_row, neighbor_col)] = 1
                maze_sparse[self.rc_to_i(neighbor_row, neighbor_col), self.rc_to_i(row, col)] = 1
                for next_neighbor_row, next_neighbor_col in [(neighbor_row - 1, neighbor_col), (neighbor_row + 1, neighbor_col), (neighbor_row, neighbor_col - 1), (neighbor_row, neighbor_col + 1)]:
                    if (next_neighbor_row, next_neighbor_col) in cells:
                        maze_sparse[self.rc_to_i(next_neighbor_row, next_neighbor_col), self.rc_to_i(neighbor_row, neighbor_col)] = 1
                        maze_sparse[self.rc_to_i(neighbor_row, neighbor_col), self.rc_to_i(next_neighbor_row, next_neighbor_col)] = 1
                if (neighbor_row, neighbor_col) not in cells:
                    cells.append((neighbor_row, neighbor_col))
        
        # Add walls
        maze_full = csgraph.minimum_spanning_tree(maze_sparse)
        maze_full += maze_full.transpose()
        walls = sparse.triu(maze_sparse - maze_full).nonzero()
        walls = [(walls[0][i], walls[1][i]) for i in range(walls[0].shape[0])]
        self._rng.shuffle(walls)
        for i in range(math.ceil(self._wall_percentage / 100.0 * len(walls))):
            maze_sparse[walls[i][0], walls[i][1]] = 0
            maze_sparse[walls[i][1], walls[i][0]] = 0

        # Add mud
        paths = sparse.triu(maze_sparse).nonzero()
        paths = [(paths[0][i], paths[1][i]) for i in range(paths[0].shape[0])]
        self._rng.shuffle(paths)
        for i in range(math.ceil(self._mud_percentage / 100.0 * len(paths))):
            mud_weight = self._rng.choice(range(self._mud_range[0], self._mud_range[1] + 1))
            maze_sparse[paths[i][0], paths[i][1]] = mud_weight
            maze_sparse[paths[i][1], paths[i][0]] = mud_weight
        
        # Set vertices
        for vertex in range(maze_sparse.shape[0]):
            neighbors = maze_sparse[vertex].rows[0]
            if len(neighbors) > 0:
                self.add_vertex(vertex)

        # Set edges
        for vertex in range(maze_sparse.shape[0]):
            neighbors = maze_sparse[vertex].rows[0]
            for neighbor in neighbors:
                self.add_edge(vertex, neighbor, maze_sparse[vertex, neighbor])

#####################################################################################################################################################
#####################################################################################################################################################