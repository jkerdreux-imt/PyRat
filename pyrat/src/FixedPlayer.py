#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a fixed player.
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
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class FixedPlayer (Player):

    """
        This player follows a predetermined list of actions.
        This is useful to save and replay a game.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:    Self,
                   name:    str,
                   skin:    str,
                   actions: List[str]
                 ) ->       Self:

        """
            This function is the constructor of the class.
            We do not duplicate asserts already made in the parent method.
            In:
                * self:    Reference to the current object.
                * name:    Name of the player.
                * skin:    Skin of the player.
                * actions: List of actions to perform.
            Out:
                * A new instance of the class.
        """

        # Inherit from parent class
        super().__init__(name, skin)

        # Debug
        assert isinstance(actions, list) # Type check for actions
        assert all(action in Maze.possible_actions for action in actions) # Check that all actions are valid

        # Private attributes
        self.__actions = actions
       
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState
             ) ->          str:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns the next action to perform.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions
        """

        # Get next action
        action = self.__actions.pop(0)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
