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

# Internal imports
from pyrat.src.Maze import Maze

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
                   description: Dict[Integral, Dict[Integral, Integral]]
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
        assert isinstance(description, dict) # Type check for description
        assert all(isinstance(vertex, Integral) for vertex in description) # Type check for description
        assert all(isinstance(neighbor, Integral) for vertex in description for neighbor in description[vertex]) # Type check for description
        assert all(isinstance(description[vertex][neighbor], Integral) for vertex in description for neighbor in description[vertex]) # Type check for description
        assert len(description) > 1 # The maze has at least two vertices
        assert all(len(description[vertex]) > 0 for vertex in description) # All vertices are connected to at least one neighbor
        assert all(vertex in description[neighbor] for vertex in description for neighbor in description[vertex]) # The graph is symmetric
        assert all(description[vertex][neighbor] == description[neighbor][vertex] for vertex in description for neighbor in description[vertex]) # Weights are symmetric
        assert all(description[vertex][neighbor] > 0 for vertex in description for neighbor in description[vertex]) # Weights are positive

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
        
        # Determine the vertices
        vertices = self.__description.keys()

        # Determine the edges
        edges = []
        for vertex in self.__description:
            neighbors = self.__description[vertex]
            for neighbor in neighbors:
                edges.append((vertex, neighbor, self.__description[vertex][neighbor]))

        # Build the maze
        self._initialize_maze(vertices, edges)

#####################################################################################################################################################
#####################################################################################################################################################
