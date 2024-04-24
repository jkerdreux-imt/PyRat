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

# External typing imports
from typing import *
from typing_extensions import *
from numbers import *

# Other external imports
import copy
import numpy
import numpy.random as nprandom
import multiprocessing
import multiprocessing.managers as mpmanagers
import time
import traceback
import sys
import os
import datetime

# Internal imports
from pyrat.src.Maze import Maze
from pyrat.src.RandomMaze import RandomMaze
from pyrat.src.MazeFromDict import MazeFromDict
from pyrat.src.MazeFromMatrix import MazeFromMatrix
from pyrat.src.Player import Player
from pyrat.src.GameState import GameState
from pyrat.src.RenderingEngine import RenderingEngine
from pyrat.src.AsciiRenderingEngine import AsciiRenderingEngine
from pyrat.src.PygameRenderingEngine import PygameRenderingEngine

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
                   random_seed:         Optional[Integral] = None,
                   random_seed_maze:    Optional[Integral] = None,
                   random_seed_cheese:  Optional[Integral] = None,
                   random_seed_players: Optional[Integral] = None,
                   maze_width:          Integral = 15,
                   maze_height:         Integral = 13,
                   cell_percentage:     Number = 80.0,
                   wall_percentage:     Number = 60.0,
                   mud_percentage:      Number = 20.0,
                   mud_range:           Tuple[Integral, Integral] = (4, 9),
                   fixed_maze:          Optional[Union[Dict[Integral, Integral], numpy.ndarray]] = None,
                   nb_cheese:           Integral = 21,
                   fixed_cheese:        Optional[List[Integral]] = None,
                   render_mode:         str = "gui",
                   render_simplified:   bool = False,
                   gui_speed:           Number = 1.0,
                   trace_length:        Integral = 0,
                   fullscreen:          bool = False,
                   save_path:           str = ".",
                   save_game:           bool = False,
                   preprocessing_time:  Number = 3.0,
                   turn_time:           Number = 0.1,
                   game_mode:           str = "standard",
                   continue_on_error:   bool = False
                 ) ->                   Self:

        """
            This function is the constructor of the class.
            Assertions checked in the objects manipulated by the game are not checked again.
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
                * gui_speed:           When rendering as GUI, controls the speed of the game (GUI rendering only).
                * trace_length:        Maximum length of the trace to display when players are moving (GUI rendering only).
                * fullscreen:          Renders the game in fullscreen mode (GUI rendering only).
                * save_path:           Path where games are saved.
                * save_game:           Indicates if the game should be saved.
                * preprocessing_time:  Time given to the players before the game starts.
                * turn_time:           Time after which players will miss a turn.
                * game_mode:           Indicates if players play concurrently ("standard"), wait for each other ("synchronous"), or if multiprocessing is disabled ("sequential").
                * continue_on_error:   If a player crashes, continues the game anyway.
            Out:
                * A new instance of the class.
        """

        # Debug
        assert isinstance(random_seed, (Integral, type(None))) # Type check for random_seed
        assert isinstance(random_seed_maze, (Integral, type(None))) # Type check for random_seed_maze
        assert isinstance(random_seed_cheese, (Integral, type(None))) # Type check for random_seed_cheese
        assert isinstance(random_seed_players, (Integral, type(None))) # Type check for random_seed_players
        assert random_seed is None or (random_seed is not None and random_seed_maze is None and random_seed_cheese is None and random_seed_players is None) # If random_seed is set, other random seeds should not be set
        assert isinstance(render_mode, str) # Type check for render_mode
        assert render_mode in ["gui", "ansi", "ascii", "no_rendering"] # Type check for render_mode
        assert isinstance(turn_time, Number) # Type check for render_simplified
        assert turn_time >= 0 # Turn time should be non-negative
        assert isinstance(preprocessing_time, Number) # Type check for preprocessing_time
        assert preprocessing_time >= 0 # Preprocessing time should be non-negative
        assert isinstance(game_mode, str) # Type check for game_mode
        assert game_mode in ["standard", "synchronous", "sequential"] # Type check for game_mode
        assert isinstance(continue_on_error, bool) # Type check for continue_on_error
        assert not(game_mode == "sequential" and render_mode == "gui") # Sequential mode is not compatible with GUI rendering
        
        # Private attributes
        self.__random_seed = random_seed
        self.__random_seed_maze = random_seed_maze
        self.__random_seed_cheese = random_seed_cheese
        self.__random_seed_players = random_seed_players
        self.__maze_width = maze_width
        self.__maze_height = maze_height
        self.__cell_percentage = cell_percentage
        self.__wall_percentage = wall_percentage
        self.__mud_percentage = mud_percentage
        self.__mud_range = mud_range
        self.__fixed_maze = fixed_maze
        self.__nb_cheese = nb_cheese
        self.__fixed_cheese = fixed_cheese
        self.__render_mode = render_mode
        self.__render_simplified = render_simplified
        self.__gui_speed = gui_speed
        self.__trace_length = trace_length
        self.__fullscreen = fullscreen
        self.__save_path = save_path
        self.__save_game = save_game
        self.__preprocessing_time = preprocessing_time
        self.__turn_time = turn_time
        self.__game_mode = game_mode
        self.__continue_on_error = continue_on_error
        self.__game_random_seed_maze = None
        self.__game_random_seed_cheese = None
        self.__game_random_seed_players = None
        self.__players_asked_location = []
        self.__players = []
        self.__initial_game_state = None
        self.__player_traces = None
        self.__actions_history = None
        self.__rendering_engine = None
        self.__maze = None

        # Initialize the game
        self.__reset()

    #############################################################################################################################################
    #                                                              PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def add_player ( self:     Self,
                     player:   Player,
                     team:     str = "",
                     location: Union[str, Integral] = "center"
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

        # Debug
        assert isinstance(player, Player) # Type check for player
        assert isinstance(team, str) # Type check for team
        assert isinstance(location, (str, Integral)) # Type check for location
        assert location in ["random", "same", "center"] or (isinstance(location, Integral) and 0 <= location < self.__maze.height * self.__maze.width) # Type check for location
        assert player.name not in self.__player_traces # Player name should be unique

        # Set random seed
        nprandom.seed(self.__game_random_seed_players + len(self.__players))
        
        # Set initial location
        # If random, we choose a random location
        # If same, we choose the same location as the previous player
        # If center, we choose the center of the maze
        # If a fixed index, we choose the closest cell to the index
        self.__players_asked_location.append(location)
        if location == "random":
            self.__initial_game_state.player_locations[player.name] = nprandom.choice(list(self.__maze.vertices))
        elif location == "same" and len(self.__players) > 0:
            self.__initial_game_state.player_locations[player.name] = list(self.__initial_game_state.player_locations.values())[-1]
        elif location == "center":
            self.__initial_game_state.player_locations[player.name] = self.__maze.rc_to_i(self.__maze.height // 2, self.__maze.width // 2)
        elif isinstance(location, Integral) and self.__maze.i_exists(location):
            self.__initial_game_state.player_locations[player.name] = location
        else:
            print("Warning: Player '%s' cannot start at unreachable location %d, starting at closest cell (using Euclidean distance)" % (player.name, location), file=sys.stderr)
            location_rc = numpy.array(self.__maze.i_to_rc(location))
            valid_cells = self.__maze.vertices
            distances = [numpy.linalg.norm(location_rc - numpy.array(self.__maze.i_to_rc(cell))) for cell in valid_cells]
            self.__initial_game_state.player_locations[player.name] = valid_cells[numpy.argmin(distances)]
        
        # Append to team
        if team not in self.__initial_game_state.teams:
            self.__initial_game_state.teams[team] = []
        self.__initial_game_state.teams[team].append(player.name)

        # Initialize other elements of game state
        self.__initial_game_state.score_per_player[player.name] = 0
        self.__initial_game_state.muds[player.name] = {"target": None, "count": 0}

        # Other attributes
        self.__players.append(player)
        self.__player_traces[player.name] = []
        self.__actions_history[player.name] = []
        
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
        
        # Debug
        assert len(self.__players) > 0 # At least 1 player

        # We catch exceptions that may happen during the game
        try:
            
            # Reset the game
            if self.__initial_game_state.turn is not None:
                self.__reset()
            self.__initial_game_state.turn = 0

            # Initialize stats
            stats = {"players": {}, "turns": -1}
            for player in self.__players:
                stats["players"][player.name] = {"actions": {"mud": 0, "error": 0, "miss": 0, "nothing": 0, "north": 0, "east": 0, "south": 0, "west": 0, "wall": 0}, "score": 0, "turn_durations": [], "preprocessing_duration": None}
            
            # In multiprocessing mode, prepare processes
            maze_per_player = {player.name: copy.deepcopy(self.__maze) for player in self.__players}
            if self.__game_mode != "sequential":

                # Create a process per player
                turn_start_synchronizer = multiprocessing.Manager().Barrier(len(self.__players) + 1)
                turn_timeout_lock = multiprocessing.Manager().Lock()
                player_processes = {}
                for player in self.__players:
                    player_processes[player.name] = {"process": None, "input_queue": multiprocessing.Manager().Queue(), "output_queue": multiprocessing.Manager().Queue(), "turn_end_synchronizer": multiprocessing.Manager().Barrier(2)}
                    player_processes[player.name]["process"] = multiprocessing.Process(target=_player_process_function, args=(player, maze_per_player[player.name], player_processes[player.name]["input_queue"], player_processes[player.name]["output_queue"], turn_start_synchronizer, turn_timeout_lock, player_processes[player.name]["turn_end_synchronizer"], None, None,))
                    player_processes[player.name]["process"].start()

                # If playing in standard mode, we create processs to wait instead of missing players
                if self.__game_mode == "standard":
                    waiter_processes = {}
                    for player in self.__players:
                        waiter_processes[player.name] = {"process": None, "input_queue": multiprocessing.Manager().Queue()}
                        waiter_processes[player.name]["process"] = multiprocessing.Process(target=_waiter_process_function, args=(waiter_processes[player.name]["input_queue"], turn_start_synchronizer,))
                        waiter_processes[player.name]["process"].start()

            # Initial rendering of the maze
            self.__rendering_engine.render(self.__players, self.__maze, self.__initial_game_state)
            
            # We play until the game is over
            game_state = copy.deepcopy(self.__initial_game_state)
            players_ready = [player for player in self.__players]
            players_running = {player.name: True for player in self.__players}
            while any(players_running.values()):

                # We communicate the state of the game to the players not in mud
                actions_as_text = {player.name: "miss" for player in self.__players}
                durations = {player.name: None for player in self.__players}
                for ready_player in players_ready:
                    final_stats = copy.deepcopy(stats) if game_state.game_over() else {}
                    player_game_state = copy.deepcopy(game_state)
                    if self.__game_mode != "sequential":
                        player_processes[ready_player.name]["input_queue"].put((player_game_state, final_stats))
                    else:
                        actions_as_text[ready_player.name], durations[ready_player.name] = _player_process_function(ready_player, maze_per_player[ready_player.name], None, None, None, None, None, player_game_state, final_stats)
                
                # In multiprocessing mode, we for everybody to receive data to start
                # In sequential mode, decisions are already received at this point
                if self.__game_mode != "sequential":
                    turn_start_synchronizer.wait()

                # Wait a bit
                sleep_time = self.__preprocessing_time if game_state.turn == 0 else self.__turn_time
                time.sleep(sleep_time)

                # In synchronous mode, we wait for everyone
                if self.__game_mode == "synchronous":
                    for player in self.__players:
                        player_processes[player.name]["turn_end_synchronizer"].wait()
                        actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()

                # In standard mode, we block the possibility to return an action and check who answered in time
                elif self.__game_mode == "standard":

                    # Wait at least for those in mud
                    for player in self.__players:
                        if game_state.is_in_mud(player.name) and players_running[player.name]:
                            player_processes[player.name]["turn_end_synchronizer"].wait()
                            actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()

                    # For others, set timeout and wait for output info of those who passed just before timeout
                    with turn_timeout_lock:
                        for player in self.__players:
                            if not game_state.is_in_mud(player.name) and players_running[player.name]:
                                if not player_processes[player.name]["output_queue"].empty():
                                    player_processes[player.name]["turn_end_synchronizer"].wait()
                                    actions_as_text[player.name], durations[player.name] = player_processes[player.name]["output_queue"].get()

                # Check which players are ready to continue
                players_ready = []
                for player in self.__players:
                    if actions_as_text[player.name].startswith("postprocessing"):
                        players_running[player.name] = False
                    if self.__game_mode == "standard" and (actions_as_text[player.name].startswith("postprocessing") or actions_as_text[player.name] == "miss"):
                        waiter_processes[player.name]["input_queue"].put(True)
                    else:
                        players_ready.append(player)

                # Check for errors
                if any([actions_as_text[player.name].endswith("error") for player in self.__players]) and not self.__continue_on_error:
                    raise Exception("A player has crashed, exiting")

                # We save the turn info if we are not postprocessing
                if not game_state.game_over():
                
                    # Apply the actions
                    corrected_actions = {player.name: actions_as_text[player.name] if actions_as_text[player.name] in Maze.possible_actions else "nothing" for player in self.__players}
                    new_game_state = self.__determine_new_game_state(game_state, corrected_actions)
                    
                    # Save stats
                    for player in self.__players:
                        if not actions_as_text[player.name].startswith("preprocessing"):
                            if actions_as_text[player.name] in ["north", "west", "south", "east"] and game_state.player_locations[player.name] == new_game_state.player_locations[player.name] and not game_state.is_in_mud(player.name):
                                stats["players"][player.name]["actions"]["wall"] += 1
                            else:
                                stats["players"][player.name]["actions"][actions_as_text[player.name]] += 1
                            if actions_as_text[player.name] != "mud":
                                self.__actions_history[player.name].append(corrected_actions[player.name])
                        if durations[player.name] is not None:
                            if actions_as_text[player.name].startswith("preprocessing"):
                                stats["players"][player.name]["preprocessing_duration"] = durations[player.name]
                            else:
                                stats["players"][player.name]["turn_durations"].append(durations[player.name])
                        stats["players"][player.name]["score"] = new_game_state.score_per_player[player.name]
                    stats["turns"] = game_state.turn
                    
                    # Go to next turn
                    self.__rendering_engine.render(self.__players, self.__maze, new_game_state)
                    game_state = new_game_state

        # In case of an error, we ignore stats
        except:
            print(traceback.format_exc(), file=sys.stderr)
            stats = {}
        
        # Apply end actions before returning
        self.__end(stats == {})
        return stats

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __reset ( self: Self
                ) ->    None:
        
        """
            Resets the game to its initial state.
            It will keep players and will insert them as they were added.
            In:
                * self: Reference to the current object.
            Out:
                * None.
        """
        
        # Set random seeds for the game
        self.__game_random_seed_maze = self.__random_seed if self.__random_seed is not None else self.__random_seed_maze if self.__random_seed_maze is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        self.__game_random_seed_cheese = self.__random_seed if self.__random_seed is not None else self.__random_seed_cheese if self.__random_seed_cheese is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        self.__game_random_seed_players = self.__random_seed if self.__random_seed is not None else self.__random_seed_players if self.__random_seed_players is not None else nprandom.randint(numpy.iinfo(numpy.int32).max)
        
        # Reset game analysis elements
        self.__player_traces = {}
        self.__actions_history = {}
        
        # Initialize the maze
        if self.__fixed_maze is None:
            self.__maze = RandomMaze(self.__maze_width, self.__maze_height, self.__cell_percentage, self.__wall_percentage, self.__mud_percentage, self.__mud_range, self.__game_random_seed_maze)
        elif isinstance(self.__fixed_maze, dict):
            self.__maze = MazeFromDict(self.__fixed_maze)
        else:
            self.__maze = MazeFromMatrix(self.__fixed_maze)

        # Initialize the rendering engine
        if self.__render_mode in ["ascii", "ansi"]:
            use_colors = self.__render_mode == "ansi"
            self.__rendering_engine = AsciiRenderingEngine(use_colors, self.__render_simplified)
        elif self.__render_mode == "gui":
            self.__rendering_engine = PygameRenderingEngine(self.__fullscreen, self.__trace_length, self.__gui_speed, self.__render_simplified)
        elif self.__render_mode == "no_rendering":
            self.__rendering_engine = RenderingEngine(self.__render_simplified)
        
        # Initialize the game state
        previous_initial_state = copy.deepcopy(self.__initial_game_state)
        self.__initial_game_state = GameState()

        # Add players as they were added
        for i in range(len(self.__players)):
            player = self.__players.pop(0)
            player_asked_location = self.__players_asked_location.pop(0)
            player_team = [team for team in previous_initial_state.teams if player.name in previous_initial_state.teams[team]][0]
            self.add_player(player, player_team, player_asked_location)

        # Add cheese
        available_cells = [i for i in self.__maze.vertices if i not in self.__initial_game_state.player_locations.values()]
        self.__initial_game_state.cheese.extend(self.__distribute_cheese(available_cells))
        
    #############################################################################################################################################
    
    def __end ( self:         Self,
                game_crashed: bool,
              ) ->            None:
        
        """
            Actions to do at the end of the game if needed.
            In:
                * self:         Reference to the current object.
                * game_crashed: Indicates if the game crashed.
            Out:
                * None.
        """

        # Debug
        assert isinstance(game_crashed, bool) # Type check for game_crashed
        assert isinstance(self.__save_game, bool) # Type check for self.__save_game
        assert isinstance(self.__save_path, str) # Type check for self.__save_path

        # We save the game if asked
        if self.__save_game and not game_crashed:
            
            # Create the saves directory if needed
            if not os.path.exists(self.__save_path):
                os.makedirs(self.__save_path)

            # Prepare the config dictionary
            config = {"game_mode": "synchronous",
                      "fixed_maze": self.__maze.as_dict(),
                      "fixed_cheese": self.__initial_game_state.cheese}
            
            # Create a description of the players
            player_descriptions = []
            for player in self.__players:
                player_descriptions.append({"name": player.name,
                                            "skin": player.skin,
                                            "team": [team for team in self.__initial_game_state.teams if player.name in self.__initial_game_state.teams[team]][0],
                                            "location": self.__initial_game_state.player_locations[player.name],
                                            "actions": self.__actions_history[player.name]})

            # Create the players' file, forcing players to their initial locations
            output_file_name = os.path.join(self.__save_path, datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S_%f.py"))
            with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), "save_template.py"), "r") as save_template_file:
                save_template = save_template_file.read()
                save_template = save_template.replace("{PLAYERS}", str(player_descriptions).replace("}, ", "},\n                           "))
                save_template = save_template.replace("{CONFIG}", str(config).replace(", '", ",\n              '"))
                with open(output_file_name, "w") as output_file:
                    print(save_template, file=output_file)

        # Apply ending actions of the rendering engine
        self.__rendering_engine.end()
        
    #############################################################################################################################################

    def __determine_new_game_state ( self:       Self,
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

        # Debug
        assert isinstance(game_state, GameState) # Type check for game_state
        assert isinstance(actions, dict) # Type check for actions
        assert all(player_name in [player.name for player in self.__players] for player_name in actions) # Type check for actions
        assert all(action in Maze.possible_actions for action in actions.values()) # All actions are valid

        # Initialize new game state
        new_game_state = copy.deepcopy(game_state)
        new_game_state.turn += 1

        # Move all players accordingly
        for player in self.__players:
            row, col = self.__maze.i_to_rc(game_state.player_locations[player.name])
            target = None
            if actions[player.name] == "north" and row > 0:
                target = self.__maze.rc_to_i(row - 1, col)
            elif actions[player.name] == "south" and row < self.__maze.height - 1:
                target = self.__maze.rc_to_i(row + 1, col)
            elif actions[player.name] == "west" and col > 0:
                target = self.__maze.rc_to_i(row, col - 1)
            elif actions[player.name] == "east" and col < self.__maze.width - 1:
                target = self.__maze.rc_to_i(row, col + 1)
            if target is not None and target in self.__maze.get_neighbors(game_state.player_locations[player.name]):
                weight = self.__maze.get_weight(game_state.player_locations[player.name], target)
                if weight == 1:
                    new_game_state.player_locations[player.name] = target
                elif weight > 1:
                    new_game_state.muds[player.name]["target"] = target
                    new_game_state.muds[player.name]["count"] = weight

        # All players in mud advance a bit
        for player in self.__players:
            if new_game_state.is_in_mud(player.name):
                new_game_state.muds[player.name]["count"] -= 1
                if new_game_state.muds[player.name]["count"] == 0:
                    new_game_state.player_locations[player.name] = new_game_state.muds[player.name]["target"]
                    new_game_state.muds[player.name]["target"] = None

        # Update cheese and scores
        for c in game_state.cheese:
            players_on_cheese = [player for player in self.__players if c == new_game_state.player_locations[player.name]]
            for player_on_cheese in players_on_cheese:
                new_game_state.score_per_player[player_on_cheese.name] += 1.0 / len(players_on_cheese)
            if len(players_on_cheese) > 0:
                new_game_state.cheese.remove(c)
        
        # Store trace for GUI
        for player in self.__players:
            self.__player_traces[player.name].append(new_game_state.player_locations[player.name])
            self.__player_traces[player.name] = self.__player_traces[player.name][-self.__trace_length:]
        
        # Return new game state
        return new_game_state
        
    #############################################################################################################################################

    def __distribute_cheese ( self:            Self,
                              available_cells: List[Integral],
                            ) ->               List[Integral]:
        
        """
            Distributes pieces of cheese in the maze, according to the provided criteria.
            If a fixed list of cheese was provided, it is used.
            Otherwise, the cheese is distributed randomly.
            In:
                * self:            Reference to the current object.
                * available_cells: List of indices of cells that can be used to place cheese.
            Out:
                * cheese: List of indices of cells containing cheese.
        """
        
        # Debug
        assert isinstance(available_cells, list) # Type check for available_cells
        assert all([isinstance(cell, Integral) for cell in available_cells]) # Type check for available_cells
        assert all([self.__maze.i_exists(cell) for cell in available_cells]) # Type check for available_cells

        # If we ask for a fixed list of cheese, we use it
        if self.__fixed_cheese is not None:
            
            # Debug
            assert isinstance(self.__fixed_cheese, list) # Type check for fixed_cheese
            assert all([isinstance(cell, Integral) for cell in self.__fixed_cheese]) # Type check for fixed_cheese
            assert len(set(self.__fixed_cheese)) == len(self.__fixed_cheese) # Only distinct cheese
            assert len(available_cells) >= len(self.__fixed_cheese) # Enough space for cheese
            assert all([self.__maze.i_exists(cell) for cell in self.__fixed_cheese]) # Only on existing cells
            assert all([cell in available_cells for cell in self.__fixed_cheese]) # Only on available cells

            # Place the cheese
            cheese = copy.deepcopy(self.__fixed_cheese)

        # Otherwise, we place the cheese randomly
        else:
            
            # Debug
            assert isinstance(self.__nb_cheese, Integral) # Type check for nb_cheese
            assert self.__nb_cheese > 0 # At least one cheese
            assert len(available_cells) >= self.__nb_cheese # Enough space for cheese

            # Set random seed
            nprandom.seed(self.__game_random_seed_cheese)

            # Place the cheese randomly
            nprandom.shuffle(available_cells)
            cheese = available_cells[:self.__nb_cheese]

        # Return the cheese
        return cheese

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def _player_process_function ( player:                  Player,
                               maze:                    Maze,
                               input_queue:             Optional[multiprocessing.Queue] = None,
                               output_queue:            Optional[multiprocessing.Queue] = None,
                               turn_start_synchronizer: Optional[multiprocessing.Barrier] = None,
                               turn_timeout_lock:       Optional[multiprocessing.Lock] = None,
                               turn_end_synchronizer:   Optional[multiprocessing.Barrier] = None,
                               game_state:              Optional[GameState] = None,
                               final_stats:             Optional[Dict[str, Any]] = None,
                             ) ->                       Tuple[str, Optional[float]]:
    
    """
        This function is executed in a separate process per player.
        It handles the communication with the player and calls the functions given as arguments.
        It is defined outside of the class due to multiprocessing limitations.
        If not using multiprocessing, the function returns the action and the duration of the turn.
        In:
            * player:                  Player controlled by the process.
            * maze:                    Maze in which the player plays.
            * input_queue:             Queue to receive the game state (set is multiprocessing).
            * output_queue:            Queue to send the action (set is multiprocessing).
            * turn_start_synchronizer: Barrier to synchronize the start of the turn (set is multiprocessing).
            * turn_timeout_lock:       Lock to synchronize the timeout of the turn (set is multiprocessing).
            * turn_end_synchronizer:   Barrier to synchronize the end of the turn (set is multiprocessing).
            * game_state:              Initial game state (set is sequential).
            * final_stats:             Final stats (set is sequential).
        Out:
            * action:   Action performed by the player.
            * duration: Duration of the turn.
    """

    # Debug
    assert isinstance(player, Player) # Type check for player
    assert isinstance(maze, Maze) # Type check for maze
    assert isinstance(input_queue, (mpmanagers.BaseProxy, type(None))) # Type check for input_queue
    assert isinstance(output_queue, (mpmanagers.BaseProxy, type(None))) # Type check for output_queue
    assert isinstance(turn_start_synchronizer, (mpmanagers.BarrierProxy, type(None))) # Type check for turn_start_synchronizer
    assert isinstance(turn_timeout_lock, (mpmanagers.AcquirerProxy, type(None))) # Type check for turn_timeout_lock
    assert isinstance(turn_end_synchronizer, (mpmanagers.BarrierProxy, type(None))) # Type check for turn_end_synchronizer
    assert isinstance(game_state, (GameState, type(None))) # Type check for game_state
    assert isinstance(final_stats, (dict, type(None))) # Type check for final_stats
    assert final_stats is None or all(isinstance(key, str) for key in final_stats) # Type check for final_stats
    assert (input_queue is None and output_queue is None and turn_start_synchronizer is None and turn_timeout_lock is None and turn_end_synchronizer is None) ^ (game_state is None and final_stats is None) # Either multiprocessing or sequential
    
    # We catch exceptions that may happen during the game
    use_multiprocessing = input_queue is not None
    try:

        # Main loop
        while True:
            
            # In multiprocessing, wait for all players ready
            if use_multiprocessing:
                turn_start_synchronizer.wait()
                game_state, final_stats = input_queue.get()
            
            # Call the correct function
            duration = None
            try:
                
                # Call postprocessing once the game is over
                if final_stats:
                    action = "postprocessing_error"
                    player.postprocessing(maze, game_state, final_stats)
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
                        player.preprocessing(maze, game_state)
                        action = "preprocessing"
                    else:
                        action = "error"
                        a = player.turn(maze, game_state)
                        if a not in Maze.possible_actions:
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
            if use_multiprocessing:
                with turn_timeout_lock:
                    output_queue.put((action, duration))
                turn_end_synchronizer.wait()
                if action.startswith("postprocessing"):
                    break
            else:
                return action, duration

    # Ignore
    except:
        pass

    # Default return
    return "error", None

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
