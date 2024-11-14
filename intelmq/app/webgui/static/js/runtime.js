// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

var app = {}; // will be later redefined as a VisModel object or any other object (used in Configuration and Monitor tab)

//TODO: add global
function generate_runtime_conf(nodes, defaults) {

    let tmp_nodes = nodes;
    tmp_nodes.global = defaults;

    sortObjectByPropertyName(tmp_nodes);
    for (let id in tmp_nodes) {
        let node = tmp_nodes[id];
        delete node.id;
        if ('parameters' in node) {
            sortObjectByPropertyName(node.parameters);
        }
        sortObjectByPropertyName(node);
    }

    return JSON.stringify(tmp_nodes, undefined, 4);
}

function read_runtime_conf(config) {
    bot_definition = config;
    let nodes = {};
    for (let bot_id in config) {
	if (bot_id != 'global') {
            bot_definition[bot_id].groupname = GROUPNAME_TO_GROUP[bot_definition[bot_id].group]; // translate ex: `Parser` to `parsers`
            let bot = config[bot_id];
            bot.bot_id = bot_id;

            if (!('enabled' in bot)) {
                bot.enabled = true;
            }

            if (!('run_mode' in bot)) {
                bot.run_mode = 'continuous';
            }

            if (bot.parameters.destination_queues === undefined) {
                bot.parameters.destination_queues = {};
            }

            nodes[bot_id] = bot;
	}
    }

    return nodes;
}

function load_file(url, callback) {
    let escaped_url = escape_html(url);
    authenticatedGetJson(url)
            .done(function (json) {
                try {
                    callback(json);
                }
                catch(e) {
                    // don't bother to display error, I think the problem will be clearly seen with the resource itself, not within the processing
                    console.log(e);
                    show_error(`Failed to load config file properly <a class="command" href="${escaped_url}">${escaped_url}</a>.`, true);
                }
            })
            .fail(function (jqxhr, textStatus, error) {
                let err = escape_html(`${textStatus}, ${error}`);
                show_error(`Get an error <b>${err}</b> when trying to obtain config file properly <a class="command" href="${escaped_url}">${escaped_url}</a>.`, true);
                callback({});
            });
}


// Configuration files fetching
function load_configuration(callback = () => {}) {
        load_file(RUNTIME_FILE, (config) => {
            app.defaults = read_defaults_conf(config);
            app.nodes = read_runtime_conf(config);
            if (typeof read_positions_conf !== "undefined") { // skipped on Monitor tab
                load_file(POSITIONS_FILE, (config) => {
                    app.positions = read_positions_conf(config);
                    draw();
                    resize();

                    callback();
                });
            } else {
                callback();
            }
        });
}
