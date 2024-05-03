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
import random
import sys

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
        self.__adjacency[self.nb_vertices() - 1] = {}
        
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
        assert not self.has_edge(vertex_1, vertex_2) # Edge does not already exist
        assert not (symmetric and self.has_edge(vertex_2, vertex_1)) # Symmetric edge does not already exist if asked

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
        assert self.has_edge(vertex_1, vertex_2) # Edge exists

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
        adjacency_matrix = numpy.zeros((self.nb_vertices(), self.nb_vertices()), dtype=int)
        for i, vertex1 in enumerate(self.vertices):
            for j, vertex2 in enumerate(self.vertices):
                if self.has_edge(vertex1, vertex2):
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
        adjacency_matrix = torch.zeros((self.nb_vertices(), self.nb_vertices()), dtype=int)
        for i, vertex1 in enumerate(self.vertices):
            for j, vertex2 in enumerate(self.vertices):
                if self.has_edge(vertex1, vertex2):
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
            symmetric = self.has_edge(neighbor, vertex)
            self.remove_edge(vertex, neighbor, symmetric=symmetric)
        
        # Remove the vertex and reindex the adjacency matrix
        index = self.vertices.index(vertex)
        for i in range(self.nb_vertices() - 1):
            self.__adjacency[i] = {key if key < index else key - 1 : value for key, value in self.__adjacency[i + 1 if i >= index else i].items()}
        del self.__adjacency[self.nb_vertices() - 1]
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
        assert self.has_edge(vertex_1, vertex_2) # Edge exists
        assert (not symmetric) or (symmetric and self.has_edge(vertex_2, vertex_1)) # If symmetric, the edge exists

        # Remove edge
        del self.__adjacency[self.vertices.index(vertex_1)][self.vertices.index(vertex_2)]

        # Remove symmetric edge
        if symmetric:
            del self.__adjacency[self.vertices.index(vertex_2)][self.vertices.index(vertex_1)]

    #############################################################################################################################################

    def is_connected ( self: Self,
                     ) ->    bool:

        """
            Checks whether the graph is connected.
            Uses a depth-first search.
            In:
                * self: Reference to the current object.
            Out:
                * connected: Whether the graph is connected.
        """
        
        # Debug
        assert self.nb_vertices() > 0 # The graph has at least one vertex

        # Create a list of visited vertices
        visited = [True] + [False] * (self.nb_vertices() - 1)
        stack = [0]
        
        # Depth-first search
        while stack:
            vertex = stack.pop()
            for neighbor in self.get_neighbors(self.vertices[vertex]):
                index = self.vertices.index(neighbor)
                if not visited[index]:
                    visited[index] = True
                    stack.append(index)
        
        # Check if all vertices have been visited
        connected = all(visited)
        return connected

    #############################################################################################################################################

    def minimum_spanning_tree ( self:        Self,
                                random_seed: Optional[Integral] = None
                              ) ->           Self:

        """
            Returns the minimum spanning tree of the graph.
            In:
                * self: Reference to the current object.
                * random_seed: Seed for the random number generator.
            Out:
                * minimum_spanning_tree: Graph representing the minimum spanning tree.
        """
        
        # Debug
        assert random_seed is None or isinstance(random_seed, Integral) # Type check for random_seed
        assert random_seed is None or 0 <= random_seed < sys.maxsize # random_seed is a valid seed

        # Initialize a random number generator
        rng = random.Random(random_seed)

        # Shuffle vertices
        vertices_to_add = self.vertices
        rng.shuffle(vertices_to_add)

        # Create the minimum spanning tree, initialized with a random vertex
        mst = Graph()
        vertex = vertices_to_add.pop(0)
        mst.add_vertex(vertex)
        
        # Add vertices until all are included
        while vertices_to_add:
            vertex = vertices_to_add.pop(0)
            neighbors = self.get_neighbors(vertex)
            rng.shuffle(neighbors)
            neighbors_in_mst = [neighbor for neighbor in neighbors if neighbor in mst.vertices]
            if neighbors_in_mst:
                neighbor = neighbors_in_mst[0]
                symmetric = self.has_edge(neighbor, vertex)
                weight = self.get_weight(neighbor, vertex)
                mst.add_vertex(vertex)
                mst.add_edge(vertex, neighbor, weight, symmetric)
            else:
                vertices_to_add.append(vertex)

        # Return the minimum spanning tree
        return mst

    #############################################################################################################################################

    def nb_vertices ( self: Self,
                    ) ->    Integral:

        """
            Returns the number of vertices in the graph.
            In:
                * self: Reference to the current object.
            Out:
                * nb_vertices: Number of vertices in the graph.
        """
        
        # Get the number of vertices
        nb_vertices = len(self.vertices)
        return nb_vertices

    #############################################################################################################################################

    def nb_edges ( self: Self,
                 ) ->    Integral:
    
        """
            Returns the number of edges in the graph.
            Symmetric edges are counted once.
            In:
                * self: Reference to the current object.
            Out:
                * nb_edges: Number of edges in the graph.
        """
        
        # Get the number of edges
        nb_edges = len(self.get_edge_list())
        return nb_edges

    #############################################################################################################################################

    def get_edge_list ( self: Self,
                      ) ->    List[Tuple[Any, Any]]:

        """
            Returns the list of edges in the graph.
            Symmetric edges are counted once.
            In:
                * self: Reference to the current object.
            Out:
                * edge_list: List of edges in the graph, as tuples (vertex_1, vertex_2).
        """
        
        # Get the list of edges
        edge_list = []
        for i, vertex in enumerate(self.vertices):
            for neighbor in self.get_neighbors(vertex):
                if i < self.vertices.index(neighbor):
                    edge_list.append((vertex, neighbor))
        return edge_list

    #############################################################################################################################################

    def has_edge ( self:      Self,
                   vertex_1:  Any,
                   vertex_2:  Any,
                 ) ->         bool:
        
        """
            Checks whether an edge exists between two vertices.
            In:
                * self:     Reference to the current object.
                * vertex_1: First vertex.
                * vertex_2: Second vertex.
            Out:
                * edge_exists: Whether an edge exists between the two vertices.
        """

        # Debug
        assert vertex_1 in self.vertices # Vertex 1 is in the graph
        assert vertex_2 in self.vertices # Vertex 2 is in the graph

        # Check whether the edge exists
        edge_exists = vertex_2 in self.get_neighbors(vertex_1)
        return edge_exists

    #############################################################################################################################################


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
        for vertex_1, vertex_2, weight, symmetric in self.get_edge_list():
            string += "|  |  {} {} ({}) --> {}\n".format(vertex_1, "<--" if symmetric else "---", weight, vertex_2)
        return string.strip()

#####################################################################################################################################################
#####################################################################################################################################################
