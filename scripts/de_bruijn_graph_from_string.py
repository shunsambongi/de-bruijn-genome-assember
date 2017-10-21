import sys
from prefix import prefix
from suffix import suffix

def de_bruijn_graph(text, k):
    graph = {}
    for i in range(len(text) - k + 1):
        kmer = text[i:i+k]
        if prefix(kmer) not in graph:
            graph[prefix(kmer)] = [suffix(kmer)]
        else:
            graph[prefix(kmer)].append(suffix(kmer))
    return graph


if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        k = int(next(file).strip())
        text = next(file).strip()
    graph = de_bruijn_graph(text, k)
    items = sorted(graph.items())
    dir_edge = '->'
    for item in items:
        print(item[0], dir_edge, ','.join(sorted(item[1])))
