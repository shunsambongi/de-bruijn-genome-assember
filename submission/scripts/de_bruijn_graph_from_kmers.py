import sys
from prefix import prefix
from suffix import suffix

def de_bruijn_graph(patterns):
    graph = {}
    for pattern in patterns:
        if prefix(pattern) not in graph:
            graph[prefix(pattern)] = [suffix(pattern)]
        else:
            graph[prefix(pattern)].append(suffix(pattern))
    return graph

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        patterns = [line.strip() for line in file.readlines()]
    graph = de_bruijn_graph(patterns)
    items = sorted(graph.items())
    dir_edge = '->'
    for item in items:
        print(item[0], dir_edge, ','.join(sorted(item[1])))
