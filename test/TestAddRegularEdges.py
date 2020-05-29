'''
Tests for Graph.add_regular_edges  

Created on 2020-05-12
@author: Juan Marchionatto
'''
import unittest

import Graph as G


class Test(unittest.TestCase):

    def test_add_regular_edges(self):
        a = G.Vertex('a')
        b = G.Vertex('b')
        c = G.Vertex('c')
        
        # check exceptions first
        g = G.Graph([a, b, c], [])
        self.assertRaises(ValueError, g.add_regular_edges, 3)
        self.assertRaises(ValueError, g.add_regular_edges, 1)

        # now check all cases of all sizes in range 
        for size in range(3, 11):
            self.check_for_size(size)
        

    def check_for_size(self, size):
        if size % 2 == 0:
            for n in range(1, size-1):
                g = self.makeGraph(size)
                g.add_regular_edges(n)
                regEdgesQ = self.check_regular_edges(g)
                assert regEdgesQ == n, ("testing for size: %r and degree: %r, "
                    "each node had %r edges instead of %r") % (size, n, regEdgesQ, n)
        else:
            idxs = [n * 2 for n in range(1, int((size-1)/2))]
            for n in idxs:
                g = self.makeGraph(size)
                g.add_regular_edges(n)
                regEdgesQ = self.check_regular_edges(g)
                assert regEdgesQ == n, ("testing for size: %r and degree: %r, "
                    "each node had %r edges instead of %r") % (size, n, regEdgesQ, n)
            
                
    def makeGraph(self, size):
        gLabels = ['{0}'.format(n) for n in range(0, size)]
        return G.Graph(gLabels, [])   
    
    
    def check_regular_edges(self, g):
        '''checks that all nodes has same number of vertices and returns that number'''
        if len(g.vertices()) == 0:
            return 0
       
        edgeLenMap = {}
        for v in g.vertices():
            edgeLenMap[v] = len(g.out_edges(v))
        
        commonLen = -1                   
        for eLen in edgeLenMap.values():
            if commonLen == -1: 
                commonLen = eLen
            else:
                if commonLen != eLen:
                    raise ValueError('Not all nodes have same qty of edges: ', g)
        return commonLen


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
