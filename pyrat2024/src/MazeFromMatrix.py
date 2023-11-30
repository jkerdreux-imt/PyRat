#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a fixed maze from a given matrix.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import numpy

# Internal imports
from pyrat2024.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class MazeFromMatrix (Maze):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This is a maze that is created from a fixed description as a numpy.ndarray.
        Indices of rows and columns are the indices of the corresponding cells.
        Entries are the weights of the corresponding edges.
        Rows and columns with only 0 values will be ignored.
        This class can be useful to test a player on a fixed maze, to compare its performance with other players.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:        Self,
                   description: numpy.ndarray
                 ) ->           Self:

        """
            This function is the constructor of the class.
            In:
                * self:        Reference to the current object.
                * description: Fixed maze as a matrix.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__()

        # Debug
        assert isinstance(description, numpy.ndarray) # Type check for description
        assert len(description.shape) == 2 # Check that the description is a matrix
        assert description.shape[0] == description.shape[1] # Check that the matrix is square
        assert description.shape[0] > 1 # The maze has at least two vertices
        assert all(isinstance(weight, Integral) for weight in description.flatten()) # Weights are integers
        assert description == description.T # Check that the matrix is symmetric
        assert all(weight >= 0 for weight in description.flatten()) # Check that the weights are non-negative
        assert any(weight > 0 for weight in description.flatten()) # Check that the maze has at least one edge

        # Private attributes
        self.__description = description

        # Generate the maze
        self.__create_maze()

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __create_maze ( self: Self,
                      ) ->    None:

        """
            Creates a maze from the description provided at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Add vertices
        for vertex in range(self.__description.shape[0]):
            neighbors = self.__description[vertex].nonzero()[0].tolist()
            if len(neighbors) > 0:
                self.add_vertex(vertex)
        
        # Add edges
        for vertex in range(self.__description.shape[0]):
            neighbors = self.__description[vertex].nonzero()[0].tolist()
            for neighbor in neighbors:
                self.add_edge(vertex, neighbor, self.__description[vertex, neighbor])

        # Infer dimensions
        self._infer_dimensions()

#####################################################################################################################################################
#####################################################################################################################################################
