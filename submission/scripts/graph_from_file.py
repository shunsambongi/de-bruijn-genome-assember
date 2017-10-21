import sys

def graph_from_file(file):
    graph = {}
    lines = [line.strip() for line in file.readlines()]
    for line in lines:
        line = line.split(' -> ')
        graph[line[0]] = line[1].split(',')
    return graph
