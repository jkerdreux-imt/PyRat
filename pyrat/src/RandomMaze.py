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
import sys
import random
import abc

# PyRat imports
from pyrat.src.Maze import Maze

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class RandomMaze (Maze, abc.ABC):

    """
        This class inherits from the Maze class.
        Therefore, it has the attributes and methods defined in the Maze class in addition to the ones defined below.

        This class is abstract and cannot be instantiated.
        You should use one of the subclasses to create a maze, or create your own subclass.

        A random maze is a maze that is created randomly.
        You can specify the size of the maze, the density of cells, walls, and mud, and the range of the mud values.
        You can also specify a random seed to reproduce the same maze later.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:            Self,
                   cell_percentage: Number,
                   wall_percentage: Number,
                   mud_percentage:  Number,
                   mud_range:       Tuple[Integral, Integral],
                   random_seed:     Optional[Integral] = None,
                   *args:           Any,
                   **kwargs:        Any
                 ) ->               Self:

        """
            This function is the constructor of the class.
            We do not duplicate asserts already made in the parent method.
            In:
                * self:            Reference to the current object.
                * cell_percentage: Percentage of cells to be reachable.
                * wall_percentage: Percentage of walls to be present.
                * mud_percentage:  Percentage of mud to be present.
                * mud_range:       Range of the mud values.
                * random_seed:     Random seed for the maze generation, set to None for a random value.
                * args:            Arguments to pass to the parent constructor.
                * kwargs:          Keyword arguments to pass to the parent constructor.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(*args, **kwargs)
        
        # Debug
        assert isinstance(cell_percentage, Number) # Type check for cell_percentage
        assert isinstance(wall_percentage, Number) # Type check for wall_percentage
        assert isinstance(mud_percentage, Number) # Type check for mud_percentage
        assert isinstance(mud_range, (tuple, list)) # Type check for mud_range
        assert isinstance(random_seed, (Integral, type(None))) # Type check for random_seed
        assert random_seed is None or 0 <= random_seed < sys.maxsize # random_seed is a valid seed
        assert len(mud_range) == 2 # Mud range is an interval of 2 elements
        assert isinstance(mud_range[0], Integral) # Type check for mud_range[0]
        assert isinstance(mud_range[1], Integral) # Type check for mud_range[1]
        assert 0.0 <= cell_percentage <= 100.0 # cell_percentage is a percentage
        assert 0.0 <= wall_percentage <= 100.0 # wall_percentage is a percentage
        assert 0.0 <= mud_percentage <= 100.0 # mud_percentage is a percentage
        assert 1 < mud_range[0] <= mud_range[1] # mud_range is a valid interval with minimum value 1

        # Protected attributes
        self._cell_percentage = cell_percentage
        self._wall_percentage = wall_percentage
        self._mud_percentage = mud_percentage
        self._mud_range = mud_range
        self._random_seed = random_seed
        self._rng = random.Random(self._random_seed)

    #############################################################################################################################################
    #                                                             PROTECTED METHODS                                                             #
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

        # Add cells
        self._add_cells()
        
        # Add walls
        self._add_walls()

        # Add mud
        self._add_mud()

        # TODO

#####################################################################################################################################################
#####################################################################################################################################################