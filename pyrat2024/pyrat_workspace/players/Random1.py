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
import random

# Internal imports
from pyrat2024 import Player, Maze, GameState

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

    def turn ( self:             Self,
               maze:             Maze,
               game_state:       GameState,
               possible_actions: List[str]
             ) ->                str:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns a random action from the list of possible actions.
            In:
                * self:             Reference to the current object.
                * maze:             An object representing the maze in which the player plays.
                * game_state:       An object representing the state of the game.
                * possible_actions: List of possible actions.
            Out:
                * action: One of the possible actions, as given in possible_actions.
        """

        # Choose a random action to perform
        action = random.choice(possible_actions)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
