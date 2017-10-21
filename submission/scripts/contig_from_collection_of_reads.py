import sys
from de_bruijn_graph_from_kmers import de_bruijn_graph
from string_from_path import string_from_path
from eulerian_cycle import eulerian_cycle
import de_bruijn_graph_from_string

def maximal_nonbranching_paths(graph):
    k = len(list(graph.keys())[0]) + 1
#    print(k)
    paths = []
    in_counts = [x for sublist in graph.values() for x in sublist]
#    printg(graph)
    for v in set(list(graph.keys()) + in_counts):
        if not is_1_to_1(v, in_counts, graph):
            if v in graph and len(graph[v]) > 0:
                for w in graph[v]:
                    nonbranching_path = string_from_path([v, w])
                    while is_1_to_1(w, in_counts, graph):
                        u = graph[w][0]
                        nonbranching_path = string_from_path([nonbranching_path, u])
                        w = u
#                    print(nonbranching_path)
                    paths.append(nonbranching_path)
    for path in paths:
#        printg(graph)
#        print(path)
        sub_graph = de_bruijn_graph_from_string.de_bruijn_graph(path, k)
#        printg(sub_graph)
#        print('\n')
        for key, value in sub_graph.items():
            for item in value:
                graph[key].remove(item)
            if not graph[key]:
                del graph[key]
#        printg(graph)
#        print('\n')
    while graph:
        cycle = eulerian_cycle(graph)
        path = string_from_path(cycle)
        paths.append(path)
    return paths

def is_1_to_1(node, in_counts, graph):
    indegree = in_counts.count(node)
    outdegree = 0
    if node in graph:
        outdegree = len(graph[node])
#    print(node, indegree, outdegree)
    return indegree == outdegree == 1

def printg(graph):
    for item in graph:
        print(item, ' -> ', ','.join(graph[item]))


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        patterns = [line.strip() for line in file.readlines()]
    graph = de_bruijn_graph(patterns)
    contigs = maximal_nonbranching_paths(graph)
    print(' '.join(sorted(contigs)))
