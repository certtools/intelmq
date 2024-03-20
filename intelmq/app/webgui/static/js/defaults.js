// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>, 2020 Edvard Rejthar <github@edvard.cz>, 2021 Mikk Margus Möll <mikk@cert.ee>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

function generate_defaults_conf(defaults) {
    return JSON.stringify(sortObjectByPropertyName(defaults), undefined, 4);
}

function read_defaults_conf(config) {
    let global = {};

    for (let key in config.global) {
        try {
            global[key] = JSON.parse(config.global[key]);
        } catch (err) {
            global[key] = config.global[key];
        }
    }

    return global;
}

function remove_defaults(nodes) {
    for (let id in nodes) {
        delete nodes[id].defaults;
    }

    return nodes;
}

function get_reverse_nodes(dest_bot_id) {
    let out = [];
    let dest_bot = app.nodes[dest_bot_id];
    if (dest_bot === undefined) {
        // for example for newly configured bots
        return out;
    }

    let connected_nodes = app.network.getConnectedNodes(dest_bot_id);
    let queue_id = `${dest_bot_id}-queue`;
    let reverse_allowed_neighbors = REVERSE_ACCEPTED_NEIGHBORS[dest_bot.group];

    for (let src_bot of connected_nodes.map(src_bot_id => app.nodes[src_bot_id]).filter(src_bot => reverse_allowed_neighbors.includes(src_bot.group))) {
         for (let list of Object.values(src_bot.parameters.destination_queues)) {
             if (list.includes(queue_id)) {
                 out.push(src_bot.bot_id);
                 break;
             }
         }
    }

    return out;
}

function get_reverse_edges(dest_bot_id) {
    let out = [], queue_id = `${dest_bot_id}-queue`;
    for (let edge_id of app.network.getConnectedEdges(dest_bot_id)) {
        let [from, to, path] = from_edge_id(edge_id);
        if (to === queue_id) {
            out.push(edge_id);
        }
    }

    return out;
}

function to_edge_id(from, to, path) { // e.g HTTP-Collector|JSON-Parser-queue|_default
    return [from, to.replace(/-queue$/, ''), path].map(escape).join('|');
}

function from_edge_id(edge_id) {
    let [from, to, path] = edge_id.split('|').map(unescape);
    return [from, `${to}-queue`, path];
}

function gen_new_id(prefix) {
    if (!(prefix in app.nodes)) { // no need to add numeric suffix
        return prefix;
    }

    let i = 1, new_id;
    //reserve a new unique name
    do {
        new_id = `${prefix}-${++i}`;
    } while (new_id in app.nodes);

    return new_id;

}
