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
from pyrat.src.Player import Player
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class RenderingEngine ():

    """
        A rendering engine is an object that can render a PyRat game.
        By defaut, this engine renders nothing, which is a valid rendering mode for a PyRat game.
        Inherit from this class to create a rendering engine that does something.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:              Self,
                   render_simplified: bool = False
                 ) ->                 Self:

        """
            This function is the constructor of the class.
            In:
                * self:              Reference to the current object.
                * render_simplified: Whether to render the simplified version of the game.
            Out:
                * A new instance of the class.
        """

        # Debug
        assert isinstance(render_simplified, bool) # Type check for render_simplified

        # Protected attributes
        self._render_simplified = render_simplified
        
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def render ( self:       Self,
                 players:    List[Player],
                 maze:       Maze,
                 game_state: GameState,
               ) ->          None:
        
        """
            This method does nothing.
            Redefine it in the child classes to render the game somehow.
            In:
                * self:       Reference to the current object.
                * players:    PLayers of the game.
                * maze:       Maze of the game.
                * game_state: State of the game.
            Out:
                * None.
        """

        # Debug
        assert isinstance(players, list) # Type check for players
        assert all(isinstance(player, Player) for player in players)
        assert isinstance(maze, Maze)
        assert isinstance(game_state, GameState)

        # Nothing to do
        pass

    #############################################################################################################################################

    def end ( self: Self,
            ) ->    None:
        
        """
            This method does nothing.
            Redefine it in the child classes to do something when the game ends if needed.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # Nothing to do
        pass

#####################################################################################################################################################
#####################################################################################################################################################
