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
import numpy
import torch

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
            It returns a copy of the list of vertices.
            In:
                * self: Reference to the current object.
            Out:
                * vertices_copy: A copy of __vertices.
        """

        # Return a copy of the list of vertices
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

    def as_dict ( self: Self,
                ) ->    Dict[Any, Dict[Any, Number]]:

        """
            Returns a dictionary representing the adjacency matrix.
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
        
    #############################################################################################################################################

    def as_numpy_ndarray ( self: Self,
                         ) ->    numpy.ndarray:

        """
            Returns a numpy ndarray representing the graph.
            Entries are given in order of the vertices.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Numpy ndarray representing the adjacency matrix.
        """
        
        # Create the adjacency matrix
        adjacency_matrix = numpy.zeros((len(self.vertices), len(self.vertices)), dtype=int)
        for i, vertex1 in enumerate(self.vertices):
            for j, vertex2 in enumerate(self.vertices):
                if vertex2 in self.get_neighbors(vertex1):
                    adjacency_matrix[i, j] = self.get_weight(vertex1, vertex2)
        return adjacency_matrix

    #############################################################################################################################################

    def as_torch_tensor ( self: Self,
                        ) ->    torch.Tensor:

        """
            Returns a torch tensor representing the maze.
            Entries are given in order of the vertices.
            In:
                * self: Reference to the current object.
            Out:
                * adjacency_matrix: Torch tensor representing the adjacency matrix.
        """
        
        # Create the adjacency matrix
        adjacency_matrix = torch.zeros((len(self.vertices), len(self.vertices)), dtype=int)
        for i, vertex1 in enumerate(self.vertices):
            for j, vertex2 in enumerate(self.vertices):
                if vertex2 in self.get_neighbors(vertex1):
                    adjacency_matrix[i, j] = self.get_weight(vertex1, vertex2)
        return adjacency_matrix

    #############################################################################################################################################

    def remove_vertex ( self:   Self,
                        vertex: Any
                      ) ->      None:

        """
            Removes a vertex from the graph.
            Also removes all edges connected to this vertex.
            In:
                * self:   Reference to the current object.
                * vertex: Vertex to remove.
            Out:
                * None.
        """
        
        # Debug
        assert vertex in self.vertices # Vertex is in the graph

        # Remove connections to the vertex
        for neighbor in self.get_neighbors(vertex):
            symmetric = vertex in self.get_neighbors(neighbor)
            self.remove_edge(vertex, neighbor, symmetric=symmetric)
        
        # Remove the vertex and reindex the adjacency matrix
        index = self.vertices.index(vertex)
        for i in range(len(self.vertices) - 1):
            self.__adjacency[i] = {key if key < index else key - 1 : value for key, value in self.__adjacency[i + 1 if i >= index else i].items()}
        del self.__adjacency[len(self.vertices) - 1]
        del self.__vertices[index]
        
    #############################################################################################################################################

    def remove_edge ( self:      Self,
                      vertex_1:  Any,
                      vertex_2:  Any,
                      symmetric: bool = False
                    ) ->         None:

        """
            Removes an edge from the graph.
            In:
                * self:      Reference to the current object.
                * vertex_1:  First vertex.
                * vertex_2:  Second vertex.
                * symmetric: Also delete the symmetric edge.
            Out:
                * None.
        """
        
        # Debug
        assert isinstance(symmetric, bool) # Type check for symmetric
        assert vertex_1 in self.vertices # Vertex 1 is in the graph
        assert vertex_2 in self.vertices # Vertex 2 is in the graph
        assert vertex_2 in self.get_neighbors(vertex_1) # Edge exists
        assert (not symmetric) or (symmetric and vertex_1 in self.get_neighbors(vertex_2)) # If symmetric, the edge exists

        # Remove edge
        del self.__adjacency[self.vertices.index(vertex_1)][self.vertices.index(vertex_2)]

        # Remove symmetric edge
        if symmetric:
            del self.__adjacency[self.vertices.index(vertex_2)][self.vertices.index(vertex_1)]

    #############################################################################################################################################
    #                                                              PRIVATE METHODS                                                              #
    #############################################################################################################################################

    def __str__ ( self: Self,
                ) ->    str:

        """
            This method returns a string representation of the object.
            In:
                * self: Reference to the current object.
            Out:
                * string: String representation of the object.
        """
        
        # Create the string
        string = "Graph object:\n"
        string += "|  Vertices: " + str(self.vertices) + "\n"
        string += "|  Adjacency matrix:\n"
        for vertex in self.vertices:
            for neighbor in self.get_neighbors(vertex):
                if self.vertices.index(neighbor) > self.vertices.index(vertex):
                    symmetric = vertex in self.get_neighbors(neighbor)
                    weight = self.get_weight(vertex, neighbor)
                    string += "|  |  {} {} ({}) --> {}\n".format(vertex, "<--" if symmetric else "---", weight, neighbor)
        return string.strip()

#####################################################################################################################################################
#####################################################################################################################################################
