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

        # Public attributes
        self.player_locations = {}
        self.score_per_player = {}
        self.muds = {}
        self.teams = {}
        self.cheese = []
        self.turn = 0

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
