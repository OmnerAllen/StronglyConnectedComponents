# Omner Allen and Kaden Baxter













class Graph:
    def __init__(self, nodes=None):
        #create an empty graph
        self.nodes = nodes if nodes is not None else {}
        self.dict_of_children = {}
        self.dict_of_parents = {}
        self.edge_order = []
        return

    def add_node(self, node, data=None):
        # adds a node to the graph if it isn't already present
        if node not in self.nodes:
            self.nodes[node] = data
            self.dict_of_children[node] = {}
            self.dict_of_parents[node] = {}
        return
    
    def add_edge(self, parent, child, data=None):
        # adds a directed edge from parent to child
        if parent not in self.nodes or child not in self.nodes:
            return False
        
        edgeExists = child in self.dict_of_children[parent]

        self.dict_of_children[parent][child] = data
        self.dict_of_parents[child][parent] = data

        if not edgeExists:
            self.edge_order.append((parent, child))

        return
    
    def add_undirected_edge(self, node1, node2, data=None):
        # adds an undirected edge between node1 and node2, calls add_edge twice
        self.add_edge(node1, node2, data)
        self.add_edge(node2, node1, data)
        return
    
    def get_node_data(self, node):
        # returns the data associated with the given node
        if node not in self.nodes:
            return None
        return self.nodes[node]
    
    def get_edge_data(self, parent, child):
        # returns the data associated with the edge from parent to child
        if parent not in self.nodes or child not in self.nodes or child not in self.dict_of_children[parent]:
            return None
        return self.dict_of_children[parent][child]
    
    def get_children(self, parent):
        # returns an iterable of the children of the given parent node
    
        if parent not in self.dict_of_children:
            return []
        return list(self.dict_of_children[parent].keys())
    
    def get_parents(self, node):
        # returns an iterable of the parents of the given node
        if node not in self.dict_of_parents:
            return []
        return list(self.dict_of_parents[node].keys())
    
    def contains_node(self, node):
        # returns True if the graph contains the given node, False otherwise
        if node in self.nodes:
            return True
        return False
    
    def contains_edge(self, parent, child):
        # returns True if there is an edge from parent to child, False otherwise
        if parent not in self.dict_of_children:
            return False
        if child not in self.dict_of_children[parent]:
            return False
        return True

    def get_nodes(self):
        # returns an iterable of all nodes in the graph
        return list(self.nodes.keys())
    
    def get_edges(self):
        # returns an iterable of all edges in the graph (as (parent,child) tuples)
        # edges are returned in the order they were added
        return list(self.edge_order)
    
    def swap_edge(parent, child):
        pass

    def reversed_graph(self):
        # get all nodes
        # create new graph with nodes passed in
        # add all swapped edges
        # return graph
        reversed = Graph(self.get_nodes())
        for node in reversed.get_nodes():
            children = self.dict_of_children[node]
            parents = self.dict_of_parents[node]

            for c in children:
                reversed.add_edge(c, node)
            for p in parents:
                reversed.add_edge(node, p)
        return reversed




def test_reversed_graph():
    g=Graph()
    g.add_node("one", data = "one data") #(node, data)
    g.add_node("two", data = "two data") #(node, data)

    g.add_edge("one","two", data = "added edge from one to two")

    r = g.reversed_graph()
    edges = r.get_edges()

    assert edges == [("two", "one")]
    
    