#####################################################################################################################################################
######################################################################## INFO #######################################################################
#####################################################################################################################################################

"""
    This file contains useful elements to define a graph.
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

class Graph ():

    """
        A graph is a mathematical structure that models pairwise relations between objects.
        It consists of a set of vertices and a set of edges.
        It is implemented using an adjacency dictionary.
        The keys of the dictionary are the vertices of the graph.
        The values of the dictionary are dictionaries themselves.
        The keys of these dictionaries are the neighbors of the corresponding vertex.
        The values of these dictionaries are the weights of the corresponding edges.
        It should be manipulated using the methods defined below and not directly.
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

        # Private attributes
        self.__vertices = []
        self.__adjacency = {}

    #############################################################################################################################################
    #                                                                  GETTERS                                                                  #
    #############################################################################################################################################

    @property
    def vertices ( self: Self
                 ) ->    List[Any]:
        
        """
            Getter for __vertices.
            It returns a copy of the attribute to avoid unwanted modifications.
            In:
                * self: Reference to the current object.
            Out:
                * vertices_copy: A copy of __vertices.
        """

        # Return a copy of the attribute
        vertices_copy = self.__vertices.copy()
        return vertices_copy

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def add_vertex ( self:   Self,
                     vertex: Any
                   ) ->      None:

        """
            Adds a vertex to the graph.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to add.
            Out:
                * None.
        """
        
        # Debug
        assert vertex not in self.vertices # Vertex is not already in the graph

        # Add vertex to the list of vertices and create an entry in the adjacency matrix
        self.__vertices.append(vertex)
        self.__adjacency[len(self.vertices) - 1] = {}
        
    #############################################################################################################################################

    def add_edge ( self:      Self,
                   vertex_1:  Any,
                   vertex_2:  Any,
                   weight:    Number = 1,
                   symmetric: bool = False
                 ) ->         None:

        """
            Adds an edge to the graph.
            By default, it is unweighted, encoded using a weight of 1.0.
            The edge can be directed or not.
            In:
                * self:      Reference to the current object.
                * vertex_1:  First vertex.
                * vertex_2:  Second vertex.
                * weight:    Weight of the edge.
                * symmetric: Whether the edge is symmetric.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(weight, Number) # Type check for weight
        assert isinstance(symmetric, bool) # Type check for symmetric
        assert vertex_1 in self.vertices # Vertex 1 is in the graph
        assert vertex_2 in self.vertices # Vertex 2 is in the graph
        assert vertex_2 not in self.get_neighbors(vertex_1) # Edge does not already exist
        assert not (symmetric and vertex_1 in self.get_neighbors(vertex_2)) # Symmetric edge does not already exist if asked

        # Add edge to the adjacency dictionary
        self.__adjacency[self.vertices.index(vertex_1)][self.vertices.index(vertex_2)] = weight
        if symmetric:
            self.__adjacency[self.vertices.index(vertex_2)][self.vertices.index(vertex_1)] = weight
    
    #############################################################################################################################################

    def get_neighbors ( self:   Self,
                        vertex: Any
                      ) ->      List[Any]:

        """
            Returns the list of neighbors of a vertex.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex of which to get neighbors.
            Out:
                * neighbors: List of neighbors of the vertex.
        """
        
        # Debug
        assert vertex in self.vertices # Vertex is in the graph

        # Get neighbors
        neighbors = [self.vertices[i] for i in self.__adjacency[self.vertices.index(vertex)]]
        return neighbors

    #############################################################################################################################################

    def get_weight ( self:     Self,
                     vertex_1: Any,
                     vertex_2: Any
                   ) ->        Number:

        """
            Returns the weight of an edge.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * weight: Weight of the edge.
        """
        
        # Debug
        assert vertex_1 in self.vertices # Vertex 1 is in the graph
        assert vertex_2 in self.vertices # Vertex 2 is in the graph
        assert vertex_2 in self.get_neighbors(vertex_1) # Edge exists

        # Get weight
        weight = self.__adjacency[self.vertices.index(vertex_1)][self.vertices.index(vertex_2)]
        return weight

    #############################################################################################################################################

    def add_vertex ( self:   Self,
                     vertex: Any
                   ) ->      None:

        """
            Adds a vertex to the graph.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to add.
            Out:
                * None.
        """
        
        # Debug
        assert vertex not in self.vertices # Vertex is not already in the graph

        # Add vertex to the list of vertices and create an entry in the adjacency matrix
        self.__vertices.append(vertex)
        self.__adjacency[len(self.vertices) - 1] = {}
        
    #############################################################################################################################################

    def as_dict ( self: Self,
                ) ->    Dict[Any, Dict[Any, Number]]:

        """
            Returns a dictionary representing the adjacency matrix.
            Useful for exporting the maze when saving the game.
            The vertices must be hashable objects.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_dict: Dictionary representing the adjacency matrix.
        """
        
        # Debug
        assert all([isinstance(vertex, Hashable) for vertex in self.vertices]) # Vertices are hashable

        # Transform in a dictionary
        adjacency_dict = {vertex : {neighbor : self.get_weight(vertex, neighbor) for neighbor in self.get_neighbors(vertex)} for vertex in self.vertices}
        return adjacency_dict
        
#####################################################################################################################################################
#####################################################################################################################################################
