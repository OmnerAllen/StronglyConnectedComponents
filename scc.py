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
        # make new graph
        # add nodes to new graph
        # add edges (reversed) to new graph
        # return graph
        reversed = Graph()
        for node in self.get_nodes():
            reversed.add_node(node, self.get_node_data(node))
        for parent, child in self.get_edges():
            reversed.add_edge(child, parent, self.get_edge_data(parent,child))

        return reversed


# DFS on reversed_graph
# returns our topo order
# optional dfs order, default is just start from one until the end


def scc(g:Graph):
    r = g.reversed_graph()
    already_searchedr = []
    already_searchedo = []
    order = []
    sccs = []
    

    def dfsr(node):
        already_searchedr.append(node)
        for child in r.get_children(node):
            if child not in already_searchedr:
                dfsr(child)
        order.append(node)
        
        
    for node in r.get_nodes():
        if node not in already_searchedr:
            dfsr(node)

    def dfso(node, component):
        already_searchedo.append(node)
        component.append(node)
        for child in g.get_children(node):
            if child not in already_searchedo:
                dfso(child, component)
        
    for node in reversed(order):
        if node not in already_searchedo:
            component = []
            dfso(node, component)
            sccs.append(frozenset(component))

    return sccs

def meta_graph(og:Graph):
    sccs = scc(og)
    meta = Graph()
    node_to_scc = {}

    for scc_set in sccs:
        for node in scc_set:
            node_to_scc[node] = scc_set

    for scc_set in reversed(sccs):
        meta.add_node(scc_set)
    
    for parent, child in og.get_edges():
        scc_parent = node_to_scc[parent]
        scc_child = node_to_scc[child]
        if scc_parent != scc_child:
            meta.add_edge(scc_parent, scc_child)

    return meta



def test_reversed_graph():
    g=Graph()
    g.add_node("one", data = "one data") #(node, data)
    g.add_node("two", data = "two data") #(node, data)

    g.add_edge("one","two", data = "added edge from one to two")

    r = g.reversed_graph()
    edges = r.get_edges()

    assert edges == [("two", "one")]
    
def test_frozensets():
    g=Graph()
    g.add_node("one")
    g.add_node("two")
    g.add_node("three")
    g.add_node("four")

    g.add_undirected_edge("one", "two")
    g.add_edge("two", "three")
    g.add_edge("four", "one")

    sccsExpected = [frozenset({"three"}), frozenset({"one", "two"}), frozenset({"four"})]
    sccsCalculated = scc(g)

    assert sccsExpected == sccsCalculated
    
def test_metagraph1():
    g=Graph()
    g.add_node("one")
    g.add_node("two")
    g.add_node("three")
    g.add_node("four")

    g.add_undirected_edge("one", "two")
    g.add_edge("two", "three")
    g.add_edge("four", "one")

    m = meta_graph(g)

    scc_four = frozenset({"four"})
    scc_onetwo = frozenset({"one", "two"})
    scc_three = frozenset({"three"})

    assert m.get_nodes() == [scc_four, scc_onetwo, scc_three]

    assert m.contains_edge(scc_four, scc_onetwo)
    assert m.contains_edge(scc_onetwo, scc_three)
    assert not m.contains_edge(scc_four, scc_three)

def test_metagraph2():
    g=Graph()
    g.add_node("one")
    g.add_node("two")
    g.add_node("three")
    g.add_node("four")
    g.add_node("five")

    g.add_undirected_edge("one", "two")
    g.add_undirected_edge("four", "five")
    g.add_edge("two", "three")
    g.add_edge("three", "four")

    m = meta_graph(g)

    scc_fourfive = frozenset({"four", "five"})
    scc_onetwo = frozenset({"one", "two"})
    scc_three = frozenset({"three"})

    assert m.get_nodes() == [scc_onetwo, scc_three, scc_fourfive]
    
    assert m.contains_edge(scc_onetwo, scc_three)
    assert m.contains_edge(scc_three, scc_fourfive)
    assert not m.contains_edge(scc_onetwo, scc_fourfive)