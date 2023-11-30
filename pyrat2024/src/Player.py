#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a player.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import abc

# Internal imports
from pyrat2024.src.Maze import Maze
from pyrat2024.src.GameState import GameState

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Player (abc.ABC):

    """
        This class is abstract and cannot be instantiated.
        You should use one of the subclasses to create a maze, or create your own subclass.

        A player is an agent that can play a PyRat game.
        The preprocessing method is called once at the beginning of the game.
        The turn method is called at each turn of the game.
        The postprocessing method is called once at the end of the game.
        Only the turn method is mandatory.
        If you want to keep track of some information between turns, you can define a constructor and add attributes to the object.
        Check examples to see how to do it properly.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                   name: str,
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

        # Debug
        assert isinstance(name, str) # Type check for the name
        assert isinstance(skin, str) # Type check for the skin

        # Public attributes
        self.name = name
        self.skin = skin

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def preprocessing ( self:       Self,
                        maze:       Maze,
                        game_state: GameState
                      ) ->          None:
        
        """
            This method can optionally be implemented in the child classes.
            It is called once at the beginning of the game.
            It is typically given more time than the turn function, to perform complex computations.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * None.
        """

        # Debug
        assert isinstance(maze, Maze) # Type check for the maze
        assert isinstance(game_state, GameState) # Type check for the game state

        # By default, this method does nothing unless implemented in the child classes
        pass

    #############################################################################################################################################

    @abc.abstractmethod
    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState
             ) ->          str:

        """
            This method is abstract and must be implemented in the child classes.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined as a static attribute of class Maze.
            These can be accessed using Maze.possible_actions.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions.
        """

        # Debug
        assert isinstance(maze, Maze) # Type check for the maze
        assert isinstance(game_state, GameState) # Type check for the game state

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#############################################################################################################################################

    def postprocessing ( self:       Self,
                         maze:       Maze,
                         game_state: GameState,
                         stats:      Dict[str, Any],
                       ) ->          None:

        """
            This method can optionally be implemented in the child classes.
            It is called once at the end of the game.
            It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
                * stats:      Statistics about the game.
            Out:
                * None.
        """

        # Debug
        assert isinstance(maze, Maze) # Type check for the maze
        assert isinstance(game_state, GameState) # Type check for the game state
        assert isinstance(stats, dict) # Type check for the stats
        assert all(isinstance(key, str) for key in stats.keys()) # Type check for the keys of the stats

        # By default, this method does nothing unless implemented in the child classes
        pass

#####################################################################################################################################################
#####################################################################################################################################################
