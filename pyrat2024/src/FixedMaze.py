#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a fixed maze.
    It is meant to be used as a library, and not to be executed directly.
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
from pyrat2024.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class FixedMaze (Maze):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        A fixed maze is a maze that is created from a fixed description.
        It can be provided as a mae object, a matrix, a dictionary, or a string of one of these last 2 representations.
        This class is especially useful to allow exporting a maze to a file, and then reusing it later.
        It is also useful to test a player on a fixed maze, to compare its performance with other players.
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
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__()
        
        # Generate the maze
        self._create_maze(description)

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self:        Self,
                       description: Union[None, str, Maze, Dict[int, Dict[int, int]], numpy.ndarray]
                     ) ->           None:

        """
            This function creates a maze from the description provided at initialization.
            In:
                * self: Reference to the current object.
                * description: Fixed maze in any handled format (an existing maze, an adjacency dictionary, a numpy matrix, or a string of one of these last 2 representations).
            Out:
                * None.
        """

        # Transform in a structure if a string
        maze = ast.literal_eval(description) if isinstance(description, str) else description
        if isinstance(description, list):
            maze = numpy.array(maze)
        
        # If given as a matrix
        if isinstance(maze, numpy.ndarray):
            for vertex in range(maze.shape[0]):
                neighbors = maze[vertex].nonzero()[0].tolist()
                if len(neighbors) > 0:
                    self.add_vertex(vertex)
            for vertex in range(maze.shape[0]):
                neighbors = maze[vertex].nonzero()[0].tolist()
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor, maze[vertex, neighbor])
            self._infer_dimensions()
        
        # If given as a dictionary
        elif isinstance(maze, dict):
            for vertex in maze:
                self.add_vertex(vertex)
            for vertex in maze:
                neighbors = maze[vertex]
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor, maze[vertex][neighbor])
            self._infer_dimensions()
        
        # If given as a maze
        elif isinstance(maze, Maze):
            for vertex in maze.get_vertices():
                self.add_vertex(vertex)
            for vertex in maze.get_vertices():
                neighbors = maze.get_neighbors(vertex)
                for neighbor in neighbors:
                    self.add_edge(vertex, neighbor, maze.get_weight(vertex, neighbor))
            self.width = maze.width
            self.height = maze.height
            
        # Error if type is unrecognized
        else:
            raise TypeError("The provided maze description is of an unrecognized type.")
    
    #############################################################################################################################################

    def _infer_dimensions ( self: Self
                          ) ->    None:

        """
            This function infers the width and height of the maze from its vertices and edges.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Infer width
        self.width = 1
        for vertex in self.get_vertices():
            neighbors = self.get_neighbors(vertex)
            if max(neighbors) - vertex > 1:
                self.width = max(neighbors) - vertex
                break
        
        # Infer height
        self.height = int(numpy.ceil((max(self.get_vertices()) + 1) / self.width))

#####################################################################################################################################################
#####################################################################################################################################################
