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
import abc

# PyRat imports
from pyrat.src.Maze import Maze
from pyrat.src.GameState import GameState
from pyrat.src.enums import Action, PlayerSkin

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
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self: Self,
                   name: Optional[str] = None,
                   skin: PlayerSkin = PlayerSkin.RAT
                 ) ->    Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
            In:
                * self: Reference to the current object.
                * name: Name of the player (if None, we take the name of the class).
                * skin: Skin of the player.
            Out:
                * A new instance of the class.
        """

        # Debug
        assert isinstance(name, (str, type(None))) # Type check for the name
        assert isinstance(skin, PlayerSkin) # Type check for the skin

        # Private attributes
        self.__name = name if name is not None else self.__class__.__name__
        self.__skin = skin

    #############################################################################################################################################
    #                                                            ATTRIBUTE ACCESSORS                                                            #
    #############################################################################################################################################

    @property
    def name ( self: Self,
             ) ->    str:
        
        """
            Getter for __name.
            In:
                * self: Reference to the current object.
            Out:
                * self.__name: The __name attribute.
        """

        # Get the attribute
        return self.__name

    #############################################################################################################################################

    @property
    def skin ( self: Self,
             ) ->    PlayerSkin:
        
        """
            Getter for __skin.
            In:
                * self: Reference to the current object.
            Out:
                * self.__skin: The __skin attribute.
        """

        # Get the attribute
        return self.__skin

    #############################################################################################################################################
 
    @skin.setter
    def skin ( self:  Self,
               value: PlayerSkin
             ) ->     None:
        
        """
            Setter for __skin.
            In:
                * self:  Reference to the current object.
                * value: New value for the __skin attribute.
            Out:
                * None.
        """

        # Set the attribute
        self.__skin = value

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
             ) ->          Action:

        """
            This method is abstract and must be implemented in the child classes.
            It is called at each turn of the game.
            It returns an action to perform among the possible actions, defined in the Action enumeration.
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
