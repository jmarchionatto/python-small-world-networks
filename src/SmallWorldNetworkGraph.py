'''
Graph of implementation of Watts and Strogatz paper
"Collective Dynamics of 'small-world' networks" 

Created on May 11, 2020

@author: Juan Marchionatto
'''
import matplotlib.pyplot as pyplot
import math 

import Graph as G
import SmallWorldNetwork as SWN


def main():
    ''' Graph over 20 random realizations of the rewiring process. Graphs have 1000 Verices
    and average of 10 edges each. 
    Make a graph that replicates the line marked C(p)/C(0) in Figure 2 of the paper. In other
        words, confirm that the clustering coefficient drops off slowly for small values of p.'''

    clustCoefArr = []
    LCoefArr = []
    pArr = []

    loopCnt = 0
     
    # generate 10-exponential prabability values so they are plotted
    # as equidistant in the log plot
    for i in range(38, -1, -2):
        pw = math.pow(10, i/10)
        p = 1/pw
        pArr.append(p)
                
        g = makeRegGraph(1000, 10)

        if loopCnt == 0:
            C0 = g.clustering_coefficient()
            L0 = g.averagePathLength()
        
        g.rewire(p)
        
        clustCoef = g.clustering_coefficient()
        clustCoefArr.append(clustCoef/C0) 

        lCoef = g.averagePathLength()
        LCoefArr.append(lCoef/L0)
        
        loopCnt +=1
        print("Loop {:2d} of {:2d}.   P: {:07.5f}   C(p)/C(0): {:07.5f}    L(p)/L(0): {:07.5f}".format(
            loopCnt, 20, p, clustCoef/C0, lCoef/L0) )
    
    pyplot.xscale('log')
    pyplot.xlim(.0001, 1)
    pyplot.ylim(.05, 1.02)
    pyplot.plot(pArr, clustCoefArr, 'bo')
    pyplot.plot(pArr, LCoefArr, 'go')

    pyplot.show()
    

def makeRegGraph(VQty, degree):
    vs = []
    for vi in range(0,VQty):
        vs.append( G.Vertex(str(vi)) )
    g = SWN.SmallWorldNetwork(vs, [])
    g.add_regular_edges(degree)
    return g


if __name__ == "__main__":
    main()

