#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a PyRat game.
    It is meant to be used as a library, and not to be executed directly.
"""

#####################################################################################################################################################
###################################################################### IMPORTS ######################################################################
#####################################################################################################################################################

# External imports
import numpy
import numpy.random as nprandom
import multiprocessing
import time
import traceback
import ast
import sys
import os
import datetime
from typing import *
from typing_extensions import *

# Internal imports
from pyrat2024.src.Maze import Maze
from pyrat2024.src.RandomMaze import RandomMaze
from pyrat2024.src.FixedMaze import FixedMaze
from pyrat2024.src.Player import Player
from pyrat2024.src.GameState import GameState
from pyrat2024.src.RenderingEngine import RenderingEngine
from pyrat2024.src.AsciiRenderingEngine import AsciiRenderingEngine
from pyrat2024.src.PygameRenderingEngine import PygameRenderingEngine

#####################################################################################################################################################
###################################################################### CLASSES ######################################################################
#####################################################################################################################################################

class Game ():

    """
        A game is a class that allows to play a game of PyRat.
        It is initialized with the parameters of the game.
        Players should then be added to the game using the add_player method.
        Finally, the start method should be called to start the game.
        Once the game is over, it will provide statistics about the game.
        Set your own parameters to define interesting objectives for the players.
    """

    #############################################################################################################################################
    #                                                                CONSTRUCTOR                                                                #
    #############################################################################################################################################

    def __init__ ( self:                Self,
                   random_seed:         Union[None, int] = None,
                   random_seed_maze:    Union[None, int] = None,
                   random_seed_cheese:  Union[None, int] = None,
                   random_seed_players: Union[None, int] = None,
                   maze_width:          int = 15,
                   maze_height:         int = 13,
                   cell_percentage:     float = 80.0,
                   wall_percentage:     float = 60.0,
                   mud_percentage:      float = 20.0,
                   mud_range:           Tuple[int, int] = (4, 9),
                   fixed_maze:          Union[None, str, Maze, Dict[int, Dict[int, int]], numpy.ndarray] = None,
                   nb_cheese:           int = 21,
                   fixed_cheese:        Union[None, str, List[int]] = None,
                   render_mode:         str = "gui",
                   render_simplified:   bool = False,
                   gui_speed:           float = 1.0,
                   trace_length:        int = 0,
                   fullscreen:          bool = False,
                   save_path:           str = ".",
                   save_game:           bool = False,
                   preprocessing_time:  float = 3.0,
                   turn_time:           float = 0.1,
                   synchronous:         bool = False,
                   continue_on_error:   bool = False
                 ) ->                   Self:

        """
            This function is the constructor of the class.
            In:
                * self:                Reference to the current object.
                * random_seed:         Global random seed for all elements, set to None for a random value.
                * random_seed_maze:    Random seed for the maze generation, set to None for a random value.
                * random_seed_cheese:  Random seed for the pieces of cheese distribution, set to None for a random value.
                * random_seed_players: Random seed for the initial location of players, set to None for a random value.
                * maze_width:          Width of the maze in number of cells.
                * maze_height:         Height of the maze in number of cells.
                * cell_percentage:     Percentage of cells that can be accessed in the maze, 0%% being a useless maze, and 100%% being a full rectangular maze.
                * wall_percentage:     Percentage of walls in the maze, 0%% being an empty maze, and 100%% being the maximum number of walls that keep the maze connected.
                * mud_percentage:      Percentage of pairs of adjacent cells that are separated by mud in the maze.
                * mud_range:           Interval of turns needed to cross mud.
                * fixed_maze:          Fixed maze in any PyRat accepted representation (takes priority over any maze description and will automatically set maze_height and maze_width).
                * nb_cheese:           Number of pieces of cheese in the maze.
                * fixed_cheese:        Fixed list of cheese (takes priority over number of cheese).
                * render_mode:         Method to display the game (avaible modes are "gui", "ansi", "ascii", and "no_rendering").
                * render_simplified:   If the maze is rendered, hides some elements that are not essential.
                * gui_speed:           When rendering as GUI, controls the speed of the game.
                * trace_length:        Maximum length of the trace to display when players are moving (GUI rendering only).
                * fullscreen:          Renders the game in fullscreen mode (GUI rendering only).
                * save_path:           Path where games are saved.
                * save_game:           Indicates if the game should be saved.
                * preprocessing_time:  Time given to the players before the game starts.
                * turn_time:           Time after which players will miss a turn.
                * synchronous:         If set, waits for all players to return an action before moving, even if turn_time is exceeded.
                * continue_on_error:   If a player crashes, continues the game anyway.
            Out:
                * A new instance of the class.
        """

        # Check arguments are correct
        #assert 0 < maze_width
        #assert 0 < maze_height
        #assert 0.0 <= cell_percentage <= 100.0
        #assert 0.0 <= wall_percentage <= 100.0
        #assert 0.0 <= mud_percentage <= 100.0
        #assert 1 < mud_range[0] <= mud_range[1]
        #assert 0 < nb_cheese
        #assert 0.0 <= preprocessing_time
        #assert 0.0 <= turn_time
        
        # Save arguments as attributes
        self.random_seed = random_seed
        self.random_seed_maze = random_seed_maze
        self.random_seed_cheese = random_seed_cheese
        self.random_seed_players = random_seed_players
        self.maze_width = maze_width
        self.maze_height = maze_height
        self.cell_percentage = cell_percentage
        self.wall_percentage = wall_percentage
        self.mud_percentage = mud_percentage
        self.mud_range = mud_range
        self.fixed_maze = fixed_maze
        self.nb_cheese = nb_cheese
        self.fixed_cheese = fixed_cheese
        self.render_mode = render_mode
        self.render_simplified = render_simplified
        self.gui_speed = gui_speed
        self.trace_length = trace_length
        self.fullscreen = fullscreen
        self.save_path = save_path
        self.save_game = save_game
        self.preprocessing_time = preprocessing_time
        self.turn_time = turn_time
        self.synchronous = synchronous
        self.continue_on_error = continue_on_error
        
        # Initialize game attributes
        self.game_random_seed_maze = None
        self.game_random_seed_cheese = None
        self.game_random_seed_players = None
        self.players = None
        self.initial_game_state = None
        self.player_traces = None
        self.actions_history = None
        self.rendering_engine = None
        self.maze = None
        self.reset()

    #############################################################################################################################################
    #                                                              PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def reset ( self: Self
              ) ->    None:
        
        """
            Resets the game to its initial state, without any player, cheese, etc.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """
        
        # Set random seeds for the game
        self.game_random_seed_maze = self.random_seed if self.random_seed is not None else self.random_seed_maze if self.random_seed_maze is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        self.game_random_seed_cheese = self.random_seed if self.random_seed is not None else self.random_seed_cheese if self.random_seed_cheese is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        self.game_random_seed_players = self.random_seed if self.random_seed is not None else self.random_seed_players if self.random_seed_players is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        
        # Initialize game elements
        self.players = []
        self.initial_game_state = GameState()

        # Initialize game analysis elements
        self.player_traces = {}
        self.actions_history = {}

        # Initialize the maze
        if self.fixed_maze is None:
            self.maze = RandomMaze(self.maze_width, self.maze_height, self.cell_percentage, self.wall_percentage, self.mud_percentage, self.mud_range, self.game_random_seed_maze)
        else:
            self.maze = FixedMaze(self.fixed_maze)
        
        # Initialize the rendering engine
        if self.render_mode in ["ascii", "ansi"]:
            use_colors = self.render_mode == "ansi"
            self.rendering_engine = AsciiRenderingEngine(use_colors, self.render_simplified)
        elif self.render_mode == "gui":
            self.rendering_engine = PygameRenderingEngine(self.fullscreen, self.trace_length, self.gui_speed, self.render_simplified)
        elif self.render_mode == "no_rendering":
            self.rendering_engine = RenderingEngine(self.render_simplified)
        
    #############################################################################################################################################
    
    def add_player ( self:     Self,
                     player:   Player,
                     team:     str = "",
                     location: str = "center"
                   ) ->        None:
        
        """
            Adds a player to the game.
            In:
                * self:     Reference to the current object.
                * player:   Player to add.
                * team:     Team of the player.
                * location: Controls initial location of the player ("random", "same", "center", or a fixed index).
            Out:
                * None.
        """

        # Set random seed
        nprandom.seed(self.game_random_seed_players + len(self.players))
        
        # Check if the name is unique
        if player.name in self.player_traces:
            raise Exception("Player name", player.name, "already exists")

        # Set random initial location
        if location == "random":
            self.initial_game_state.player_locations[player.name] = nprandom.choice(list(self.maze.get_vertices()))
        
        # Or same initial location as previous player
        elif location == "same" and len(self.players) > 0:
            self.initial_game_state.player_locations[player.name] = list(self.initial_game_state.player_locations.values())[-1]

        # Or initial location in the center
        elif location == "center":
            self.initial_game_state.player_locations[player.name] = self.maze.rc_to_i(self.maze.height // 2, self.maze.width // 2)
        
        # Or fixed index initial location
        elif isinstance(location, int) and 0 <= location < self.maze.height * self.maze.width:
            if location in self.maze.get_vertices():
               self.initial_game_state.player_locations[player.name] = location
            else:
                print("Warning: Player %s cannot start at unreachable location %d, starting at closest cell (using Euclidean distance)" % (player.name, location), file=sys.stderr)
                location_rc = numpy.array(self.maze.i_to_rc(location))
                valid_cells = self.maze.get_vertices()
                distances = [numpy.linalg.norm(location_rc - numpy.array(self.maze.i_to_rc(cell))) for cell in valid_cells]
                self.initial_game_state.player_locations[player.name] = valid_cells[numpy.argmin(distances)]
        
        # Or invalid initial location
        else:
            raise Exception("Invalid initial location provided for player", player.name)
        
        # Append to team
        if team not in self.initial_game_state.teams:
            self.initial_game_state.teams[team] = []
        self.initial_game_state.teams[team].append(player.name)

        # Initialize other elements of game state
        self.initial_game_state.score_per_player[player.name] = 0
        self.initial_game_state.muds[player.name] = {"target": None, "count": 0}

        # Other attributes
        self.players.append(player)
        self.player_traces[player.name] = []
        self.actions_history[player.name] = []
        
    #############################################################################################################################################

    def start ( self: Self
              ) ->    Dict[str, Any]:

        """
            Starts a game, asking players for decisions until the game is over.
            In:
                * self: Reference to the current object.
            Out:
                * stats: Game statistics computed during the game.
        """
        
        # We catch exceptions that may happen during the game
        try:
            
            # Start the game
            self._distribute_cheese()
            game_state = self.initial_game_state.copy()
            possible_actions = ["nothing", "north", "east", "south", "west"]

            # Initialize stats
            stats = {"players": {}, "turns": -1}
            for player in self.players:
                stats["players"][player.name] = {"actions": {"mud": 0, "error": 0, "miss": 0, "nothing": 0, "north": 0, "east": 0, "south": 0, "west": 0, "wall": 0}, "score": 0, "turn_durations": [], "preprocessing_duration": None}
            
            # Create a process per player
            turn_start_synchronizer = multiprocessing.Manager().Barrier(len(self.players) + 1)
            turn_timeout_lock = multiprocessing.Manager().Lock()
            player_processes = {}
            player_fixed_data = {}
            for player in self.players:
                player_fixed_data[player.name] = [self.maze.copy(), possible_actions.copy()]
                player_processes[player.name] = {"process": None, "input_queue": multiprocessing.Manager().Queue(), "output_queue": multiprocessing.Manager().Queue(), "turn_end_synchronizer": multiprocessing.Manager().Barrier(2)}
                player_processes[player.name]["process"] = multiprocessing.Process(target=_player_process_function, args=(player, player_processes[player.name]["input_queue"], player_processes[player.name]["output_queue"], turn_start_synchronizer, turn_timeout_lock, player_processes[player.name]["turn_end_synchronizer"],))
                player_processes[player.name]["process"].start()

            # If playing asynchrounously, we create processs to wait instead of missing players
            if not self.synchronous:
                waiter_processes = {}
                for player in self.players:
                    waiter_processes[player.name] = {"process": None, "input_queue": multiprocessing.Manager().Queue()}
                    waiter_processes[player.name]["process"] = multiprocessing.Process(target=_waiter_process_function, args=(waiter_processes[player.name]["input_queue"], turn_start_synchronizer,))
                    waiter_processes[player.name]["process"].start()

            # Initial rendering of the maze
            self.rendering_engine.render(self.players, self.maze, game_state)
            
            # We play until the game is over
            players_ready = [player.name for player in self.players]
            players_running = {player.name: True for player in self.players}
            while any(players_running.values()):

                # We communicate the state of the game to the players not in mud
                for ready_player in players_ready:
                    final_stats = stats.copy() if game_state.game_over() else None
                    player_processes[ready_player]["input_queue"].put((*player_fixed_data[ready_player], game_state.copy(), final_stats))
                turn_start_synchronizer.wait()
                
                # Check that a turn lasts al least the time it should for each player
                # Useful to guarantee processs have at least the required time
                sleep_time = self.preprocessing_time if game_state.turn == 0 else self.turn_time
                time.sleep(sleep_time)
                
                # In synchronous mode, we wait for everyone
                actions_as_text = {player.name: "postprocessing" for player in self.players}
                durations = {player.name: None for player in self.players}
                if self.synchronous:
                    for player in self.players:
                        player_processes[player.name]["turn_end_synchronizer"].wait()
                        actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()

                # Otherwise, we block the possibility to return an action and check who answered in time
                else:

                    # Wait at least for those in mud
                    for player in self.players:
                        if game_state.is_in_mud(player.name) and players_running[player.name]:
                            player_processes[player.name]["turn_end_synchronizer"].wait()
                            actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()

                    # For others, set timeout and wait for output info of those who passed just before timeout
                    with turn_timeout_lock:
                        for player in self.players:
                            if not game_state.is_in_mud(player.name) and players_running[player.name]:
                                if not player_processes[player.name]["output_queue"].empty():
                                    player_processes[player.name]["turn_end_synchronizer"].wait()
                                    actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()
                                else:
                                    actions_as_text[player.name] = "miss"
                
                # Check which players are ready to continue
                players_ready = []
                for player in self.players:
                    if actions_as_text[player.name].startswith("postprocessing"):
                        players_running[player.name] = False
                    if not self.synchronous and (actions_as_text[player.name].startswith("postprocessing") or actions_as_text[player.name] == "miss"):
                        waiter_processes[player.name]["input_queue"].put(True)
                    else:
                        players_ready.append(player.name)

                # Check for errors
                if any([actions_as_text[player.name].endswith("error") for player in self.players]) and not self.continue_on_error:
                    raise Exception("A player has crashed, exiting")

                # We save the turn info if we are not postprocessing
                if not game_state.game_over():
                
                    # Apply the actions
                    corrected_actions = {player.name: actions_as_text[player.name] if actions_as_text[player.name] in possible_actions else "nothing" for player in self.players}
                    new_game_state = self._determine_new_game_state(game_state, corrected_actions)
                    
                    # Save stats
                    for player in self.players:
                        if not actions_as_text[player.name].startswith("preprocessing"):
                            if actions_as_text[player.name] in ["north", "west", "south", "east"] and game_state.player_locations[player.name] == new_game_state.player_locations[player.name] and not game_state.is_in_mud(player.name):
                                stats["players"][player.name]["actions"]["wall"] += 1
                            else:
                                stats["players"][player.name]["actions"][actions_as_text[player.name]] += 1
                            if actions_as_text[player.name] != "mud":
                                self.actions_history[player.name].append(corrected_actions[player.name])
                        if durations[player.name] is not None:
                            if actions_as_text[player.name].startswith("preprocessing"):
                                stats["players"][player.name]["preprocessing_duration"] = durations[player.name]
                            else:
                                stats["players"][player.name]["turn_durations"].append(durations[player.name])
                        stats["players"][player.name]["score"] = new_game_state.score_per_player[player.name]
                    stats["turns"] = game_state.turn
                    
                    # Go to next turn
                    self.rendering_engine.render(self.players, self.maze, new_game_state)
                    game_state = new_game_state

        # In case of an error, we ignore stats
        except:
            print(traceback.format_exc(), file=sys.stderr)
            stats = {}
        
        # Apply end actions before returning
        self._end()
        return stats

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def _end ( self: Self
             ) ->    None:
        
        """
            Actions to do at the end of the game if needed.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """

        # We save the game if asked
        if self.save_game:
            
            # Create the saves directory if needed
            if not os.path.exists(self.save_path):
                os.makedirs(self.save_path)

            # Prepare the config dictionary
            config = {"synchronous": True,
                      "fixed_maze": self.maze.adjacency,
                      "fixed_cheese": self.initial_game_state.cheese}
            
            # Create a description of the players
            player_descriptions = []
            for player in self.players:
                player_descriptions.append({"name": player.name,
                                            "skin": player.skin,
                                            "team": [team for team in self.initial_game_state.teams if player.name in self.initial_game_state.teams[team]][0],
                                            "location": self.initial_game_state.player_locations[player.name],
                                            "actions": self.actions_history[player.name]})

            # Create the players' file, forcing players to their initial locations
            output_file_name = os.path.join(self.save_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f.py"))
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "save_template.py"), "r") as save_template_file:
                save_template = save_template_file.read()
                save_template = save_template.replace("{PLAYERS}", str(player_descriptions).replace("}, ", "},\n                           "))
                save_template = save_template.replace("{CONFIG}", str(config).replace(", '", ",\n              '"))
                with open(output_file_name, "w") as output_file:
                    print(save_template, file=output_file)

        # Apply ending actions of the rendering engine
        self.rendering_engine.end()
        
    #############################################################################################################################################

    def _determine_new_game_state ( self:       Self,
                                    game_state: GameState,
                                    actions:    Dict[str, str]
                                  ) ->          GameState:
        
        """
            Updates the game state after a turn, given decisions of players.
            In:
                * self:       Reference to the current object.
                * game_state: Current game state.
                * actions:    Action performed per player.                
            Out:
                * new_game_state: New game state after the turn.
        """

        # Initialize new game state
        new_game_state = game_state.copy()
        new_game_state.turn += 1

        # Move all players accordingly
        for player in self.players:
            try:
                row, col = self.maze.i_to_rc(game_state.player_locations[player.name])
                target = None
                if actions[player.name] == "north" and row > 0:
                    target = self.maze.rc_to_i(row - 1, col)
                elif actions[player.name] == "south" and row < self.maze.height - 1:
                    target = self.maze.rc_to_i(row + 1, col)
                elif actions[player.name] == "west" and col > 0:
                    target = self.maze.rc_to_i(row, col - 1)
                elif actions[player.name] == "east" and col < self.maze.width - 1:
                    target = self.maze.rc_to_i(row, col + 1)
                if target is not None and target in self.maze.get_neighbors(game_state.player_locations[player.name]):
                    weight = self.maze.get_weight(game_state.player_locations[player.name], target)
                    if weight == 1:
                        new_game_state.player_locations[player.name] = target
                    elif weight > 1:
                        new_game_state.muds[player.name]["target"] = target
                        new_game_state.muds[player.name]["count"] = weight
            except:
                print("Warning: Invalid action %s for player %s" % (str(actions[player.name]), player.name), file=sys.stderr)

        # All players in mud advance a bit
        for player in self.players:
            if new_game_state.is_in_mud(player.name):
                new_game_state.muds[player.name]["count"] -= 1
                if new_game_state.muds[player.name]["count"] == 0:
                    new_game_state.player_locations[player.name] = new_game_state.muds[player.name]["target"]
                    new_game_state.muds[player.name]["target"] = None

        # Update cheese and scores
        for c in game_state.cheese:
            players_on_cheese = [player for player in self.players if c == new_game_state.player_locations[player.name]]
            for player_on_cheese in players_on_cheese:
                new_game_state.score_per_player[player_on_cheese.name] += 1.0 / len(players_on_cheese)
            if len(players_on_cheese) > 0:
                new_game_state.cheese.remove(c)
        
        # Store trace for GUI
        for player in self.players:
            self.player_traces[player.name].append(new_game_state.player_locations[player.name])
            self.player_traces[player.name] = self.player_traces[player.name][-self.trace_length:]
        
        # Return new game state
        return new_game_state
        
    #############################################################################################################################################

    def _distribute_cheese ( self: Self,
                           ) ->    List[int]:
        
        """
            Distributes pieces of cheese in the maze, according to the provided criteria.
            If a fixed list of cheese was provided, it is used.
            Otherwise, the cheese is distributed randomly.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """
        
        # Find usable cells
        available_cells = [i for i in self.maze.get_vertices() if i not in self.initial_game_state.player_locations.values()]

        # If we ask for a fixed list of cheese, we use it
        if self.fixed_cheese is not None:
            
            # Convert string to list if needed
            self.initial_game_state.cheese = ast.literal_eval(self.fixed_cheese) if isinstance(self.fixed_cheese, str) else self.fixed_cheese
            if not isinstance(self.initial_game_state.cheese, list):
                raise Exception("Unhandled type", type(self.initial_game_state.cheese), "when loading fixed cheese, should be a list")
            
            # Check if there are duplicates
            if len(self.initial_game_state.cheese) != len(set(self.initial_game_state.cheese)):
                raise Exception("Duplicates in fixed cheese")
            
            # Check if there is enough space
            if len(available_cells) < len(self.initial_game_state.cheese):
                raise Exception("Not enough space for asked number of cheese")
            
            # Check if all locations are valid
            if len(set(self.initial_game_state.cheese) & set(available_cells)) != len(self.initial_game_state.cheese):
                raise Exception("Some cheese cannot be placed")
            
        # Otherwise, we place the cheese randomly
        else:
            
            # Set random seed
            nprandom.seed(self.game_random_seed_cheese)

            # Check if there is enough space
            if len(available_cells) < self.nb_cheese:
                raise Exception("Not enough space for asked number of cheese")

            # We place the cheese randomly
            nprandom.shuffle(available_cells)
            self.initial_game_state.cheese = available_cells[:self.nb_cheese]

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def _player_process_function ( player:                  Player,
                               input_queue:             multiprocessing.Queue,
                               output_queue:            multiprocessing.Queue,
                               turn_start_synchronizer: multiprocessing.Barrier,
                               turn_timeout_lock:       multiprocessing.Lock,
                               turn_end_synchronizer:   multiprocessing.Barrier
                             ) ->                       None:
    
    """
        This function is executed in a separate process per player.
        It handles the communication with the player and calls the functions given as arguments.
        It is defined outside of the class due to multiprocessing limitations.
        In:
            * player:                  Player controlled by the process.
            * input_queue:             Queue to receive the game state.
            * output_queue:            Queue to send the action.
            * turn_start_synchronizer: Barrier to synchronize the start of the turn.
            * turn_timeout_lock:       Lock to synchronize the timeout of the turn.
            * turn_end_synchronizer:   Barrier to synchronize the end of the turn.
        Out:
            * None.
    """

    # We catch exceptions that may happen during the game
    try:

        # Main loop
        while True:
            
            # Wait for all players ready
            turn_start_synchronizer.wait()
            maze, possible_actions, game_state, final_stats = input_queue.get()
            duration = None
            try:
                
                # Call postprocessing once the game is over
                if final_stats is not None:
                    action = "postprocessing_error"
                    player.postprocessing(maze, game_state, possible_actions, final_stats)
                    action = "postprocessing"
                    
                # If in mud, we return immediately (main process will wait for us in all cases)
                elif game_state.is_in_mud(player.name):
                    action = "mud"
                
                # Otherwise, we ask for an action
                else:
                
                    # Measure start time
                    start = time.process_time()
                    
                    # Go
                    if game_state.turn == 0:
                        action = "preprocessing_error"
                        player.preprocessing(maze, game_state, possible_actions)
                        action = "preprocessing"
                    else:
                        action = "error"
                        a = player.turn(maze, game_state, possible_actions)
                        if a not in possible_actions:
                            raise Exception("Invalid action %s by player %s" % (str(a), player.name))
                        action = a
                    
                    # Set end time
                    end_time = time.process_time()
                    duration = end_time - start
                        
            # Print error message in case of a crash
            except:
                print("Player %s has crashed with the following error:" % player.name, file=sys.stderr)
                print(traceback.format_exc(), file=sys.stderr)
                    
            # Turn is over
            with turn_timeout_lock:
                output_queue.put((action, duration))
            turn_end_synchronizer.wait()
            if action.startswith("postprocessing"):
                break

    # Ignore
    except:
        pass

#####################################################################################################################################################

def _waiter_process_function ( input_queue:             multiprocessing.Queue,
                               turn_start_synchronizer: multiprocessing.Barrier,
                             ) ->                       None:
    
    """
        This function is executed in a separate process per player.
        It handles the timeouts of the player.
        It is defined outside of the class due to multiprocessing limitations.
        In:
            * input_queue:             Queue to receive the game state.
            * turn_start_synchronizer: Barrier to synchronize the start of the turn.
        Out:
            * None.
    """

    # We catch exceptions that may happen during the game
    try:

        # We just mark as ready
        while True:
            _ = input_queue.get()
            turn_start_synchronizer.wait()

    # Ignore
    except:
        pass

#####################################################################################################################################################
#####################################################################################################################################################
