#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a maze.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
import abc

# Internal imports
from pyrat2024.src.Graph import Graph

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Maze (Graph, metaclass=abc.ABCMeta):

    """
        This class inherits from the Graph class.
        Therefore, it has the attributes and methods defined in the Graph class in addition to the ones defined below.
        
        This class is abstract and cannot be instantiated.
        You should use one of the subclasses to create a maze, or create your own subclass.
        
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
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__()
        
        # Save arguments as attributes
        self.width = width
        self.height = height

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def copy ( self: Self
             ) ->    Self:
        
        """
            Creates a copy of the maze.
            In:
                * self: Reference to the current object.
            Out:
                * maze_copy: Copy of the maze.
        """

        # Create the copy
        maze_copy = Maze(self.width, self.height)
        maze_copy.adjacency = self.adjacency.copy()
        return maze_copy

    #############################################################################################################################################

    def i_to_rc ( self: Self,
                  i:    int,
                ) ->    Tuple[int, int]:
        
        """
            Transforms a maze index in a pair (row, col).
            In:
                * self: Reference to the current object.
                * i:    Index of the cell.
            Out:
                * row: Row of the cell.
                * col: Column of the cell.
        """
        
        # Conversion
        row = i // self.width
        col = i % self.width
        return row, col
    
    #############################################################################################################################################
    
    def rc_to_i ( self: Self,
                  row:  int,
                  col:  int,
                ) ->    int:
        
        """
            Transforms a (row, col) pair of maze coordiates (lexicographic order) in a maze index.
            In:
                * self: Reference to the current object.
                * row:  Row of the cell.
                * col:  Column of the cell.
            Out:
                * i: Corresponding cell index in the maze.
        """
        
        # Conversion
        i = row * self.width + col
        return i
    
    #############################################################################################################################################
    
    def rc_exists ( self: Self,
                    row:  int,
                    col:  int,
                  ) ->    int:
        
        """
            Checks if a given (row, col) pair corresponds to a valid cell in the maze.
            In:
                * self: Reference to the current object.
                * row:  Row of the cell.
                * col:  Column of the cell.
            Out:
                * exists: True if the cell exists, False otherwise.
        """
        
        # Check if the cell exists
        exists = 0 <= row < self.height and 0 <= col < self.width and self.rc_to_i(row, col) in self.get_vertices()
        return exists
    
    #############################################################################################################################################

    def coords_difference ( self:     Self,
                            vertex_1: int,
                            vertex_2: int,
                          ) ->        Tuple[int, int]:
        
        """
            Computes the difference between the coordinates of two cells.
            In:
                * self:     Reference to the current object.
                * vertex_1: First cell.
                * vertex_2: Second cell.
            Out:
                * row_diff: Difference between the rows of the cells.
                * col_diff: Difference between the columns of the cells.
        """
        
        # Get coordinates
        row_1, col_1 = self.i_to_rc(vertex_1)
        row_2, col_2 = self.i_to_rc(vertex_2)

        # Compute difference
        row_diff = row_2 - row_1
        col_diff = col_2 - col_1
        return row_diff, col_diff
    
#####################################################################################################################################################
#####################################################################################################################################################
