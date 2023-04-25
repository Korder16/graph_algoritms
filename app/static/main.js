$(document).ready(function(){
    $('.btn').click(function(){
        var e = document.getElementById("rk-variant");
        var rk_variant_text = e.options[e.selectedIndex].text;

        var text_input = document.getElementById("nodes-to-visit");
        var nodes_to_visit = text_input.value

        $.ajax({
            url: '?variant_number=' + rk_variant_text + '&nodes_to_visit=' + nodes_to_visit,
            type: 'get',
            contentType: 'application/json',
            data: {},
            success: function(response){

                $(".result-table-head th").remove()

                $("#result-table-body tr").remove()
                $("#result-table-body td").remove()

                for(var i = 0; i < response.column_names.length; i++) {
                    $(".result-table-head").append('<th>' + response.column_names[i] + '</th>')
                }

                const table_body = document.getElementById("result-table-body");
                for(var i = 0; i < response.row_data.length; i++) {
                    const row = response.row_data[i];
                    var row_element = document.createElement('tr')
                    for(var j = 0; j < row.length; j++) {
                        var td = document.createElement('td')
                        var td_text = document.createTextNode(row[j])
                        td.appendChild(td_text)
                        row_element.appendChild(td)
                    }

                    table_body.appendChild(row_element)
                }

                $('.graph-image').attr('src', 'data:image/png;base64,' + response.graph_img_bytes)

                $('.connectivity-components li').remove()
                for(var i = 0; i < response.node_infos.length; i++) {
                    var node_name = response.node_infos[i]['name']
                    var transitive_closure_nodes = response.node_infos[i]['transitive_closure']['nodes']
                    var reverse_transitive_closure_nodes = response.node_infos[i]['reverse_transitive_closure']['nodes']
                    var connectivity_component = response.node_infos[i]['connectivity_component']

                    $('.connectivity-components').append(
                        '<li> Вершина ' + node_name + ':<br/>' +
                        'Г' + node_name + ': {' + transitive_closure_nodes + '}' + '<br/>' +
                        '(Г^' + node_name + ')⁻¹' + ': {' + reverse_transitive_closure_nodes + '}' + '<br/>' +
                        'C' + node_name + ': {' + connectivity_component + '}' + '<br/>' +
                         '</li>'
                    )
                }
            },
            error: function(ajaxContext) {
                alert('Алгоритм не работает на рассматриваемых вершинах:' + nodes_to_visit);
            }
        })
    })
})