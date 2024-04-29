#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a particular player.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
from numbers import *
import random

# PyRat imports
from pyrat import Player, Maze, GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random1 (Player):

    """
        This player controls a PyRat character by performing random actions.
        More precisely, at each turn, a random choice among all possible actions is selected.
        Note that this doesn't take into account the structure of the maze.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                   name: str = "Random 1",
                   skin: str = "default"
                 ) ->    Self:

        """
            This function is the constructor of the class.
            In:
                * self: Reference to the current object.
                * name: Name of the player.
                * skin: Skin of the player.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(name, skin)
       
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          Maze.PossibleAction:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Maze.PossibleAction enumeration.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Choose a random action to perform
        action = random.choice(list(Maze.PossibleAction))
        return action

#####################################################################################################################################################
#####################################################################################################################################################
