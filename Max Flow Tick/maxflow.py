import csv

def bfs_path(graph, s, t):
    vertices = set([edge[0] for edge in graph.keys()]+[edge[1] for edge in graph.keys()])
    path_dict = {}
    for v in vertices:
        path_dict[v] = {'Seen': False, 'Come From': None}
    # Set start node to seen
    path_dict[s]['Seen'] = True
    to_explore = [s]

    # Get neighbours for each vertex
    neighbours = {}
    for v, w in graph.keys():
        v, w = v, w
        if v in neighbours:
            neighbours[v] += [w]
        else:
            neighbours[v] = [w]
    
    # Traverse graph starting from s
    while not to_explore == []:
        v = to_explore[0]
        del to_explore[0]
        if v in neighbours:
            for w in neighbours[v]:
                if not path_dict[w]['Seen']:
                    to_explore.append(w)
                    path_dict[w]['Seen'] = True
                    path_dict[w]['Come From'] = v, graph[(str(v), str(w))][1]
            
    # Reconstruct path starting at t
    if path_dict[t]['Come From'] is None:
        # Find all vertices we visited from s as this is a min cut 
        visited = []
        for v in path_dict:
            if path_dict[v]['Seen']:
                visited.append(v)
        return None, visited # No path from s to t
    else:
        path = [(t, None)]
        while True:
            if path_dict[path[0][0]]['Come From'][0] == s:
                path = [path_dict[path[0][0]]['Come From']] + path
                break
            path = [path_dict[path[0][0]]['Come From']] + path
        return path, []
    

    

def compute_max_flow(capacity, s, t):
    # Initialise flows
    flows = {}
    for edge in capacity.keys():
        flows[edge] = 0

    # Define helper function to find augmenting path
    def find_augmenting_path():
        # Define residual graph 
        h = {}
        for edge in capacity.keys():
            if flows[edge] < capacity[edge]:
                h[edge] = capacity[edge] - flows[edge], 'inc'
            if flows[edge] > 0:
                h[(edge[1], edge[0])] = flows[edge], 'dec'
        
        path, min_c = bfs_path(h, s, t)
        if not path is None:
            return path, []
        else:
            return None, min_c
    
    min_cut = []
    
    # Repeatedly find augmenting path and add flow to it
    while True:
        path, min_cut = find_augmenting_path()
        if path is None:
            break
        else:
            delta = float('inf')
            for i in range(len(path)-1):
                edge = path[i][0], path[i+1][0]
                if path[i][1] == 'inc':
                    delta = min(delta, capacity[edge] - flows[edge])
                else:
                    delta = min(delta, flows[path[i+1][0], path[i][0]])
        
        for i in range(len(path)-1):
            edge = path[i][0], path[i+1][0]
            if path[i][1] == 'inc':
                flows[edge] += delta
            else:
                flows[path[i+1][0], path[i][0]] -= delta
    
    outgoing = 0
    incoming = 0
    vertices = set([edge[0] for edge in capacity.keys()]+[edge[1] for edge in capacity.keys()])
    for v in vertices:
        if ('0', v) in flows:
            outgoing += flows[('0', v)]
        if (v, '0') in flows:
            incoming += flows[(v, '0')]
    total_flow = outgoing - incoming

    return total_flow, flows, min_cut


with open('flownetwork_07.csv') as f:
    rows = [row for row in csv.reader(f)][1:]
capacity = {(u, v): int(c) for u,v,c in rows}

print(compute_max_flow(capacity, '0', '14'))