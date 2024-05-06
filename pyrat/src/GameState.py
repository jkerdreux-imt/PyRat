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
import os

# PyRat imports
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
    #                                                               MAGIC METHODS                                                               #
    #############################################################################################################################################

    def __init__ ( self: Self,
                 ) ->    Self:

        """
            This function is the constructor of the class.
            When an object is instantiated, this method is called to initialize the object.
            This is where you should define the attributes of the object and set their initial values.
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

    def __str__ ( self: Self,
                ) ->    str:

        """
            This method returns a string representation of the object.
            This defines what will be shown when calling print on the object.
            In:
                * self: Reference to the current object.
            Out:
                * string: String representation of the object.
        """

        # Create the string
        string = "GameState object:\n"
        string += "|  Players: {}\n".format(self.player_locations)
        string += "|  Scores: {}\n".format(self.score_per_player)
        string += "|  Muds: {}\n".format(self.muds)
        string += "|  Teams: {}\n".format(self.teams)
        string += "|  Cheese: {}\n".format(self.cheese)
        string += "|  Turn: {}".format(self.turn)
        return string

    #############################################################################################################################################
    #                                                            ATTRIBUTE ACCESSORS                                                            #
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
 
    @turn.setter
    def turn ( self:  Self,
               value: Integral
             ) ->     None:
        
        """
            Setter for __turn.
            In:
                * self:  Reference to the current object.
                * value: New value for the __turn attribute.
            Out:
                * None.
        """

        # Debug
        assert caller_file() == os.path.join(os.path.dirname(os.path.realpath(__file__)), "Game.py") # The method is called by the engine

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
        if len(self.cheese) == 0:
            is_over = True
            return is_over

        # In a multi-team game, the game is over when no team can change their ranking anymore
        score_per_team = self.get_score_per_team()
        if len(score_per_team) > 1:
            is_over = True
            for team1 in score_per_team:
                for team2 in score_per_team:
                    if team1 != team2:
                        if score_per_team[team1] == score_per_team[team2] or (score_per_team[team1] < score_per_team[team2] and score_per_team[team1] + len(self.cheese) >= score_per_team[team2]):
                            is_over = False
            return is_over

        # The game is not over
        is_over = False
        return is_over

#####################################################################################################################################################
#####################################################################################################################################################
