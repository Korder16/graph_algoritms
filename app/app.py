from flask import Flask, render_template, request, jsonify
import numpy as np

from graph_algorithms import malgrange, dijkstra

app = Flask(__name__)


def solve_malgrange_rk_impl(variant, nodes_to_visit: list):
    colors = [
        'red',
        'green',
        'yellow',
        'blue',
        'white',
        'pink',
        'grey'
    ]

    adj_matrix = malgrange.rename_adj_matrix(variant)
    return malgrange.process_graph(adj_matrix, nodes_to_visit, colors)


def solve_dijkstra_rk_impl(variant):
    adj_matrix = dijkstra.rename_adj_matrix(variant)

    adj_matrix = dijkstra.rename_adj_matrix(variant)
    return dijkstra.process_graph(adj_matrix)


@app.route('/malgrange')
def solve_malgrange_rk():

    if request.is_json:
        variant_number = request.args.get('variant_number', type=int)
        variant = malgrange.rk_variants[variant_number]

        nodes_to_visit = request.args.get('nodes_to_visit', type=str)
        result_table, node_infos, graph_img_bytes = solve_malgrange_rk_impl(variant, nodes_to_visit.replace(' ', '').split(','))

        row_data = []
        for index, row in result_table.iterrows():
            row_data.append([index] + row.tolist())

        column_names = np.insert(result_table.columns.values, 0, ' ')

        return jsonify(
            {
                'node_infos': [node_info.serialize() for node_info in node_infos],
                'graph_img_bytes': graph_img_bytes,
                'column_names': column_names.tolist(),
                'row_data': row_data
            }
        )

    return render_template('malgrange.html', variants=malgrange.rk_variants.keys())

@app.route('/dijkstra')
def solve_dijkstra_rk():

    if request.is_json:
        variant_number = request.args.get('variant_number', type=int)
        variant = dijkstra.rk_variants[variant_number]

        result_table, graph_img_bytes = solve_dijkstra_rk_impl(variant)

        row_data = []
        for index, row in result_table.iterrows():
            row_data.append([index] + row.tolist())

        column_names = np.insert(result_table.columns.values, 0, ' ')

        return jsonify(
            {
                'graph_img_bytes': graph_img_bytes,
                'column_names': column_names.tolist(),
                'row_data': row_data
            }
        )

    return render_template('dijkstra.html', variants=dijkstra.rk_variants.keys())


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
