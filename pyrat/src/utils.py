#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains a few functions that can be useful in general.
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
import shutil
import inspect
import cProfile
import pyprof2calltree
import pdoc
import pathlib
import sys

#####################################################################################################################################################
##################################################################### FUNCTIONS #####################################################################
#####################################################################################################################################################

def create_workspace ( target_directory: str
                     ) ->                None:

    """
        Creates all the directories for a clean student workspace.
        Also creates a few default programs to start with.
        In:
            * target_directory: The directory in which to create the workspace.
        Out:
            * None.
    """

    # Debug
    assert isinstance(target_directory, str) # Type check for target_directory

    # Copy the template workspace into the current directory if not already existing
    source_workspace = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "workspace")
    target_workspace = os.path.join(target_directory, "pyrat_workspace")
    shutil.copytree(source_workspace, target_workspace, ignore=shutil.ignore_patterns('__pycache__'))

#####################################################################################################################################################

def generate_documentation ( workspace_directory: str
                           ) ->                   None:

    """
        Generates the documentation for the project.
        The function will parse the PyRat library, and all the subdirectories of the workspace directory.
        This will create a doc directory in the workspace directory, and fill it with the documentation.
        In:
            * workspace_directory: The directory in which the workspace is located.
        Out:
            * None.
    """
    
    # Debug
    assert isinstance(workspace_directory, str) # Type check for workspace_directory

    # Process paths
    target_directory = pathlib.Path(os.path.join(workspace_directory, "doc"))
    workspace_subdirectories = [os.path.join(workspace_directory, directory) for directory in os.listdir(workspace_directory) if directory != "doc"]
    for d in workspace_subdirectories:
        sys.path.append(d)
    
    # Generate the documentation for PyRat, and for workspace subdirectories
    pdoc.render.configure(docformat="google")
    pdoc.pdoc("pyrat", *workspace_subdirectories, output_directory=target_directory)

#####################################################################################################################################################

def caller_file () -> str:

    """
        Returns the name of the file from which the caller of this function was called.
        In:
            * None.
        Out:
            * caller: The name of the file from which the caller of this function was called.
    """

    # Check stack to get the name
    caller = inspect.currentframe().f_back.f_back.f_code.co_filename
    return caller

#####################################################################################################################################################

def start_profiling () -> None:

    """
        Function to start profiling the code.
        In:
            * None.
        Out:
            * None.
    """
    
    # Create global object
    global profiler
    profiler = cProfile.Profile()
    profiler.enable()

#####################################################################################################################################################

def stop_profiling () -> None:

    """
        Function to call after the code blocks to profile.
        It will open a window with the profiling results.
        In:
            * None.
        Out:
            * None.
    """
    
    # Debug
    assert "profiler" in globals() # Profiling must have been started

    # Get stats and visualize
    global profiler
    profiler.create_stats()
    pyprof2calltree.visualize(profiler.getstats())

#####################################################################################################################################################
#####################################################################################################################################################