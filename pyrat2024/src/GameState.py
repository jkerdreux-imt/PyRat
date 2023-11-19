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

# External imports
from typing import *
from typing_extensions import *

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

        # Initialize state attributes
        self.player_locations = {}
        self.score_per_player = {}
        self.muds = {}
        self.teams = {}
        self.cheese = []
        self.turn = 0

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def copy ( self: Self
             ) ->    Self:
        
        """
            Creates a copy of the game state.
            In:
                * self: Reference to the current object.
            Out:
                * game_state_copy: Copy of the game state.
        """

        # Create the copy
        game_state_copy = GameState()
        game_state_copy.player_locations = self.player_locations.copy()
        game_state_copy.score_per_player = self.score_per_player.copy()
        game_state_copy.muds = self.muds.copy()
        game_state_copy.teams = self.teams.copy()
        game_state_copy.cheese = self.cheese.copy()
        game_state_copy.turn = self.turn
        return game_state_copy

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

        # Get whether the player is currently crossing mud
        in_mud = self.muds[name]["target"] is not None
        return in_mud
    
    #############################################################################################################################################

    def get_score_per_team ( self: Self
                           ) ->    Dict[str, float]:
        
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
