import random
import Graph as G

class RandomGraph(G.Graph):
    def add_random_edges(self, p):
        '''takes a probability p and, starting with an edgeless graph, 
            adds edges at random so that the probability is p that there 
            is an edge between any two nodes.'''
        if len( self.edges() ) > 0:
            raise ValueError("Graph has edges")
        
        vs = [ *self.keys() ]
        while( len(vs) != 0 ):
            v = vs.pop(0)
            for v1 in vs:
                if random.random() < p:
                    super().add_edge( G.Edge(v, v1) )
                    
