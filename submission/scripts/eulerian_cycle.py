import sys
from graph_from_file import graph_from_file

def eulerian_cycle(graph):
    start_node = list(graph.keys())[0]
    cycle = get_cycle(start_node, graph)
    while graph:
        for i, node in enumerate(cycle):
            if node in graph:
                cycle = get_cycle(node, graph) + cycle[i:] + cycle[:i]
                break
    cycle.append(cycle[0])
    return cycle

def get_cycle(node, graph):
    cycle = []
    while node in graph:
        cycle.append(node)
        next_node = graph[node][0]
        graph[node] = graph[node][1:]
        if not graph[node]:
            del graph[node]
        node = next_node
    return cycle

if __name__ == '__main__':
    with open(sys.argv[1]) as file:
        graph = graph_from_file(file)
#        lines = [line.strip() for line in file.readlines()]
#        for line in lines:
#            line = line.split(' -> ')
#            graph[line[0]] = line[1].split(',')
    cycle = eulerian_cycle(graph)
    dir_edge = '->'
    print(dir_edge.join(cycle))
