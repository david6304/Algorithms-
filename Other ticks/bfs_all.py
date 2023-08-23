def shortest_paths(g, s, t):
    path_dict = {v: [float('inf'), None] for v in g.keys()}
    path_dict[s][0] = 1
    to_explore = [s]

    while to_explore:
        v = to_explore[0]
        del to_explore[0]
        if g[v]:
            for w in g[v]:
                if path_dict[w][0] == float('inf'):
                    to_explore.append(w)
                    path_dict[w] = [path_dict[v][0]+1, [v]]
                elif path_dict[w][0] == path_dict[v][0] + 1:
                    path_dict[w][1].append(v)
                
    
    if path_dict[t][1] is None:
        return []
    else:
        def get_paths(v, path_dict):
            paths = []
            if path_dict[v][1] is None:
                return [[v]]
            for pred in path_dict[v][1]:
                pred_paths = get_paths(pred, path_dict)
                for path in pred_paths:
                    paths.append(path + [v])
            
            return paths

        return get_paths(t, path_dict)
    
graph = {0: {3}, 1: {2, 3}, 2: set(), 3: {2}}
print(shortest_paths(graph, 3, 1)) 