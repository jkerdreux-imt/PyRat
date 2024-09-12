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
import shutil
import inspect
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
    root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..")
    source_workspace = os.path.join(root, "pyratws")
    source_wstoml = os.path.join(root, "pyratws.toml")
    target_workspace = os.path.join(target_directory, "pyratws")
    target_wstoml = os.path.join(target_directory, "pyproject.toml")
    shutil.copytree(source_workspace, target_workspace, ignore=shutil.ignore_patterns('__pycache__'))
    shutil.copy(source_wstoml, target_wstoml)

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

def pyrat_files () -> List[str]:

    """
        Returns the list of all the files in the PyRat library.
        In:
            * None.
        Out:
            * files: The list of all the files in the PyRat library.
    """

    # Get the list of all the files in the PyRat library
    pyrat_path = os.path.dirname(os.path.realpath(__file__))
    files = [os.path.join(pyrat_path, file) for file in os.listdir(pyrat_path) if file.endswith(".py")]
    return files

#####################################################################################################################################################
#####################################################################################################################################################
