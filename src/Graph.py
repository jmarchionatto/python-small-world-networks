'''
Graph implementation to following Allen Downey's book 
"Think Complexity" (Version 1.1)

Created on May 11, 2020

@author: Juan Marchionatto
'''
from _ast import Pass

class Graph(dict):
    def __init__(self, vs=[], es=[]):
        """create a new graph. (vs) is a list of vertices; (es) is a list of edges."""
        for v in vs:
            self.add_vertex(v)
        for e in es:
            self.add_edge(e)

    def add_vertex(self, v):
        """add (v) to the graph"""
        self[v] = {}

    def add_edge(self, e):
        """add (e) to the graph by adding an entry in both directions.
        If there is already an edge connecting these Vertices, the
        new edge replaces it.
        """
        v, w = e
        if v == w:
            raise ValueError("No self edges accepted")
        
        self[v][w] = e
        self[w][v] = e

    def get_edge(self, vs):
        """ takes two vertices and returns the edge between them
            if it exists and None otherwise. Hint: use a try statement.
        """
        if len(vs) != 2:
            raise ValueError("vs must contain 2 vertices")

        try:
            return self[vs[0]][vs[1]]
        except KeyError:
            return None
        
    def remove_edge(self, e):
        """ takes an edge and removes all references to it from the graph"""
        
        v, w = e
        try:
            del( self[v][w] )
        except: 
            Pass
            
        try: 
            del( self[w][v] )
        except: 
            Pass
            
    def vertices(self):
        '''returns a list of the vertices in a graph'''
        return [ *self.keys() ]
    
    def edges(self):
        '''returns a list of edges in a graph'''
#         es = set();
#         for v in self.values():
#             es.update( v.values() )
#         return [ *es ]

        # converted to comprehension        
        es = set( e for v in self.values() for e in v.values() )  
        return [ *es ]

    def out_vertices(self, v):
        '''takes a Vertex and returns a list of the adjacent
            vertices (the ones connected to the given node by an edge).'''
        try:
            return list(self[v].keys()) 
        except KeyError:
            return []
    
    def out_edges(self, v): 
        '''takes a Vertex and returns a list of edges connected to it'''
        try:
            return list(self[v].values()) 
        except KeyError:
            return []
                                                
    def add_all_edges(self): 
        '''starts with an edgeless Graph and makes a complete 
            graph by adding edges between all pairs of vertices.'''
        vs = [ *self.keys() ]
        while( len(vs) != 0 ):
            v = vs.pop(0)
            for v1 in vs:
                self.add_edge( Edge(v, v1) )
            
    def add_regular_edges(self, degree):
        ''' adds edges to an edgeless graph so that every vertex 
            has the same degree. The degree of a node is the number 
            of edges it is connected to.'''
        if len( self.edges() ) > 0:
            raise ValueError("Graph has edges")

        if degree > len(self):
            raise ValueError("Can't make dgree higher than number of vertices - 1")
        
        if len(self) % 2 == 1 and degree % 2 == 1:
            raise ValueError("Can't set odd degree to a grap with odd number of vertices")
        
        if degree == len(self) - 1:
            self.add_all_edges()
        
        
        '''rule is:
            for even Vs: 
                degree even: node 0 to all nodes 1 to degree/2
                degree odd:  even rule + half Vs to node_idx+len(Vs)/2 th node
            for odd Vs: 
                degree even: to all 1-nth nodes n=degree/2
                degree odd: No  
        '''
        vs = self.vertices()
        for fromIdx in range(0, len(vs)):
            for n in range(1, int(degree/2) + 1):
                toIdx = (fromIdx + n) % len(vs)
                if fromIdx == toIdx:
                    raise ValueError("fromIdx is same as toIdx")
                self.add_edge( Edge(vs[fromIdx], vs[toIdx]) )
                
        if degree % 2 == 1:
            '''only happens for even number of nodes''' 
            halfVs = int(len(vs)/2)
            for fromIdx in range(0, halfVs):
                toIdx = fromIdx + halfVs
                if fromIdx == toIdx:
                    raise ValueError("fromIdx is same as toIdx")
                self.add_edge( Edge(vs[fromIdx], vs[toIdx]) )


    def is_regular(self):
        ''' informs if graph is regular. Returns None to indicate it is not 
            or the degree if it is regular'''
        
        # get degree of first V
        try:
            vq = len(self.out_vertices(next(iter(self))))
        except StopIteration:
            raise ValueError("Graph has no vertices")
        
        # compare with degree of the rest of the Vs
        for v in self:
            if vq != len(self.out_vertices(v)):
                return None 
        return vq


    def is_connected(self):
        '''returns True if the Graph is connected and False otherwise
            Strategy: starting by first node, we will put it in a queue,
            then, for each element in the queue, we will:
            _ remove it from the queue
            _ add it to the visited set
            _ compare the visited set with the node set. 
                If equal, graph is connected
                If not, keep on with the procedure
            _ if there are neighbour nodes: add them to the queue
                else: compare visited nodes with node set. If equal: connected
            _ loop
        '''
        allNodes = set(self)
        toVisit = [ next(iter(allNodes)) ]
        visited = set() 
        while( len(toVisit) > 0 ):
            n = toVisit.pop()
            visited.add(n)
            if allNodes == visited:
                return True
            nonVisitedAdjNodes = [ x for x in self.out_vertices(n) if x not in visited ]
            toVisit.extend( nonVisitedAdjNodes )
            
        return False
        

class Vertex(object):
    def __init__(self, label=''):
        self.label = label

    def __repr__(self):
        return 'Vertex(%s)' % repr(self.label)

    __str__ = __repr__


class Edge(tuple):
    def __new__(cls, *vs):
        return tuple.__new__(cls, vs)

    def __repr__(self):
        return 'Edge(%s, %s)' % (repr(self[0]), repr(self[1]))

    __str__ = __repr__
