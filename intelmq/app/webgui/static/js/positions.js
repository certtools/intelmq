// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
//
// SPDX-License-Identifier: AGPL-3.0-or-later

var app = app || {};

function generate_positions_conf() {
    var new_positions = app.network.getPositions();
    new_positions = sortObjectByPropertyName(new_positions);

    new_positions.settings = settings;
    return JSON.stringify(new_positions, undefined, 4);
}

function read_positions_conf(config) {
    if("settings" in config) { // reload settings
        settings = config.settings;
        if (settings.physics === null) {
            settings.physics = Object.keys(app.nodes).length < 40; // disable physics by default when there are more then 40 bots
        }
        delete config.settings;
    }
    return config;
}
