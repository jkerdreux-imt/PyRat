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

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import random

# Internal imports
from pyrat import Player, Maze, GameState
from utils import locations_to_action

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Random3 (Player):

    """
        This player is an improvement of the Random2 player.
        Here, we add elements that help us explore better the maze.
        More precisely, we keep a list (in a global variable to be updated at each turn) of cells that have already been visited in the game.
        Then, at each turn, we choose in priority a random move among those that lead us to an unvisited cell.
        If no such move exists, we move randomly using the method in "random_2".
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self: Self,
                   name: str = "Random 3",
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

        # We create an attribute to keep track of visited cells
        self.visited_cells = []
       
    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def turn ( self:       Self,
               maze:       Maze,
               game_state: GameState,
             ) ->          str:

        """
            This method redefines the abstract method of the parent class.
            It is called at each turn of the game.
            It returns an action that explores a random unvisited cell if possible.
            If no such action exists, it returns a random action that does not lead to a wall.
            In:
                * self:       Reference to the current object.
                * maze:       An object representing the maze in which the player plays.
                * game_state: An object representing the state of the game.
            Out:
                * action: One of the possible actions
        """

        # Mark current cell as visited
        if game_state.player_locations[self.name] not in self.visited_cells:
            self.visited_cells.append(game_state.player_locations[self.name])

        # Go to an unvisited neighbor in priority
        neighbors = maze.get_neighbors(game_state.player_locations[self.name])
        unvisited_neighbors = [neighbor for neighbor in neighbors if neighbor not in self.visited_cells]
        if len(unvisited_neighbors) > 0:
            neighbor = random.choice(unvisited_neighbors)
            
        # If there is no unvisited neighbor, choose one randomly
        else:
            neighbor = random.choice(neighbors)
        
        # Retrieve the corresponding action
        action = locations_to_action(maze, game_state.player_locations[self.name], neighbor)
        return action

#####################################################################################################################################################
#####################################################################################################################################################
