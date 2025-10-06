class AlgorithmDijkstra:
    def __init__(self, graph_dict):
        self.graph = graph_dict
        self.nodes = list(graph_dict.keys())

    def reconstruct_paths(self, current_node, start_node, predecessors):
        if current_node == start_node:
            return [[start_node]]

        paths_from_start = []
        for pred in predecessors[current_node]:
            for path in self.reconstruct_paths(pred, start_node, predecessors):
                paths_from_start.append(path + [current_node])

        return paths_from_start

    def find_short_path(self, start_node, end_node):
        distances = {node: float('inf') for node in self.graph}
        predecessors = {node: [] for node in self.graph}
        distances[start_node] = 0
        labeled_nodes = set()
        while len(labeled_nodes) < len(self.graph):
            current_node = None
            min_distance = float('inf')
            for node in self.graph:
                if node not in labeled_nodes and distances[node] < min_distance:
                    min_distance = distances[node]
                    current_node = node
            if current_node is None:
                return None
            labeled_nodes.add(current_node)
            for neighbor, weight in self.graph[current_node].items():
                if neighbor not in labeled_nodes:
                    new_distance = distances[current_node] + weight
                    if new_distance < distances[neighbor]:
                        distances[neighbor] = new_distance
                        predecessors[neighbor] = [current_node]
                    elif new_distance == distances[neighbor]:
                        predecessors[neighbor].append(current_node)
        if distances[end_node] == float('inf'):
            return None
        all_shortest_paths = self.reconstruct_paths(end_node, start_node, predecessors)
        return all_shortest_paths, distances[end_node]
