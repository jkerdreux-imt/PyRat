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

# External imports
from typing import *
from typing_extensions import *

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

        # Initialize graph attributes
        self.adjacency = {}

    #############################################################################################################################################
    #                                                               PUBLIC METHODS                                                              #
    #############################################################################################################################################

    def copy ( self: Self
             ) ->    Self:
        
        """
            Creates a copy of the graph.
            In:
                * self: Reference to the current object.
            Out:
                * graph_copy: Copy of the graph.
        """

        # Create the copy
        graph_copy = Graph()
        graph_copy.adjacency = self.adjacency.copy()
        return graph_copy

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
        
        # Check that vertex is not already in the graph
        if vertex in self.adjacency:
            raise ValueError("Vertex", vertex, "already in the graph.")

        # Add vertex to the adjacency dictionary
        self.adjacency[vertex] = {}
        
    #############################################################################################################################################

    def add_edge ( self:      Self,
                   vertex_1:  Any,
                   vertex_2:  Any,
                   weight:    float = 1.0,
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
        
        # Check that vertices are in the graph
        if vertex_1 not in self.adjacency:
            raise ValueError("Vertex", vertex_1, "not in the graph.")
        if vertex_2 not in self.adjacency:
            raise ValueError("Vertex", vertex_2, "not in the graph.")

        # Check that the edge is not already in the graph
        if vertex_2 in self.adjacency[vertex_1]:
            raise ValueError("Edge", vertex_1, "-", vertex_2, "already in the graph.")
        if symmetric and vertex_1 in self.adjacency[vertex_2]:
            raise ValueError("Edge", vertex_2, "-", vertex_1, "already in the graph.")

        # Add edge to the adjacency dictionary
        self.adjacency[vertex_1][vertex_2] = weight
        if symmetric:
            self.adjacency[vertex_2][vertex_1] = weight
    
    #############################################################################################################################################

    def get_vertices ( self: Self
                     ) ->    List[Any]:

        """
            Returns the list of vertices in the graph.
            In:
                * self: Reference to the current object.
            Out:
                * vertices: List of vertices in the graph.
        """
        
        # Get vertices
        vertices = list(self.adjacency.keys())
        return vertices
        
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
        
        # Check that vertex is in the graph
        if vertex not in self.adjacency:
            raise ValueError("Vertex", vertex, "not in the graph.")

        # Get neighbors
        neighbors = list(self.adjacency[vertex].keys())
        return neighbors

    #############################################################################################################################################

    def get_weight ( self:     Self,
                     vertex_1: Any,
                     vertex_2: Any
                   ) ->        List[Any]:

        """
            Returns the weight of an edge.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * weight: Weight of the edge.
        """
        
        # Check that vertices are in the graph
        if vertex_1 not in self.adjacency:
            raise ValueError("Vertex", vertex_1, "not in the graph.")
        if vertex_2 not in self.adjacency:
            raise ValueError("Vertex", vertex_2, "not in the graph.")

        # Get weight
        weight = self.adjacency[vertex_1][vertex_2]
        return weight

#####################################################################################################################################################
#####################################################################################################################################################
