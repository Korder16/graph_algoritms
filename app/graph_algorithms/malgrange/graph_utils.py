from dataclasses import dataclass
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
from .table_utils import generate_result_table
import base64
from io import BytesIO

plt.switch_backend('Agg')


@dataclass
class transitive_clouse_info:
    nodes: set
    distances: list

    def serialize(self):
        return {
            'nodes': sorted(list(self.nodes)),
            'distances': self.distances
        }


@dataclass
class node_info:
    name: str
    transitive_closure: transitive_clouse_info
    reverse_transitive_closure: transitive_clouse_info

    def get_connectivity_component(self) -> set:
        return set(sorted(self.transitive_closure.nodes.intersection(self.reverse_transitive_closure.nodes), key=str.lower))

    def serialize(self):
        return {
            'name': self.name,
            'transitive_closure': self.transitive_closure.serialize(),
            'reverse_transitive_closure': self.reverse_transitive_closure.serialize(),
            'connectivity_component': sorted(list(self.get_connectivity_component()))
        }

    def __repr__(self):
        tokens = [
            f'Вершина {self.name}:',
            f'  Г{self.name}: {self.transitive_closure.nodes}',
            f'  (Г^{self.name})⁻¹: {self.reverse_transitive_closure.nodes}',
            f'  С{self.name}: {self.get_connectivity_component()}'
        ]

        return '\n'.join(tokens)


class graph_utils:

    def __init__(self, graph: nx.graph) -> None:
        self.__graph = graph
        self.__node_infos = []

    def get_transitive_closure(self, node: str):
        transitive_closure = set()
        self.collect_successors(node, set(), transitive_closure)
        return transitive_closure

    def collect_successors(self, node: str, visited: set, transitive_closure: set):
        current_successors = set(self.__graph.successors(node))
        current_successors.add(node)
        for successor in current_successors:
            if successor not in visited:
                visited.add(successor)
                transitive_closure.add(successor)
                self.collect_successors(successor, visited, transitive_closure)

    def get_reverse_transitive_closure(self, node: str):
        reverse_transitive_closure = set()
        self.collect_predecessors(node, set(), reverse_transitive_closure)
        return reverse_transitive_closure

    def collect_predecessors(self, node: str, visited: set, reverse_transitive_closure: set):
        current_predecessors = set(self.__graph.predecessors(node))
        current_predecessors.add(node)
        for predecessor in current_predecessors:
            if predecessor not in visited:
                visited.add(predecessor)
                reverse_transitive_closure.add(predecessor)
                self.collect_predecessors(predecessor, visited, reverse_transitive_closure)

    def find_connecivity_components(self, nodes_to_view: list):
        connectivity_components = []
        tmp_graph = self.__graph.copy()
        nodes_to_view_iter = iter(nodes_to_view)
        erased_nodes = set()

        while len(self.__graph.nodes) > 0:
            node = next(nodes_to_view_iter)
            transitive_closure = self.get_transitive_closure(node)
            reverse_transitive_closure = self.get_reverse_transitive_closure(node)

            distances = []
            for target in tmp_graph.nodes:
                distances.append(find_distance_to_node(tmp_graph, node, target, erased_nodes))

            reverse_distances = []
            for target in tmp_graph.nodes:
                reverse_distances.append(find_distance_from_node(tmp_graph, target, node, erased_nodes))

            current_transitive_closure = transitive_clouse_info(transitive_closure, distances)
            current_reverse_transitive_closure = transitive_clouse_info(reverse_transitive_closure, reverse_distances)
            self.__node_infos.append(node_info(node, current_transitive_closure, current_reverse_transitive_closure))

            connectivity_component = set(sorted(transitive_closure.intersection(reverse_transitive_closure), key=str.lower))
            connectivity_components.append(connectivity_component)

            for comp in connectivity_component:
                erased_nodes.add(comp)

            self.__graph.remove_nodes_from(erased_nodes)
        return connectivity_components

    def get_node_infos(self):
        return self.__node_infos


def create_graph_from_adj_matrix(matrix):
    return nx.from_pandas_adjacency(matrix, create_using=nx.DiGraph)


def draw_graph(graph: nx.DiGraph, color_map: list):
    nx.draw(graph, node_color=color_map, with_labels=True)
    buff = BytesIO()
    plt.savefig(buff, format='png')
    plt.close()
    return base64.b64encode(buff.getbuffer()).decode('ascii')


def color_connectivity_components_in_graph(graph: nx.DiGraph, connectivity_components: list, colors: list):
    color_map = []

    for node in graph:
        for component, color in zip(connectivity_components, colors):
            if node in component:
                color_map.append(color)

    return color_map


def find_distance_between_two_nodes(graph: nx.digraph, src: str, dest: str):
    return nx.shortest_path_length(graph, source=src, target=dest)


def find_distance_to_node(graph: nx.digraph, src: str, dest: str, erased_nodes: set):
    if dest in erased_nodes:
        return '\\'
    else:
        if nx.has_path(graph, src, dest):
            return find_distance_between_two_nodes(graph, src, dest)
        else:
            return 'x'


def find_distance_from_node(graph: nx.digraph, src: str, dest: str, erased_nodes: set):
    if src in erased_nodes:
        return '\\'
    else:
        if nx.has_path(graph, src, dest):
            return find_distance_between_two_nodes(graph, src, dest)
        else:
            return 'x'


def rename_adj_matrix(adj_matrix: pd.DataFrame):
    mapping = {
        0: 'a',
        1: 'b',
        2: 'c',
        3: 'd',
        4: 'e',
        5: 'f',
        6: 'g',
        7: 'h',
        8: 'i',
        9: 'k'
    }

    adj_matrix = adj_matrix.rename(columns=mapping)
    adj_matrix = adj_matrix.rename(index=mapping)
    return adj_matrix


def process_graph(adj_matrix: pd.DataFrame, nodes_to_view: list, colors: list):

    graph = create_graph_from_adj_matrix(adj_matrix)
    result_graph = graph.copy()

    utils = graph_utils(graph)
    connectivity_components = utils.find_connecivity_components(nodes_to_view)

    result_table = generate_result_table(adj_matrix.copy(), utils.get_node_infos())

    color_map = color_connectivity_components_in_graph(result_graph, connectivity_components, colors)
    img_bytes = draw_graph(result_graph, color_map)

    return result_table, utils.get_node_infos(), img_bytes
