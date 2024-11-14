// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>, 2020 Edvard Rejthar <github@edvard.cz>, 2021 Mikk Margus Möll <mikk@cert.ee>
//
// SPDX-License-Identifier: AGPL-3.0-or-later

/**
 * Big variable options, passed to vis library.
 * There are also all the manipulation methods.
 */
'use strict';

var NETWORK_OPTIONS = {
    physics: {
        hierarchicalRepulsion: {
            nodeDistance: 200,
            springLength: 200
        },
        stabilization: {
            enabled: true,
            fit: true
        },
        solver: 'hierarchicalRepulsion'
    },
    interaction: {
        tooltipDelay: 1000,
        navigationButtons: true,
        keyboard: {
            bindToWindow: false
        }
    },
    nodes: {
        font: {
            size: 14, // px
            face: 'arial',
            align: 'center'
        }
    },
    edges: {
        length: 200,
        arrows: {
            to: {enabled: true, scaleFactor: 1, type: 'arrow'}
        },
        physics: true,
        font: {
            size: 14, // px
            face: 'arial',
        },
        color: {
            inherit: false
        },
        smooth: {
            enabled: true,
            type: 'continuous'
        }
    },
    groups: {
        Collector: {
            shape: 'box',
            color: GROUP_COLORS['Collector'][0],
        },
        Parser: {
            shape: 'box',
            color: GROUP_COLORS['Parser'][0]
        },
        Expert: {
            shape: 'box',
            color: GROUP_COLORS['Expert'][0],
            fontColor: "#FFFFFF"
        },
        Output: {
            shape: 'box',
            color: GROUP_COLORS['Output'][0]
        }
    },

    manipulation: {
        enabled: true,
        initiallyActive: true,
        editEdge: false,

        addNode: (data, callback) => create_form("Add Node", data, callback),
        editNode: function (data, callback) {
            create_form("Edit Node", data, callback);
            fill_bot(data.id, undefined, undefined);
        },
        deleteNode: function (data, callback) {
            callback(data);
            let node_set = new Set(data.nodes);

            for (let edge_index of data.edges) {
                let [from, to, path] = from_edge_id(edge_index);
                if (!node_set.has(from)) { // otherwise handled by node deletion below
                    remove_edge(from, to, path);
                }
            }

            for (let node_name of data.nodes) {
                delete app.nodes[node_name];
            }
            set_pending_change();
        },
        addEdge: function (data, callback) {
            if (data.from === data.to) {
                show_error('This action would cause an infinite loop');
                return;
            }

            if (data.path === undefined)
                data.path = '_default';

            let edit_needed = false; // there is path name clash
            let occupied_values = new Set(); // prevent edges from overlapping
            let roundness = 0;

            let edge_id = to_edge_id(data.from, data.to, data.path);
            let source_paths = app.nodes[data.from].parameters.destination_queues;
            for (let path_id in source_paths) {
                if (source_paths[path_id].includes(`${data.to}-queue`)) {
                    let smooth = app.network_data.edges.get(edge_id).smooth;
                    occupied_values.add(smooth ? smooth.roundness : 0);

                    if(path_id === data.path) {
                        show_error('There is already a link between those bots with the same path, rename.');
                        edit_needed = true;
                    }
                }
            }

            if (occupied_values.size) {
                while(occupied_values.has(roundness)) {
                    roundness += 0.3;
                }
                data.smooth = {type: 'curvedCCW', roundness};
            }

            let group_from = app.nodes[data.from].group;
            let group_to = app.nodes[data.to].group;
            let neighbors = ACCEPTED_NEIGHBORS[group_from];
            let available_neighbor = false;

            if (neighbors.includes(group_to)) {
                data.id = edge_id;
                callback(data);
                available_neighbor = true;
                let cautious = CAUTIOUS_NEIGHBORS[group_from] ?? [];
                if (cautious.includes(group_to)) {
                    show_error(`Node type ${group_from} can connect to the ${group_to}, however it's not so common.`);
                }
            }

            if (!available_neighbor) {
                if (neighbors.length === 0) {
                    show_error(`Node type ${group_from} can't connect to other nodes`);
                } else {
                    show_error(`Node type ${group_from} can only connect to nodes of types: ${neighbors.join()}`);
                }
                return;
            }

            add_edge(data.from, data.to, data.path);

            set_pending_change(data.from);
            if (edit_needed) {
                editPath(app, data.id, true);
            }
        },
        deleteEdge: function (data, callback) {
            let [from, to, path] = from_edge_id(data.edges[0]);
            let queue = app.nodes[from].parameters.destination_queues[path];
            remove_edge(from, to, path);

            set_pending_change(from);
            callback(data);
        }
    },
    layout: {
        hierarchical: false,
        randomSeed: undefined
    }
};

