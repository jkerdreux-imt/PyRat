#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains a few functions that can be useful to multiple players, while not making sense to define as methods of the classes.
    It is meant to be used as a library, and not to be executed directly.
    Do not hesitate to add your own functions here if you think they can be useful to other players.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *

# Internal imports
from pyrat2024 import Maze

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def locations_to_action ( maze:   Maze,
                          source: int,
                          target: int
                        ) ->      str: 

    """
        Function to transform two locations into an action to reach the target from the source.
        In:
            * source:     Vertex on which the player is.
            * target:     Vertex where the character wants to go.
            * maze_width: Width of the maze in number of cells.
        Out:
            * action: Name of the action to go from the source to the target.
    """

    # Get the coordinates difference
    difference = maze.coords_difference(source, target)

    # Translate in a move
    if difference == (0, 0):
        action = "nothing"
    elif difference == (0, -1):
        action = "west"
    elif difference == (0, 1):
        action = "east"
    elif difference == (1, 0):
        action = "south"
    elif difference == (-1, 0):
        action = "north"
    
    # Raise an error if the move is impossible
    else:
        raise Exception("Impossible move from", source, "to", target)
    return action

#####################################################################################################################################################
#####################################################################################################################################################