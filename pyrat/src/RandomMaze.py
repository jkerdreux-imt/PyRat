#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a random maze.
    It is meant to be used as a library, and not to be executed directly.
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
import sys
import random
import math

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class RandomMaze (Maze):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        A random maze is a maze that is created randomly.
        You can specify the size of the maze, the density of cells, walls, and mud, and the range of the mud values.
        You can also specify a random seed to reproduce the same maze later.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:            Self,
                   width:           Integral,
                   height:          Integral,
                   cell_percentage: Number,
                   wall_percentage: Number,
                   mud_percentage:  Number,
                   mud_range:       Tuple[Integral, Integral],
                   random_seed:     Optional[Integral] = None
                 ) ->               Self:

        """
            This function is the constructor of the class.
            We do not duplicate asserts already made in the parent method.
            In:
                * self:            Reference to the current object.
                * width:           Width of the maze.
                * height:          Height of the maze.
                * cell_percentage: Percentage of cells to be reachable.
                * wall_percentage: Percentage of walls to be present.
                * mud_percentage:  Percentage of mud to be present.
                * mud_range:       Range of the mud values.
                * random_seed:     Random seed for the maze generation, set to None for a random value.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(width, height)
        
        # Debug
        assert isinstance(cell_percentage, Number) # Type check for cell_percentage
        assert isinstance(wall_percentage, Number) # Type check for wall_percentage
        assert isinstance(mud_percentage, Number) # Type check for mud_percentage
        assert isinstance(mud_range, (tuple, list)) # Type check for mud_range
        assert isinstance(random_seed, (Integral, type(None))) # Type check for random_seed
        assert random_seed is None or 0 <= random_seed < sys.maxsize # random_seed is a valid seed
        assert len(mud_range) == 2 # Mud range is an interval of 2 elements
        assert isinstance(mud_range[0], Integral) # Type check for mud_range[0]
        assert isinstance(mud_range[1], Integral) # Type check for mud_range[1]
        assert 0.0 <= cell_percentage <= 100.0 # cell_percentage is a percentage
        assert 0.0 <= wall_percentage <= 100.0 # wall_percentage is a percentage
        assert 0.0 <= mud_percentage <= 100.0 # mud_percentage is a percentage
        assert 1 < mud_range[0] <= mud_range[1] # mud_range is a valid interval with minimum value 1

        # Private attributes
        self.__cell_percentage = cell_percentage
        self.__wall_percentage = wall_percentage
        self.__mud_percentage = mud_percentage
        self.__mud_range = mud_range
        self.__random_seed = random_seed

        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
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

        # Initialize the random generator
        rng = random.Random(self.__random_seed)

        # Initialize an empty maze, and add cells until it reaches the asked density
        maze_sparse = sparse.lil_matrix((self.width * self.height, self.width * self.height), dtype=int)
        cells = [(self.height // 2, self.width // 2)]
        while len(cells) / maze_sparse.shape[0] * 100 < self.__cell_percentage:
            row, col = rng.choice(cells)
            neighbor_row, neighbor_col = rng.choice([(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)])
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
        rng.shuffle(walls)
        for i in range(math.ceil(self.__wall_percentage / 100.0 * len(walls))):
            maze_sparse[walls[i][0], walls[i][1]] = 0
            maze_sparse[walls[i][1], walls[i][0]] = 0

        # Add mud
        paths = sparse.triu(maze_sparse).nonzero()
        paths = [(paths[0][i], paths[1][i]) for i in range(paths[0].shape[0])]
        rng.shuffle(paths)
        for i in range(math.ceil(self.__mud_percentage / 100.0 * len(paths))):
            mud_weight = rng.choice(range(self.__mud_range[0], self.__mud_range[1] + 1))
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