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
import abc

# Internal imports
from Graph import Graph

#####################################################################################################################################################
################################################################## CLASS DEFINITION #################################################################
#####################################################################################################################################################

class Maze (Graph, metaclass=abc.ABCMeta):

    """
        This class is abstract and cannot be instantiated.
        A maze is a particular type of graph.
        Each vertex is a cell, indexed by a number from 0 to width*height-1.
        There are edges between adjacent cells.
        Weights indicate the number of actions required to go from one cell to an adjacent one.
        In this implementation, cells are placed on a grid and can only be connected along the cardinal directions.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:   Self,
                   width:  Union[None, int] = None,
                   height: Union[None, int] = None
                 ) ->      Self:

        """
            This function is the constructor of the class.
            In:
                * self:   Reference to the current object.
                * width:  Width of the maze, initialized to None in case it is determined afterward.
                * height: Height of the maze, initialized to None in case it is determined afterward.
            Out:
                * self: Reference to the current object.
        """

        # Inherit from parent class
        super(Maze, self).__init__()
        
        # Attributes
        self.width = width
        self.height = height

#####################################################################################################################################################
#####################################################################################################################################################
