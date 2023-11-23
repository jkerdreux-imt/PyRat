#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a fixed maze from a given dictionary.
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

class MazeFromDict (Maze):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This is a maze that is created from a fixed description as a dictionary, where keys are cell indices.
        Associated values are dictionaries, where keys are neighbors of the corresponding cell, and values are the weights of the corresponding edges.
        This class is especially useful to allow exporting a maze to a file, and then reusing it later.
        It is also useful to test a player on a fixed maze, to compare its performance with other players.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:        Self,
                   description: Dict[Integral, Dict[Integral, Number]]
                 ) ->           Self:

        """
            This function is the constructor of the class.
            In:
                * self:        Reference to the current object.
                * description: Fixed maze as a dictionary.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__()
        
        # Debug
        assert isinstance(description, dict) # Type check for the description
        assert all(isinstance(vertex, Integral) for vertex in description) # Type check for the vertices
        assert all(isinstance(neighbor, Integral) for vertex in description for neighbor in description[vertex]) # Type check for the neighbors
        assert all(isinstance(weight, Number) for vertex in description for neighbor in description[vertex] for weight in description[vertex][neighbor]) # Type check for the weights
        assert len(description) > 1 # The maze has at least two vertices
        assert all(len(description[vertex]) > 0 for vertex in description) # All vertices are connected to at least one neighbor
        assert all(vertex in description[neighbor] for vertex in description for neighbor in description[vertex]) # The graph is symmetric
        assert all(description[vertex][neighbor] == description[neighbor][vertex] for vertex in description for neighbor in description[vertex]) # Weights are symmetric
        assert all(description[vertex][neighbor] > 0 for vertex in description for neighbor in description[vertex]) # Weights are positive

        # Private attributes
        self.__description = description

        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    def _create_maze ( self: Self,
                     ) ->    None:

        """
            This method redefines the abstract method of the parent class.
            It creates a maze from the description provided at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Add vertices
        for vertex in self.description:
            self.add_vertex(vertex)
        
        # Add edges
        for vertex in self.description:
            neighbors = self.description[vertex]
            for neighbor in neighbors:
                self.add_edge(vertex, neighbor, self.description[vertex][neighbor])

        # Infer dimensions
        self._infer_dimensions()

#####################################################################################################################################################
#####################################################################################################################################################
