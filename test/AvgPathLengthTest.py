'''
Tests for SmallWorldGraph's averagePathLength function

Created on May 11, 2020
@author: Juancho
'''
import unittest

import Graph as G
import SmallWorldNetwork as SWN

class AvgPathLengthTest(unittest.TestCase):


    def test_path_length_1(self):
 
        g = self.makeRegGraph(1000, 10)
         
        apl = g.averagePathLength()
        assert apl == 50400 / 999


    def makeRegGraph(self, VQty, degree):
        vs = []
        for vi in range(0,VQty):
            vs.append( G.Vertex(str(vi)) )
        g = SWN.SmallWorldNetwork(vs, [])
        g.add_regular_edges(degree)
        return g



    def test_path_length(self):
        a = G.Vertex('a')
        b = G.Vertex('b')
        c = G.Vertex('c')
        d = G.Vertex('d')
 
        es = [G.Edge(a,b), G.Edge(b,d), G.Edge(c,d)]
        gr = SWN.SmallWorldNetwork([a,b,c,d], es)
         
        apl = gr.averagePathLength()
        exp = 5/3
        assert exp == apl        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
    
