# graph matching algorithm(s)

from graph import *

def gmatch(pattern, reference):
    """Match pattern graph to reference graph. 

       Pattern matches are subgraphs of reference (subgraph isomorphisms).
       (a subgraph is a subset of variables and subset of edges)
       Any vertices in the pattern that are equal to some vertex in reference, they are matched exactly.
       Otherwise, vertices in pattern are considered variables.
       Returns a list of solutions. 
       Each solution is a Map from pattern vertices to reference vertices (and vice versa).
    """

    if not isinstance(pattern, FanGraph):
        pattern = FanGraph(pattern)
    if not isinstance(reference, FanGraph):
        reference = FanGraph(reference)


    # For each pattern vertex:
    #  match with all vertices in reference that have at least same fanin and fanout.
    #  also match if pattern vertex in reference (same object or equal)
    #  Then combine matches (patvar, refvar) with existing partial solutions if:
    #    refvar still free in partial solution
    #    all edges adjacent to pattern vertex are also in reference graph

    solutions = None
    for patvar in pattern.vertices():
        if reference.has_vertex(patvar):
            matches = [patvar]
        else:
            fanin = pattern.fanin(patvar)
            fanout = pattern.fanout(patvar)
            inumbers = filter(lambda n: n>=fanin, reference.fanin_numbers())
            onumbers = filter(lambda n: n>=fanout, reference.fanout_numbers())
            inmatches = []
            for n in inumbers:
                inmatches += reference.infan(n)
            outmatches = []
            for n in onumbers:
                outmatches += reference.outfan(n)
            matches = Set(inmatches).intersection(outmatches)
        newsolutions = []
        if solutions == None:
            for refvar in matches:
                s = {patvar:refvar, refvar:patvar}
                newsolutions.append(s)
        else:
            for refvar in matches:
                for olds in solutions:
                    news = dict(olds)
                    news[patvar] = refvar
                    news[refvar] = patvar
                    consistent = True
                    # check for no double assignments
                    if patvar in olds:
                        if olds[patvar] != refvar:
                            consistent = False
                    if refvar in olds:
                        if olds[refvar] != patvar:
                            consistent = False
                    # check edges
                    for pe in pattern.adjacent_edges(patvar):
                        (pv1,pv2) = pe
                        if pv1 not in news or pv2 not in news:
                            continue
                        rv1 = news[pv1] 
                        rv2 = news[pv2] 
                        if not reference.has_edge(rv1,rv2):
                            consistent = False
                            break
                    if consistent:
                        newsolutions.append(news)
                #for
            #for
        #if
        solutions = newsolutions
    #for
    return solutions
#gmatch


def test():
    print "matching a triangle" 
    pattern = Graph()
    pattern.add_edge('x','a')
    pattern.add_edge('x','b')
    pattern.add_edge('y','a')
    pattern.add_edge('y','c')
    pattern.add_edge('z','b')
    pattern.add_edge('z','c')
    pattern.add_edge("distance","x")
    pattern.add_edge("distance","y")
    pattern.add_edge("distance","z")

    reference = Graph()
    reference.add_edge(1,'A')
    reference.add_edge(1,'B')
    reference.add_edge(2,'A')
    reference.add_edge(2,'C')
    reference.add_edge(3,'B')
    reference.add_edge(3,'C')
    reference.add_edge("rigid", 1)
    reference.add_edge("distance", 1)
    reference.add_edge("rigid", 2)
    reference.add_edge("distance", 2)
    reference.add_edge("rigid", 3)
    reference.add_edge("distance", 3)

    s = gmatch(pattern, reference)
    print s
    print len(s),"solutions"


    print "mathing random pattern in random graph"
    pattern = random_graph(3,6,False,"v")
    reference = random_graph(100,200,False,"t")
    s = gmatch(pattern, reference)
    print s
    print len(s),"solutions"


if __name__ == "__main__": test()



