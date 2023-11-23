#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file defines a game in which 3 teams of players compete in a maze with mud.
    When running this file, it will create a PyRat game, add players to it, and start the game.
    This is an example, made to illustrate the use of the PyRat library.
    You can use it as a template to develop your own game.
    You can customize the game elements (maze size, number of cheese, etc.) in the "config" dictionary.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import sys
import os

# Add "players" directory to the path
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "players"))

# Internal imports
from pyrat2024 import Game
from Random1 import Random1
from Random2 import Random2
from Random3 import Random3
from Random4 import Random4

#####################################################################################################################################################
######################################################################## GO! ########################################################################
#####################################################################################################################################################

if __name__ == "__main__":

    # Customize the game elements
    config = {"maze_width": 19,
              "maze_height": 15,
              "mud_percentage": 30.0,
              "mud_range": (2, 7),
              "wall_percentage": 60.0,
              "cell_percentage": 90.0,
              "nb_cheese": 41}
    
    # Instanciate the game with the chosen configuration
    game = Game(**config)

    # Instanciate and register players
    # Here we make multiple teams of players, each team having a different type of player
    # Team "Random 1" will start at the center of the maze (default)
    team_1_name = "Random 1"
    team_1_skin = "rat"
    for i in range(4):
        player = Random1("P " + str(i+1), team_1_skin)
        game.add_player(player, team_1_name)
    
    # Team "Random 2" will start at the top left corner
    team_2_name = "Random 2"
    team_2_skin = "python"
    team_2_start_location = 0
    for i in range(3):
        player = Random2("P " + str(i+5), team_2_skin)
        game.add_player(player, team_2_name, team_2_start_location)

    # Team "Random 3" will start at a random location
    # Location "same" indicates that the player will start at the same location as the previous player
    team_3_name = "Random 3"
    team_3_skin = "default"
    team_3_start_location = ["random", "same"]
    for i in range(2):
        player = Random3("P " + str(i+8), team_3_skin)
        game.add_player(player, team_3_name, team_3_start_location[i])

    # Team "Random 4" will start at the the bottom right corner
    team_4_name = "Random 4"
    team_4_skin = "mario"
    team_4_start_location = config["maze_width"] * config["maze_height"] - 1
    player = Random4("P 10", team_4_skin)
    game.add_player(player, team_4_name, team_4_start_location)
    
    # Start the game and show statistics when over
    stats = game.start()
    print(stats)

#####################################################################################################################################################
#####################################################################################################################################################