/**
 * Setting path name of a queue. If path already exists between bots, dialog re-appears.
 * If cancelled, previous path name is restored, or queue is deleted (if was just being added).
 * As this is not a standard-vis function, it has to be a separate method.
 *
 * @param app
 * @param edge id of the edge
 * @param adding True if edge is just being added (and shall be removed if we fail to provide a unique path name).
 */
function editPath(app, edge, adding=false) {
    let ok_clicked = false;
    let [from, to, original_path] = from_edge_id(edge);
    let nondefault_path = original_path === '_default' ? undefined : original_path;
    let new_path, nondefault_new_path;

    let $input = $("<input/>", {placeholder: "_default", val: nondefault_path});
    popupModal("Set the edge name", $input, () => {
        let in_val = $input.val();
        [new_path, nondefault_new_path] = (in_val && in_val !== '_default') ? [in_val, in_val] : ['_default', undefined];
        if (original_path === new_path) {
            return;
        }

        ok_clicked = true;
        set_pending_change();
    }).on("hide.bs.modal", () => {
        let from_queues = app.nodes[from].parameters.destination_queues[new_path] ?? [];
        let duplicate_edge = from_queues.includes(to);

        if (duplicate_edge) {
            if (ok_clicked) {
                show_error(`Could not add the queue ${new_path}, there already is such queue.`);
                return editPath(app, edge, adding);
            } else if(adding) {
                show_error(`Removing duplicate edge ${new_path}.`);
            } else {
                show_error("Keeping original path name.");
                return;
            }
        }

        if (ok_clicked) {
            let new_id = to_edge_id(from, to, new_path);

            remove_edge(from, to, original_path);
            app.network_data.edges.remove({id: edge});

            add_edge(from, to, new_path);
            app.network_data.edges.add({id: new_id, from, to: to.replace(/-queue$/, ''), label: nondefault_new_path});
        }
    });
}

/**
 * As this is not a standard-vis function, it has to be a separate method.
 */
function duplicateNode(app, bot) {
    let new_id = gen_new_id(bot);

    // deep copy old bot information
    let node = $.extend(true, {}, app.nodes[bot]);
    app.positions[new_id] = app.positions[bot];
    node.id = new_id;
    node.bot_id = new_id;
    app.nodes[new_id] = node;
    // add to the Vis and focus
    app.network_data.nodes.add(convert_nodes([node], true));
    for (let edge of app.network.getConnectedEdges(bot).map(edge => app.network_data.edges.get(edge))) {
        let [old_from, old_to, path] = from_edge_id(edge.id);
        if (edge.from === bot) {
            edge.from = new_id;
        }
        else if (edge.to === bot) {
            edge.to = new_id;
        }
        edge.id = to_edge_id(edge.from, edge.to, path);
        app.network_data.edges.add(edge);
    }

    app.network.selectNodes([new_id]);
    app.network.focus(new_id);
    set_pending_change();
}

function remove_edge(from, to, path) {
    let queues = app.nodes[from].parameters.destination_queues;
    let queue = queues[path];
    let to_index = queue.indexOf(to);
    if (to_index !== -1)
        queue.splice(to_index, 1);

    if (queue.length === 0)
        delete queues[path];
}

function add_edge(from, to, path) {
    if (!to.endsWith('-queue')) {
        to += '-queue';
    }
    let queues = app.nodes[from].parameters.destination_queues;
    let queue = path in queues ? queues[path] : (queues[path] = []);
    queue.push(to);
}
