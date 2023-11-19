#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file is a template to save a PyRat game.
    It contains a few tags that will be replaced by the PyRat game when needed.
    Players will reproduce their actions in the same order as in the original game.
    Computations will not be made again.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# Internal imports
from pyrat2024.src.Player import Player
from pyrat2024.src.Maze import Maze
from pyrat2024.src.GameState import GameState
from pyrat2024.src.FixedPlayer import FixedPlayer

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Customize the game elements
    config = {CONFIG}
    
    # Instanciate the game with the chosen configuration
    game = Game(**config)

    # Description of the players
    player_descriptions = {PLAYERS}

    # Instanciate and register players
    for player_description in player_descriptions:
        player = FixedPlayer(player_description["name"], player_description["skin"], player_description["actions"])
        game.add_player(player, player_description["team"], player_description["location"])
    
    # Start the game and show statistics when over
    stats = game.start()
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################