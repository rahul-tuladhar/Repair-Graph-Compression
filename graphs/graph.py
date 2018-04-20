import random
import uuid


class Graph(object):

    # TODO: Graph needs it's own unique ID, it will inject to every node as it gets added
    # then stable sort by each graph uuid, then sort by each node uuid so nodes in the same graph will be closer,
    # needed for compression algorithm

    # TODO: rather than checking if everything in in list_nodes, check n.graph_id == self.graph_id
    # this doesn't actually show if node is CURRENTLY in graph though,
    # as it could have been deleted and still have the same uid

    def __init__(self):
        self.list_nodes = list()
        self.graph_id = uuid.uuid4()

    def add_edge(self, n1, n2):  # TODO: changed params here, notify group
        """
        n2 is added to n1's adj list by calling Node.add_edge()
        n1 must be/will be a node in the graph (1st param), if it isn't, it's added to the graph
        n2 can be in graph, doesn't have to be (add_node not called), must be not equal to n1
        add additional rules for new graph implementations
        """
        # This is an unfair policy for n1 and n2.
        # N1 has to be in the graph, and then n2 is added to n1's list
        # if you wanted n2 to remain outside the graph and to have n1 added to n1's list,
        # that's not possible here and so this function is unfair.
        if n1.graph_id != self.graph_id:  # check if n1 not in graph
            self.add_node(n1)

        if n1 != n2:  # prevent looping edges, nodes that refer to themselves
            if n1.edges.count(n2) < 1:  # prevent duplicates
                n1.add_edge(
                    n2
                )  # n2 is appended to n1's list, not vice versa, directed graph

    def delete_edge(self, n1, n2):
        """
        n2 is removed from n1's adj list by calling Node.delete_edge()
        One node must be in graph, the other doesn't have to be (so can remove edges between graphs)
        """
        if n1.graph_id == self.graph_id or n2.graph_id == self.graph_id:  # if either in graph, try deleting
            # TODO: need to add removing duplicates
            while n1.edges.count(
                    n2) != 0:  # remove n as many times as it appears in edges
                try:
                    n1.delete_edge(
                        n2
                    )  # List.remove() throws ValueError if remove non existing
            # n2.delete_edge(n1) our's is a directed graph, must call delete_edge 2x if want no connections at all
            # n1.edges.remove(n4) param is n4, aka n1.delete_edge(n4)
                except ValueError:
                    raise ValueError(
                        "Tried to remove a node that isn't present")
        else:
            raise ValueError(
                'Both Nodes not in graph, cannot delete edge from this graph')

    def delete_node(self, n):
        """removes the node from the graph,
        clears the adj list therein,
        resets the node.graph_id = None,
        and removes external references to the node"""

        if n.graph_id == self.graph_id:

            # the node and it's list of edges is deleted
            n.edges = []  # clear the adj list
            self.list_nodes.remove(n)  # delete the node, error if nonexistent
            # TODO: test for this error
            n.graph_id = None  # reset uid to reflect outside the graph

            # every outside reference to the node is deleted - costly
            for x in range(len(self.list_nodes)):  # for all other nodes
                self.list_nodes[x].delete_edge(
                    n)  # delete_edge should remove duplicates
                # so all instances of n should be removed from x's adj list
            # TODO: test this, if works, change other graph classes

        else:
            raise ValueError('Node not in graph, cannot delete node')

    def add_node(self, n):
        """
        Adds a node to the Graph data structures, but it won't be connected by any edge.
        Duplicate nodes fail silently.
        New implementations should redefine this function.
        """
        if n not in self.list_nodes:  # prevent from adding >1x
            n.graph_id = self.graph_id
            self.list_nodes.append(n)

    def __str__(self):
        """ Prints out graphs in a nice format """
        formatted = " "

        for node in self.list_nodes:
            formatted += str(node) + "\n"
            for adj_node in node.edges:
                formatted += "\t" + str(adj_node) + "\n"

        return formatted

    def __eq__(self, other):
        """ compares two graphs for equality

        @warning can be very slow. Don't compare two graphs unless in a test setting

        Two graphs are considered equal iff they have the same exact nodes, in the same
        exactly positions. The ordering of nodes makes a difference to our algorithms
        so graphs w/ the same nodes in different positions within the lists
        should be considered different. """

        # type check
        if not isinstance(other, Graph):
            return False

        # check for number of nodes
        if len(self.list_nodes) != len(other.list_nodes):
            return False

        for node_index, node1 in enumerate(self.list_nodes):

            node2 = other.list_nodes[node_index]

            # check ids of "parent nodes"
            if node1.uid != node2.uid:
                return False

            # check ids of out going nodes
            for edge_index, edge1 in enumerate(node1.edges):
                edge2 = node2.edges[edge_index]

                if edge1.uid != edge2.uid:
                    return False

        # they must be equal
        return True


class Cluster(Graph):
    # apparently we're not using this class anymore...
    # ONLY one cluster at a time in our system (otherwise more uid's)
    def add_graph(self, g):
        """
        Takes a random node from both graphs and calls addEdge, returns the list of nodes
        """
        node1 = random.choice(self.list_nodes)
        node2 = random.choice(g.list_nodes)
        self.add_edge(node1, node2)

    def add_graph_by_node(self, n):
        """
        Like add_graph, but allows specification of one of the nodes (the param node).
        Randomly selects one internal node, calls add_edge on the param node,
        which doesn't have to be in the cluster/graph (param node could be external)
        """
        rand_node = random.choice(self.list_nodes)
        self.add_edge(n, rand_node)
