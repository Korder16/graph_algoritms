from ..graph_utils import rename_adj_matrix_impl, create_graph_from_adj_matrix, draw_graph
import pandas as pd

def rename_adj_matrix(adj_matrix: pd.DataFrame):
    mapping = {
        0: 'x0',
        1: 'x1',
        2: 'x2',
        3: 'x3',
        4: 'x4',
        5: 'x5',
        6: 'x6',
        7: 'x7'
    }

    return rename_adj_matrix_impl(adj_matrix, mapping)

def process_graph(adj_matrix: pd.DataFrame):
    graph = create_graph_from_adj_matrix(adj_matrix)

    img_bytes = draw_graph(graph)
    return adj_matrix, img_bytes