class Node:
    def __init__(self, variable_dictionary={}):
        """
        Generic graph node class. Node variables are stored in self.variables
        :param variable_dictionary: Dictionary containing variable values for node
        """
        self.variables = variable_dictionary

class Edge:
    def __init__(self, nodes, variable_dictionary={}):
        """
        Generic graph edge class. Edge variables are stored in self.variables
        :param nodes: Nodes that this edge connects
        :param variable_dictionary: Dictionary containing variable values for edge
        """
        self.nodes = nodes
        self.variables = variable_dictionary

class Graph:
    def __init__(self, nodes=[], edges=[]):
        """
        Generic graph class
        :param nodes:
        :param edges:
        """

        self.nodes = nodes
        self.edges = edges

        # Node connectivity matrix
        self.node_connectivity = constructNodeConnectivityMatrix(self.edges)

        # Node - edge connectivity map
        # self.node_edge_connectivity = None

    def appendNodeToGraph(self, variable_dictionary={}):
        """
        Adds new node to graph with unique index equal to largest index + 1
        :param variable_dictionary: Dictionary containing variable values for node
        :return: Index of new node
        """
        index = len(self.nodes)
        self.nodes.append(Node(variable_dictionary))

        # if self.node_edge_connectivity == None:
        #     self.node_edge_connectivity = [[None]]
        # else:
        #     self.node_edge_connectivity.append([None])

        return index

    def appendEdgeToGraph(self, nodes, variable_dictionary={}):
        """
        Adds edge to graph with unique index equal to largest index + 1
        :param nodes: Nodes that new edge connects
        :param variable_dictionary: Dictionary containing variable values for edge
        :return: Index of new edge
        """

        # Create edge
        index = len(self.edges)
        self.edges.append(Edge(nodes, variable_dictionary))

        # Update graph connectivity matrix
        self.node_connectivity = constructNodeConnectivityMatrix(self.listEdgeNodeIndices())

        # # Update node - edge connectivity map
        # for index in range(2):
        #     if self.node_edge_connectivity[nodes[index]] == [None]:
        #         self.node_edge_connectivity[nodes[index]] = [index]
        #     else:
        #         self.node_edge_connectivity[nodes[index]].append(index)

        return index

    def listEdgeNodeIndices(self):
        """
        Constructs a list with each element containing the node indices connected by an edge
        :return: List of edge-node indices
        """
        edge_node_list = [None] * len(self.edges)
        for edge_index, edge in enumerate(self.edges):
            edge_node_list[edge_index] = edge.nodes

        return edge_node_list

    def longestContinousPath(self):
        """
        Calculates longest continuous path in graph
        :return: Length of path, List of edges which make path
        """
        # Start recursion from each node
        starting_nodes = range(len(self.nodes))

        # Recursively search through connected edges from each node in starting nodes. Store maximum combinations
        max_length = 0
        max_path = []
        for starting_node in starting_nodes:
            path = self._recursivePathLength(starting_node, [], [])

            if len(path) > max_length:
                max_length = len(path)
                max_path = path

        return max_length, max_path

    def _recursivePathLength(self, current_node, visited_edges, current_longest_path):
        """
        Recursive function to find the longest path in a graph from a node
        :param current_node: Node to search from
        :param visited_edges: List of edges which have already been visted
        :return: Max length of path, List of edges which make path
        """

        # Assemble list of connected edges
        connected_edges = []
        connected_nodes = self.node_connectivity[current_node]
        for index, node in enumerate(connected_nodes):
            if node == 1:
                connected_edges.append([current_node, index])


        # Iterate over connected edges
        for edge in connected_edges:
            if edge not in visited_edges and edge[::-1] not in visited_edges:
                # Have not already visited edge so append this edge to visited edges and call recursive function at next node
                current_longest_path = self._recursivePathLength(edge[1], visited_edges + [edge], current_longest_path)

            else:
                # Reached 'dead-end'. If current path is longer than maximum so far, record it
                if len(visited_edges) > len(current_longest_path):
                    current_longest_path = visited_edges

        return current_longest_path


def constructNodeConnectivityMatrix(edges):
    """
    Calculates Matrix of connectivity for graph given list of edges
    :param edges: List of edges in form: [[node 0, node 1], [node 0, node 1],...]
    :return: Matrix of connectivity. For element in row i, column j, a value of 1 represents a connection between node i and node j
    """

    # First get a list of nodes in graph
    nodes = []
    for edge in edges:
        for node in range(2):
            if edge[node] not in nodes:
                nodes.append(edge[node])


    # Initialise empty connectivity matrix
    connectivity_matrix = []
    for row in range(len(nodes)):
        connectivity_matrix.append([0] * len(nodes))

    # Iterate over each edge. Add edge to matrix
    for edge in edges:
        connectivity_matrix[edge[0]][edge[1]] = 1
        connectivity_matrix[edge[1]][edge[0]] = 1

    return connectivity_matrix