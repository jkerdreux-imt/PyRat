#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    TODO
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
from Maze import Maze

#####################################################################################################################################################
################################################################## CLASS DEFINITION #################################################################
#####################################################################################################################################################

class RandomMaze (Maze):

    """

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
                * self: Reference to the current object.
        """

        # Inherit from parent class
        super(RandomMaze, self).__init__(width, height)
        
        # Generate the maze
        self._create_maze(cell_percentage, wall_percentage, mud_percentage, mud_range, random_seed)

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self: Self
                     ) ->    None:

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
        nprandom.seed(self.random_seed)

        # Initialize an empty maze, and add cells until it reaches the asked density
        maze_sparse = sparse.lil_matrix((self.maze_width * self.maze_height, self.maze_width * self.maze_height), dtype=int)
        cells = [(self.maze_height // 2, self.maze_width // 2)]
        while len(cells) / maze_sparse.shape[0] * 100 < self.cell_percentage:
            row, col = cells[nprandom.randint(len(cells))]
            neighbor_row, neighbor_col = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)][nprandom.randint(4)]
            if 0 <= neighbor_row < self.maze_height and 0 <= neighbor_col < self.maze_width:
                maze_sparse[self._rc_to_i(row, col, self.maze_width), self._rc_to_i(neighbor_row, neighbor_col, self.maze_width)] = 1
                maze_sparse[self._rc_to_i(neighbor_row, neighbor_col, self.maze_width), self._rc_to_i(row, col, self.maze_width)] = 1
                for next_neighbor_row, next_neighbor_col in [(neighbor_row - 1, neighbor_col), (neighbor_row + 1, neighbor_col), (neighbor_row, neighbor_col - 1), (neighbor_row, neighbor_col + 1)]:
                    if (next_neighbor_row, next_neighbor_col) in cells:
                        maze_sparse[self._rc_to_i(next_neighbor_row, next_neighbor_col, self.maze_width), self._rc_to_i(neighbor_row, neighbor_col, self.maze_width)] = 1
                        maze_sparse[self._rc_to_i(neighbor_row, neighbor_col, self.maze_width), self._rc_to_i(next_neighbor_row, next_neighbor_col, self.maze_width)] = 1
                if (neighbor_row, neighbor_col) not in cells:
                    cells.append((neighbor_row, neighbor_col))
        
        # Add walls
        maze_full = csgraph.minimum_spanning_tree(maze_sparse)
        maze_full += maze_full.transpose()
        walls = sparse.triu(maze_sparse - maze_full).nonzero()
        walls = [(walls[0][i], walls[1][i]) for i in range(walls[0].shape[0])]
        nprandom.shuffle(walls)
        for i in range(int(numpy.ceil(self.wall_percentage / 100.0 * len(walls)))):
            maze_sparse[walls[i][0], walls[i][1]] = 0
            maze_sparse[walls[i][1], walls[i][0]] = 0

        # Add mud
        paths = sparse.triu(maze_sparse).nonzero()
        paths = [(paths[0][i], paths[1][i]) for i in range(paths[0].shape[0])]
        nprandom.shuffle(paths)
        for i in range(int(numpy.ceil(self.mud_percentage / 100.0 * len(paths)))):
            mud_weight = nprandom.choice(range(self.mud_range[0], self.mud_range[1] + 1))
            maze_sparse[paths[i][0], paths[i][1]] = mud_weight
            maze_sparse[paths[i][1], paths[i][0]] = mud_weight

        # Save the maze in the appropriate format
        for vertex in range(maze_sparse.shape[0]):
            self.add_vertex(vertex)
            neighbors = maze_sparse[vertex].rows[0]
            if len(neighbors) > 0:
                self.add_vertex(vertex)
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor, maze_sparse[vertex, neighbor])

#####################################################################################################################################################
#####################################################################################################################################################
