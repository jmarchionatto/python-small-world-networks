'''
Created on May 14, 2020

@author: Juan Marchionatto
'''
import random

from RandomGraph import RandomGraph
from Graph import Edge
import GraphWorld as GW
import itertools
import math
from collections import deque  

class SmallWorldNetwork(RandomGraph):
    
    def rewire(self, p, debug=False, rewNodesDebug=False):
        ''' takes a probability p as a parameter and, starting with a
            regular graph, rewires the graph using Watts and Strogatz's algorithm. '''
        degree = self.is_regular()
        if not degree:
            raise ValueError("Can only rewire regular graphs")
        
        dn = self.getDistanceMap()
        maxDist = int(degree/2)
        if debug: print("Max dist.: %r  Distance map: %r" % (maxDist, dn))
            
        # go around the lattice incrementing distances
        for dist in range(0, maxDist):   
            if debug: print("dist: %r" % dist)
                 
            for v in dn:
                v1 = dn[v][dist]
                if debug: print("  v: %r v1: %r" % (v, v1))
                
                if random.random() < p:
                    if debug: print("      P matched. Rewiring")
                    e = self[v][v1]
                    self.rewireNodes(v, v1, e, rewNodesDebug)
            
            

    def rewireNodes(self, v1, v2, e, debug=False):
        if debug: print("rewiring %r-%r" % (v1, v2))
        
        # loop unti getting a random unconnected node
        while True:
            randV = random.choice(list(self))
            if randV != v1 and randV != v2 and randV not in self[v1]: break
        
        self.remove_edge(e)
        self.add_edge(Edge(v1, randV))
        if debug: print("%r: edge rewired to %r-%r \n" % (e, v1, randV))
        
        
    def getDistanceMap(self):
        ''' distance is the distance between nodes as per creation order, 
            no the length of connection paths '''
        m = dict()
        vs = [*self]
        cycl = itertools.cycle(vs)
        
        for a in range(0, len(vs)):
            v = next(cycl)
            vNeib = []
            for dist in range(0, len(vs)-1):
                vNeib.append( next(cycl) )
            m[v] = vNeib 
            next(cycl) # shift one
        return m
        
        
        
    def clustering_coefficient(self):
        ''' computes and returns the clustering coefficient as defined in the paper.
            This is the C of each node averaged for all nodes
            C of a node is the fraction of the connections among its neibours (excluding itself)
            over the possible connections for that group (n*(n-1))/2
        '''
        cCoefs = []
        for v in self:
            cv = self.getClustering(v)
            cCoefs.append(cv)
        return sum(cCoefs) / len(cCoefs)

        
    def getClustering(self, v):
        ''' returns the number of connections of a node's neighbours divided by the number of
            potential connections for the node neighbours , which is (n*(n-1))/2
        '''
        vNbs = self.out_vertices(v)
        if len(vNbs) < 2:
            return .0
        
        grpConnCnt = 0
        for a, b in itertools.combinations(vNbs, 2):
            grpConnCnt += 1 if b in self[a] else 0
            
        if grpConnCnt == 0:
            return .0
        
        l = len(vNbs)
        return grpConnCnt * 2 / (l * (l-1))
                

    def averagePathLength(self):
        '''returns number of edges in shortest paths between two edges,
            averaged over all pairs of edges''' 
        loopNum = 1
        totDistsCnt = 0
        totDistsSum = 0
        
        for v in self:
            loopNum += 1
            distsCnt, distsSum = self.nodeAvgPathLength(v)
            totDistsCnt += distsCnt
            totDistsSum += distsSum 
                 
        return totDistsSum / totDistsCnt    
        
        
    def nodeAvgPathLength(self, srcV):
        ''' implementation of Dikjsta''s short path length algorithm'''  
        distMap = dict()

        q = deque()
        q.append(srcV)

        dist = 0
        distMap[srcV] = dist
        
        while len(q):
            curr_node = q.popleft()
            dist = distMap[curr_node]+1 if curr_node in distMap else 1 
            
            # Enqueue V neighbours
            connected = [v for v in self.out_vertices(curr_node) 
                         if v not in distMap and v not in q]
            q.extend(connected)
            for c in connected: 
                if c not in distMap:
                    distMap[c] = dist 
        
        validDistsCnt = 0
        validDistsSum = 0
        for d in distMap.values(): 
                if d != math.inf and d != 0:
                    validDistsCnt += 1
                    validDistsSum += d
        
        return validDistsCnt, validDistsSum 
        
        
        
    def show(self):
        # create a graph and a layout
        layout = GW.CircleLayout(self)
        gw = GW.GraphWorld()
        gw.show_graph(self, layout)
        gw.mainloop()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        
            
