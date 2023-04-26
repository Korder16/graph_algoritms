import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import base64
from io import BytesIO

plt.switch_backend('Agg')

def rename_adj_matrix_impl(adj_matrix: pd.DataFrame, mapping: dict):
    adj_matrix = adj_matrix.rename(columns=mapping)
    adj_matrix = adj_matrix.rename(index=mapping)
    return adj_matrix


def create_graph_from_adj_matrix(matrix: pd.DataFrame):
    return nx.from_pandas_adjacency(matrix, create_using=nx.DiGraph)


def draw_graph(graph: nx.DiGraph, color_map: list = None):
    if color_map:
        nx.draw(graph, node_color=color_map, with_labels=True)
    else:
        nx.draw(graph, with_labels=True)
    buff = BytesIO()
    plt.savefig(buff, format='png')
    plt.close()
    return base64.b64encode(buff.getbuffer()).decode('ascii')