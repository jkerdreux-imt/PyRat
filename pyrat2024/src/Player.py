#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    TODO
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
from typing import *
from typing_extensions import *
import abc

# Internal imports
from Maze import Maze

#####################################################################################################################################################
################################################################## CLASS DEFINITION #################################################################
#####################################################################################################################################################

class Player (metaclass=abc.ABCMeta):

    """
        This class is abstract and cannot be instantiated.
        It represents a player in the game.
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
                * self: Reference to the current object.
        """

        # Inherit from parent class
        super(Player, self).__init__()
        
        # Attributes
        self.name = name
        self.skin = skin

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    @abc.abstractmethod
    def preprocessing ( maze:             Maze,
                        teams:            Dict[str, List[str]],
                        player_locations: Dict[str, int],
                        cheese:           List[int],
                        possible_actions: List[str],
                      ) ->                None:
        
        """
            This method is abstract and can optionally be implemented in the child classes.
            It is called once at the beginning of the game.
            It is typically given more time than the turn function, to perform complex computations.
            In:
                * maze:             An object representing the maze in which the player plays.
                * name:             Name of the player controlled by this function.
                * teams:            Recap of the teams of players.
                * player_locations: Locations for all players in the game.
                * cheese:           List of available pieces of cheese in the maze.
                * possible_actions: List of possible actions.
            Out:
                * None.
        """

        # By default, this method does nothing unless implemented in the child classes
        pass

    #############################################################################################################################################

    @abc.abstractmethod
    def turn ( maze:             Maze,
               teams:            Dict[str, List[str]],
               player_locations: Dict[str, int],
               player_scores:    Dict[str, float],
               player_muds:      Dict[str, Dict[str, Union[None, int]]],
               cheese:           List[int],
               possible_actions: List[str]
             ) ->                str:

        """
            This method is abstract and must be implemented in the child classes.
            It is called at every turn of the game and should return an action within the set of possible actions.
            You can access the memory you stored during the preprocessing function by doing memory.my_key.
            You can also update the existing memory with new information, or create new entries as memory.my_key = my_value.
            In:
                * maze:             An object representing the maze in which the player plays.
                * teams:            Recap of the teams of players.
                * player_locations: Locations for all players in the game.
                * player_scores:    Scores for all players in the game.
                * player_muds:      Indicates which player is currently crossing mud.
                * cheese:           List of available pieces of cheese in the maze.
                * possible_actions: List of possible actions.
            Out:
                * action: One of the possible actions, as given in possible_actions.
        """

        # This method must be implemented in the child classes
        # By default we raise an error
        raise NotImplementedError("This method must be implemented in the child classes.")

#############################################################################################################################################

    @abc.abstractmethod
    def postprocessing ( maze:             Maze,
                         teams:            Dict[str, List[str]],
                         player_locations: Dict[str, int],
                         player_scores:    Dict[str, float],
                         player_muds:      Dict[str, Dict[str, Union[None, int]]],
                         cheese:           List[int],
                         possible_actions: List[str],
                         stats:            Dict[str, Any],
                       ) ->                None:

        """
            This method is abstract and can optionally be implemented in the child classes.
            It is called once at the end of the game.
            It is not timed, and can be used to make some cleanup, analyses of the completed game, model training, etc.
            In:
                * maze:             An object representing the maze in which the player plays.
                * teams:            Recap of the teams of players.
                * player_locations: Locations for all players in the game.
                * player_scores:    Scores for all players in the game.
                * player_muds:      Indicates which player is currently crossing mud.
                * cheese:           List of available pieces of cheese in the maze.
                * possible_actions: List of possible actions.
                * stats:            Statistics about the game.
            Out:
                * None.
        """

        # By default, this method does nothing unless implemented in the child classes
        pass

#####################################################################################################################################################
#####################################################################################################################################################
