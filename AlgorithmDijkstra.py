class AlgorithmDijkstra:
    def __init__(self, graph_dict):
        self.graph = graph_dict
        self.nodes = list(graph_dict.keys())
        self.steps = []

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
        hop_depth = {node: float('inf') for node in self.graph}
        pred_hop_map = {node: {} for node in self.graph}
        distances[start_node] = 0
        hop_depth[start_node] = 0
        labeled_nodes = set()
        iteration = 1
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

            if current_node == end_node:
                selected_distance = distances[current_node]
                selected_hop = hop_depth[current_node]
                selected_from = predecessors[current_node][0] if predecessors[current_node] else "-"

                selected_pred_hops = []
                if predecessors[current_node]:
                    for pred in predecessors[current_node]:
                        hop = pred_hop_map[current_node].get(pred, selected_hop)
                        selected_pred_hops.append({"desde": pred, "salto": hop})
                else:
                    selected_pred_hops.append({"desde": "-", "salto": 0})

                self.steps.append({
                    "iteracion": iteration,
                    "seleccionado": current_node,
                    "seleccionado_distancia": selected_distance,
                    "seleccionado_desde": selected_from,
                    "seleccionado_salto": selected_hop,
                    "seleccionado_pred_hops": selected_pred_hops,
                    "actualizaciones": []
                })
                break

            step_updates = []
            for neighbor, weight in self.graph[current_node].items():
                new_distance = distances[current_node] + weight
                new_hop = hop_depth[current_node] + 1

                if neighbor in labeled_nodes:
                    step_updates.append({
                        "nodo": neighbor,
                        "desde": current_node,
                        "distancia": new_distance,
                        "iteracion_salto": new_hop,
                        "ya_etiquetado": True,
                        "distancia_actual": distances[neighbor]
                    })
                elif new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    hop_depth[neighbor] = new_hop
                    predecessors[neighbor] = [current_node]
                    pred_hop_map[neighbor] = {current_node: new_hop}
                    step_updates.append({
                        "nodo": neighbor,
                        "desde": current_node,
                        "distancia": new_distance,
                        "iteracion_salto": new_hop
                    })
                elif new_distance == distances[neighbor]:
                    predecessors[neighbor].append(current_node)
                    pred_hop_map[neighbor][current_node] = new_hop
                    step_updates.append({
                        "nodo": neighbor,
                        "desde": current_node,
                        "distancia": new_distance,
                        "iteracion_salto": new_hop,
                        "empate": True
                    })
                else:
                    step_updates.append({
                        "nodo": neighbor,
                        "desde": current_node,
                        "distancia": new_distance,
                        "iteracion_salto": new_hop,
                        "no_mejora": True,
                        "distancia_actual": distances[neighbor]
                    })

            selected_distance = distances[current_node]
            selected_hop = hop_depth[current_node]
            selected_from = predecessors[current_node][0] if predecessors[current_node] else "-"

            selected_pred_hops = []
            if predecessors[current_node]:
                for pred in predecessors[current_node]:
                    hop = pred_hop_map[current_node].get(pred, selected_hop)
                    selected_pred_hops.append({"desde": pred, "salto": hop})
            else:
                selected_pred_hops.append({"desde": "-", "salto": 0})

            self.steps.append({
                "iteracion": iteration,
                "seleccionado": current_node,
                "seleccionado_distancia": selected_distance,
                "seleccionado_desde": selected_from,
                "seleccionado_salto": selected_hop,
                "seleccionado_pred_hops": selected_pred_hops,
                "actualizaciones": step_updates
            })
            iteration += 1

        if distances[end_node] == float('inf'):
            return None
        all_shortest_paths = self.reconstruct_paths(end_node, start_node, predecessors)
        return all_shortest_paths, distances[end_node]