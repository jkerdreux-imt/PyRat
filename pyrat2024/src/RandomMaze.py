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
import scipy.sparse as sparse
import scipy.sparse.csgraph as csgraph
import numpy
import numpy.random as nprandom

# Internal imports
from pyrat2024.src.Maze import Maze

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
                   width:           int,
                   height:          int,
                   cell_percentage: float,
                   wall_percentage: float,
                   mud_percentage:  float,
                   mud_range:       Tuple[int, int],
                   random_seed:     int = None,
                 ) ->               Self:

        """
            This function is the constructor of the class.
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
        
        # Generate the maze
        self._create_maze(cell_percentage, wall_percentage, mud_percentage, mud_range, random_seed)

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self: Self,
                       cell_percentage: float,
                       wall_percentage: float,
                       mud_percentage:  float,
                       mud_range:       Tuple[int, int],
                       random_seed:     int = None,
                     ) ->               None:

        """
            This function creates a random maze using the parameters given at initialization.
            In:
                * self: Reference to the current object.
                * cell_percentage: Percentage of cells to be reachable.
                * wall_percentage: Percentage of walls to be present.
                * mud_percentage:  Percentage of mud to be present.
                * mud_range:       Range of the mud values.
                * random_seed:     Random seed for the maze generation, set to None for a random value.
            Out:
                * None.
        """

        # Set random seed
        if random_seed is not None:
            nprandom.seed(random_seed)

        # Initialize an empty maze, and add cells until it reaches the asked density
        maze_sparse = sparse.lil_matrix((self.width * self.height, self.width * self.height), dtype=int)
        cells = [(self.height // 2, self.width // 2)]
        while len(cells) / maze_sparse.shape[0] * 100 < cell_percentage:
            row, col = cells[nprandom.randint(len(cells))]
            neighbor_row, neighbor_col = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)][nprandom.randint(4)]
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
        nprandom.shuffle(walls)
        for i in range(int(numpy.ceil(wall_percentage / 100.0 * len(walls)))):
            maze_sparse[walls[i][0], walls[i][1]] = 0
            maze_sparse[walls[i][1], walls[i][0]] = 0

        # Add mud
        paths = sparse.triu(maze_sparse).nonzero()
        paths = [(paths[0][i], paths[1][i]) for i in range(paths[0].shape[0])]
        nprandom.shuffle(paths)
        for i in range(int(numpy.ceil(mud_percentage / 100.0 * len(paths)))):
            mud_weight = nprandom.choice(range(mud_range[0], mud_range[1] + 1))
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
