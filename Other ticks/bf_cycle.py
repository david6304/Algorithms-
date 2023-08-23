def find_cycle(g):
    return True

def bf(g, s):
    minweights = {v: float('inf') for v in g.keys()}
    minweights[s] = 0

    for _ in range(len(list(g.keys()))-1):
        for u in g.keys():
            if g[u]:
                for v in g[u].keys():
                    c = g[u][v]
                    if minweights[u] + c < minweights[v]:
                        minweights[v] = minweights[u] + c
        
    neg_cycle = []
    for u in g.keys():
        if g[u]:
            for v in g[u].keys():
                c = g[u][v]
                if minweights[u] + c < minweights[v]:
                    negative_loop = [v, u]
                    for _ in range(len(list(g.keys()))-1):
                        u = negative_loop[0]
                        for u in g.keys():
                            if g[u]:
                                for v in g[u].keys():
                                    c = g[u][v]
                                    if minweights[u] + c < minweights[v]:
                                        negative_loop = [v] + negative_loop
                    
                    neg_cycle = find_cycle(negative_loop)

                            
    if neg_cycle:
        return (None, neg_cycle)
    else:
        for key in minweights.keys():
            minweights[key] = minweights[key][0]
        return (minweights, None)

graph = {'a':{'b':3, 'c': -2}, 'b':{}, 'c':{'a':-1}} 

print(bf(graph, 'a'))