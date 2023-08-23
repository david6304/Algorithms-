def isDag(g):
    visited = {v: False for v in g.keys()}
    cycle = False
    for v in g.keys():
        if not visited[v]:
            stack = []
            cycle = visit(v, stack, visited, g)
            if cycle:
                return True
    return cycle

def visit(v, stack, visited, g):
    visited[v] = True
    s = stack.copy()
    s.append(v)
    if g[v]:
        for w in g[v]:
            if w in s:
                return True
            if not visited[w]:
                return visit(w, s, visited, g)
    return False

graph = {1: {2}, 2: {3}, 3: {1}}

print(isDag(graph))