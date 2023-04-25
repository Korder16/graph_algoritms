from flask import Flask, render_template, request, jsonify
import numpy as np

from graph_algorithms import process_graph, rename_adj_matrix, rk_variants

app = Flask(__name__)


def solve_rk(variant, nodes_to_visit: list):
    colors = [
        'red',
        'green',
        'yellow',
        'blue',
        'white',
        'pink',
        'grey'
    ]

    adj_matrix = rename_adj_matrix(variant)
    return process_graph(adj_matrix, nodes_to_visit, colors)


@app.route('/')
def show_rk_solution():

    if request.is_json:
        variant_number = request.args.get('variant_number', default=0, type=int)
        variant = rk_variants[variant_number]

        nodes_to_visit = request.args.get('nodes_to_visit', default='b,d,g', type=str)
        result_table, node_infos, graph_img_bytes = solve_rk(variant, nodes_to_visit.split(','))

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

    return render_template('index.html', variants=rk_variants.keys())


if __name__ == '__main__':
    from waitress import serve
    serve(app, host='0.0.0.0', port=5000)
