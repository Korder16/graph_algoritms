def fill_rows(adj_matrix, node_infos: list):
    adj_matrix.loc[' '] = ''
    for info in node_infos:
        adj_matrix.loc[f'(Г{info.name})⁻¹'] = info.reverse_transitive_closure.distances
    adj_matrix.loc[''] = '\\'


def fill_columns(adj_matrix, node_infos: list):
    adj_matrix.insert(10, '', [''] * (12 + len(node_infos)))

    col_number = 11
    for info in node_infos:
        adj_matrix.insert(col_number, f'Г{info.name}', info.transitive_closure.distances + [''] * (2 + len(node_infos)))
        col_number += 1

    adj_matrix.insert(col_number, f' ', ['\\'] * 10 + [''] * (2 + len(node_infos)))


def generate_result_table(adj_matrix, node_infos: list):
    fill_rows(adj_matrix, node_infos)
    fill_columns(adj_matrix, node_infos)
    return adj_matrix
