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
import abc
import math

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class FixedMaze (Maze, abc.ABC):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This class is abstract and cannot be instantiated.
        You should use one of the subclasses to create a maze, or create your own subclass.

        This is a maze that is created from a fixed description.
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

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
    #############################################################################################################################################

    def _initialize_maze ( self:     Self,
                           vertices: List[Integral],
                           edges:    List[Tuple[Integral, Integral, Integral]]
                         ) ->        None:

        """
            This function creates a maze from a list of vertices and a list of edges.
            It is meant to be used in the subclasses to create the maze.
            In:
                * self:     Reference to the current object.
                * vertices: List of vertices.
                * edges:    List of edges.
            Out:
                * None.
        """

        # Determine the dimensions of the maze
        self._width = max([abs(edge[1] - edge[0]) for edge in edges])
        self._height = math.ceil((max(vertices) + 1) / self.width)

        # Add vertices and edges
        for vertex in vertices:
            self.add_vertex(vertex)
        for edge in edges:
            self.add_edge(edge[0], edge[1], edge[2])

#####################################################################################################################################################
#####################################################################################################################################################
