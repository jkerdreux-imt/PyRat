#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a game state.
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
import os

# Internal imports
from pyrat.src.utils import caller_file

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class GameState ():

    """
        A game state is a snapshot of the game at a given time.
        It gives an overview of scores, locations, available cheese, who is currently crossing mud, etc.
        It also provides a few useful functions to determine who is currently leading, etc.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                 ) ->    Self:

        """
            This function is the constructor of the class.
            In:
                * self: Reference to the current object.
            Out:
                * A new instance of the class.
        """

        # Private attributes
        self.__player_locations = {}
        self.__score_per_player = {}
        self.__muds = {}
        self.__teams = {}
        self.__cheese = []
        self.__turn = None

    #############################################################################################################################################
    #                                                                  GETTERS                                                                  #
    #############################################################################################################################################

    @property
    def player_locations ( self: Self
                         ) ->    Dict[str, Integral]:
        
        """
            Getter for __player_locations.
            In:
                * self: Reference to the current object.
            Out:
                * self.__player_locations: The __player_locations attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__player_locations

    #############################################################################################################################################

    @property
    def score_per_player ( self: Self
                         ) ->    Dict[str, Number]:
        
        """
            Getter for __score_per_player.
            In:
                * self: Reference to the current object.
            Out:
                * self.__score_per_player: The __score_per_player attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__score_per_player

    #############################################################################################################################################

    @property
    def muds ( self: Self
             ) ->    Dict[str, Dict[str, Optional[Integral]]]:
        
        """
            Getter for __muds.
            In:
                * self: Reference to the current object.
            Out:
                * self.__muds: The __muds attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__muds

    #############################################################################################################################################

    @property
    def teams ( self: Self
              ) ->    Dict[str, List[str]]:
        
        """
            Getter for __teams.
            In:
                * self: Reference to the current object.
            Out:
                * self.__teams: The __teams attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__teams

    #############################################################################################################################################

    @property
    def cheese ( self: Self
               ) ->    List[Integral]:
        
        """
            Getter for __cheese.
            In:
                * self: Reference to the current object.
            Out:
                * self.__cheese: The __cheese attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__cheese

    #############################################################################################################################################

    @property
    def turn ( self: Self
             ) ->    Integral:
        
        """
            Getter for __turn.
            In:
                * self: Reference to the current object.
            Out:
                * self.__turn: The __turn attribute.
        """

        # Debug
        assert self.__turn is not None or caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The object has been initialized by the game engine, or the method is called by the engine

        # Return the attribute
        return self.__turn

    #############################################################################################################################################
    #                                                                  SETTERS                                                                  #
    #############################################################################################################################################

    @turn.setter
    def turn ( self:  Self,
               value: Integral
             ) ->     Integral:
        
        """
            Setter for __turn.
            In:
                * self:  Reference to the current object.
                * value: New value for the __turn attribute.
            Out:
                * None.
        """

        # Set the attribute
        self.__turn = value

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################
    
    def is_in_mud ( self: Self,
                    name: str
                  ) ->    bool:

        """
            This method returns whether a player is currently crossing mud.
            In:
                * self: Reference to the current object.
                * name: Name of the player.
            Out:
                * in_mud: Whether the player is currently crossing mud.
        """

        # Debug
        assert isinstance(name, str) # Type check for the name
        assert name in self.muds # Check that the player exists

        # Get whether the player is currently crossing mud
        in_mud = self.muds[name]["target"] is not None
        return in_mud
    
    #############################################################################################################################################

    def get_score_per_team ( self: Self
                           ) ->    Dict[str, Number]:
        
        """
            Returns the score per team.
            In:
                * self: Reference to the current object.
            Out:
                * score_per_team: Dictionary of scores.
        """
        
        # Aggregate players of the team
        score_per_team = {team: round(sum([self.score_per_player[player] for player in self.teams[team]]), 5) for team in self.teams}
        return score_per_team

    #############################################################################################################################################

    def game_over ( self: Self
                  ) ->    bool:
        
        """
            This function checks if the game is over.
            The game is over when there is no more cheese or when no team can catch up anymore.
            In:
                * self: Reference to the current object.
            Out:
                * is_over: Boolean indicating if the game is over.
        """

        # The game is over when there is no more cheese
        is_over = len(self.cheese) == 0

        # The game is over when no team can catch up anymore
        score_per_team = self.get_score_per_team()
        max_score = max(score_per_team.values())
        for team in self.teams:
            if score_per_team[team] != max_score and score_per_team[team] + len(self.cheese) >= max_score:
                is_over = False

        # Return the result
        return is_over

#####################################################################################################################################################
#####################################################################################################################################################
