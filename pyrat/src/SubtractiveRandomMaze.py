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

# PyRat imports
from pyrat.src.RandomMaze import RandomMaze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class SubtractiveRandomMaze (RandomMaze):

    """
        This class inherits from the RandomMaze class.
        Therefore, it has the attributes and methods defined in the RandomMaze class in addition to the ones defined below.

        A subtractive random maze is a random maze where the cells are removed one by one.
        The maze is created by removing cells from a full maze, and making sure the maze remains connected.
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
        
        # Generate the maze
        self._create_maze()

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _create_maze ( self: Self,
                     ) ->    None:
        
        """
            This method redefines the abstract method of the parent class.
            It creates a random maze using the parameters given at initialization.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Initialize maze with all cells
        for row in range(self.height):
            for col in range(self.width):
                self.add_vertex(self.rc_to_i(row, col))

        # Connect them
        for row in range(self.height):
            for col in range(self.width):
                if row > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row - 1, col))
                if col > 0:
                    self.add_edge(self.rc_to_i(row, col), self.rc_to_i(row, col - 1))

        # Remove some vertices until the desired density is reached
        target_nb_vertices = int(self.width * self.height * self._cell_percentage / 100)
        while self.nb_vertices() > target_nb_vertices:

            # Remove a random vertex
            vertex = self._rng.choice(list(self.vertices))
            self.remove_vertex(vertex)

            # Make sure the maze is still connected
            if not self.is_connected():
                self.add_vertex(vertex)
                row, col = self.i_to_rc(vertex)
                self.add_edge(vertex, self.rc_to_i(row - 1, col))
                self.add_edge(vertex, self.rc_to_i(row + 1, col))

        # Determine the maximum number of walls by computing the minimum spanning tree
        mst = self.minimum_spanning_tree()
        target_nb_walls = (self.nb_edges() - mst.nb_edges()) * self._wall_percentage / 100

#####################################################################################################################################################
#####################################################################################################################################################