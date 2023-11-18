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
import numpy
import ast

# Internal imports
from Maze import Maze

#####################################################################################################################################################
################################################################## CLASS DEFINITION #################################################################
#####################################################################################################################################################

class FixedMaze (Maze):

    """

    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:            Self,
                   description:     Union[None, str, Maze, Dict[int, Dict[int, int]], numpy.ndarray]
                 ) ->               Self:

        """
            This function is the constructor of the class.
            In:
                * self:        Reference to the current object.
                * description: Fixed maze in any handled format (an existing maze, an adjacency dictionary, a numpy matrix, or a string of one of these last 2 representations).
            Out:
                * self: Reference to the current object.
        """

        # Inherit from parent class
        super(FixedMaze, self).__init__()
        
        # Generate the maze
        self._create_maze(description)

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self: Self
                     ) ->    None:

        """
            This function creates a maze from the description provided at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Transform in a structure if a string
        fixed_maze = ast.literal_eval(self.fixed_maze) if isinstance(self.fixed_maze, str) else self.fixed_maze
        if isinstance(self.fixed_maze, list):
            fixed_maze = numpy.array(fixed_maze)
        
        # If given as a matrix
        if isinstance(fixed_maze, numpy.ndarray):
            maze = {}
            maze_width = 1
            for vertex in range(fixed_maze.shape[0]):
                for neighbor in fixed_maze[vertex].nonzero()[0]:
                    if neighbor - vertex > 1:
                        maze_width = neighbor - vertex
                    if vertex not in maze:
                        maze[vertex] = {}
                    maze[vertex][neighbor] = fixed_maze[vertex, neighbor]
            maze_height = fixed_maze.shape[0] // maze_width
        
        # If given as a dictionary
        elif isinstance(fixed_maze, dict):
            maze = fixed_maze
            maze_width = 1
            for vertex in fixed_maze:
                for neighbor in fixed_maze[vertex]:
                    if neighbor - vertex > 1:
                        maze_width = neighbor - vertex
                        break
                if maze_width != 1:
                    break
            maze_height = int(numpy.ceil((max(fixed_maze) + 1) / maze_width))
        
        # Error if type is unrecognized
        else:
            raise Exception("Unhandled type", type(fixed_maze), "when loading fixed maze, should be a matrix")
        
        # Check dimensions
        if maze_width < 1 or maze_height < 1:
            raise Exception("Invalid maze dimensions in fixed maze")
        
#####################################################################################################################################################
#####################################################################################################################################################
