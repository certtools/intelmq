// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>, 2020 Edvard Rejthar <github@edvard.cz>, 2021 Mikk Margus Möll <mikk@cert.ee>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

var NETWORK_OPTIONS = NETWORK_OPTIONS || {};

class VisModel {
    constructor() {


        this.defaults = {};
        this.nodes = {};
        this.bots = {};

        this.network = null;
        this.network_container = null;
        this.network_data = {}; // we may update existing info in the network on the fly
        this.bot_before_altering = null;

        this.positions = null;
        this.options = NETWORK_OPTIONS;
    }
}

var app = new VisModel();

var popup = null;
var documentation = null;
var span = null;
var table = null;
var disabledKeys = ['group', 'name', 'module'];
var $manipulation, $saveButton; // jQuery of Vis control panel; elements reseted with network
var node = null;

var $EDIT_DEFAULT_BUTTON = $("#editDefaults");
var BORDER_TYPE_CLASSES = {
    DEFAULT: 'info',
    GENERIC: 'success',
    RUNTIME: 'warning',
}
var BORDER_TYPES = {
    DEFAULT: 'default',
    GENERIC: 'generic',
    RUNTIME: 'runtime',
    OTHERS: 'default',
}

var draggedElement = null;

var warn_on_close_tab = false;

$(window).on('hashchange', location.reload);

$(window).on('beforeunload', () => warn_on_close_tab ? "If you have not saved your work you'll lose the changes you have made. Do you want to continue?" : undefined);

function resize() {
    // Resize body
    let network_container = document.getElementById('network-container');
    network_container.style.height = `${window.innerHeight - network_container.offsetTop}px`;
    network_container.style.overflowX = "auto";
    network_container.style.overflowY = "auto";

    if (app.network !== null && app.network !== undefined) {
        app.network.redraw();
    }

    load_html_elements();
}

function load_html_elements() {
    // Load popup, span and table
    app.network_container = document.getElementById('network-container');
    app.network_container.addEventListener('drop', handleDrop);
    app.network_container.addEventListener('dragover', allowDrop);
    popup = document.getElementById("network-popUp");
    documentation = document.getElementById("documentationButton");
    span = document.getElementById('network-popUp-title');
    table = document.getElementById("network-popUp-fields");
}


function load_bots(config) {
    // Build side menu
    for (let bot_group of Object.keys(config).reverse()) {
        let $bot_group = $("#templates > ul.side-menu > li").clone().prependTo("#side-menu").css("border-bottom-color", GROUP_COLORS[bot_group][0]);
        $bot_group.find("> a").prepend(bot_group);
        let group = config[bot_group];
        for (let bot_name in group) {
            let bot = group[bot_name];
            let $bot = $bot_group.find("ul > li:first").clone().appendTo($("ul", $bot_group))
                .attr("title", bot.description)
                .attr("data-name", bot_name)
                .attr("data-group", bot_group)
                .click(() => {
                    if ($('#network-popUp').is(':visible')) {
                        // just creating a new bot
                        fill_bot(undefined, bot_group, bot_name);
                        return false;
                    }

                    // cycling amongst the bot instances
                    if (!$bot.data("cycled")) {
                        $bot.data("cycled", []);
                    }
                    let found = null;
                    for (let bot_node of Object.values(app.nodes)) {
                        if (bot_node.module === bot.module && $.inArray(bot_node.id, $bot.data("cycled")) === -1) {
                            $bot.data("cycled").push(bot_node.id);
                            found = bot_node.id;
                            break;
                        }
                    }
                    // not found or all bots cycled
                    if (!found && $bot.data("cycled").length) {
                        found = $bot.data("cycled")[0];
                        $bot.data("cycled", [found]); // reset cycling
                    }
                    if (found) {
                        fitNode(found);
                    } else {
                        show_error(`No instance of the ${bot_name} found. Drag the label to the plan to create one.`);
                    }
                    return false;
                })
                .on('dragstart', event => { // drag to create a new bot instance
                    app.network.addNodeMode();
                    draggedElement = {
                        bot_name: bot_name,
                        bot_group: bot_group
                    };
                    // necessary for firefox
                    event.originalEvent.dataTransfer.setData('text/plain', null);
                })
                .find("a").prepend(bot_name);


            if (app.bots[bot_group] === undefined) {
                app.bots[bot_group] = {};
            }

            app.bots[bot_group][bot_name] = {
                name: bot_name,
                group: bot_group,
                module: bot.module,
                description: bot.description,
                enabled: true,
                parameters: bot.parameters,
                run_mode: 'continuous'
            };

            for (let [parameter, value] of Object.entries(bot.parameters)) {
                app.bots[bot_group][bot_name].parameters[parameter] = value;
            }
        }
        $bot_group.find("ul li").first().remove(); // get rid of the HTML template
    }

    $('#side-menu').metisMenu({restart: true});
    $EDIT_DEFAULT_BUTTON.click(e => {
        create_form('Edit Defaults', $(e.target).attr("id"), undefined);
        fill_editDefault(app.defaults);
    });

    if (getUrlParameter("configuration") !== "new") {
        load_configuration();
    } else {
        draw();
        resize();
        set_pending_change();
    }
}

function fill_editDefault(data) {
    table.innerHTML = '';
    insertBorder(BORDER_TYPES.DEFAULT);
    for (let [key, value] of Object.entries(data)) {
        insertKeyValue(key, value, BORDER_TYPES.DEFAULT, true);
    }

    // to enable scroll bar
    popup.setAttribute('class', "with-bot");
}

function handleDrop(event) {
    // --- necessary for firefox
    if (event.preventDefault) {
        event.preventDefault();
    }
    if (event.stopPropagation) {
        event.stopPropagation();
    }
    // ---

    let domPointer = app.network.interactionHandler.getPointer({x: event.clientX, y: event.clientY});
    let canvasPointer = app.network.manipulation.canvas.DOMtoCanvas(domPointer);

    let clickData = {
        pointer: {
            canvas: {
                x: canvasPointer.x,
                y: canvasPointer.y
            }
        }
    };

    app.network.manipulation.temporaryEventFunctions[0].boundFunction(clickData);

    fill_bot(undefined, draggedElement.bot_group, draggedElement.bot_name);
}

function allowDrop(event) {
    event.preventDefault();
}


// Configuration files manipulation

function save_data_on_files() {
    if (!confirm("By clicking 'OK' you are replacing the configuration in your files by the one represented by the network on this page. Do you agree?")) {
        return;
    }

    app.nodes = remove_defaults(app.nodes);

    let reloadable = 0;
    let alert_error = (file, jqxhr, textStatus, error) => {
        show_error(`There was an error saving ${file}:\nStatus: ${textStatus}\nError: ${error}`);
    };
    let saveSucceeded = (response) => {
        if (++reloadable === 4) {

        }
        if (response === 'success') {
            return true;
        } else {
            alert(response);
            return false;
        }
    }

    // can't parallelize these due to a race condition from them both touching runtime.yaml; TODO lock file in backend?
    authenticatedAjax({type: "POST", url: `${RUNTIME_FILE}`, contentType: "application/json", data: generate_runtime_conf(app.nodes, app.defaults)})
    .done(saveSucceeded)
    .fail(() => alert_error('runtime', ...arguments))
    .then(() =>
            authenticatedAjax({type: "POST", url: `${POSITIONS_FILE}`, contentType: "application/json", data: generate_positions_conf()})
            .done(saveSucceeded)
            .fail(() => alert_error('positions', ...arguments) )
    )
    // all files were correctly saved
    .then(unset_pending_change);
}


// Prepare data from configuration files to be used in Vis

function convert_edges(nodes) {
    let new_edges = [], roundness = {};
    for (let node of Object.values(nodes)) {
        let from = node.bot_id;
        let edge_map = node.parameters.destination_queues;
        for (let path in edge_map) {
            for (let to of edge_map[path]) {
                let id = to_edge_id(from, to, path);
                let new_edge = {
                    id,
                    from,
                    to: to.replace(/-queue$/, ''),
                    label: path === '_default' ? undefined : path,
                };

                // if there is multiple edges between nodes we have to distinguish them manually, see https://github.com/almende/vis/issues/1957
                let hash = new_edge.from + new_edge.to;
                if (hash in roundness) {
                    roundness[hash] += 0.3;
                } else {
                    roundness[hash] = 0;
                }
                if (roundness[hash]) {
                    new_edge.smooth = {type: "curvedCCW", roundness: roundness[hash]};
                }

                new_edges.push(new_edge);
            }
        }
    }

    return new_edges;
}

function convert_nodes(nodes, includePositions) {
    let new_nodes = [];

    for (let node of nodes) {
        let new_node = {};
        new_node.id = node.bot_id;
        new_node.label = node.bot_id;
        new_node.group = node.group;

        if (includePositions === true) {
            try {
                let {x, y} = app.positions[node.bot_id];
                new_node.x = x;
                new_node.y = y;
            } catch (err) {
                console.error('positions in file are ignored:', err, node);
                show_error('Saved positions are not valid or not complete. The configuration has possibly been modified outside of the IntelMQ-Manager.');
                includePositions = false;
            }
        }

        new_nodes.push(new_node);
    }

    return new_nodes;
}

function fill_bot(id, group, name) {
    let bot;
    table.innerHTML = '';

    if (id === undefined) {
        bot = app.bots[group][name];

        name = bot.name.replace(/\ /g, '-').replace(/[^A-Za-z0-9-]/g, '');
        group = bot.group.replace(/\ /g, '-');
        let default_id = gen_new_id(`${name}-${group}`);
        bot.bot_id = bot.id = default_id;
        bot.defaults = {};

        for (let [key, value] of Object.entries(app.defaults).filter(([key, value]) => !(key in bot.parameters))) {
            bot.defaults[key] = value;
        }
    } else {
        bot = app.nodes[id];
    }

    app.bot_before_altering = bot;

    insertKeyValue('id', bot.bot_id, 'id', false);
    insertBorder(BORDER_TYPES.GENERIC);
    for (let [key, value] of Object.entries(bot).filter(([key, value]) => STARTUP_KEYS.includes(key))) {
        insertKeyValue(key, value, BORDER_TYPES.GENERIC, false);
    }
    insertBorder(BORDER_TYPES.RUNTIME);
    for (let [key, value] of Object.entries(bot.parameters).filter(([key, value]) => key !== 'destination_queues')) {
        insertKeyValue(key, value, BORDER_TYPES.RUNTIME, true);
    }

    const modulename = bot.module.replace(/\./g, "-").replace(/_/g, "-");
    documentation.href = `https://intelmq.readthedocs.org/en/maintenance/user/bots.html#${modulename}`;
    popup.setAttribute('class', "with-bot");
}

function insertBorder(border_type) {
    let new_row = table.insertRow(-1);
    let sectionCell1 = new_row.insertCell(0);
    let sectionCell2 = new_row.insertCell(1);
    let addButtonCell = new_row.insertCell(2);

    sectionCell1.setAttribute('id', 'border');
    sectionCell2.setAttribute('id', 'border');
    sectionCell1.innerHTML = border_type;
    sectionCell2.innerHTML = border_type;

    switch (border_type) {
        case BORDER_TYPES.GENERIC:
            new_row.setAttribute('class', BORDER_TYPE_CLASSES.GENERIC);
            break;
        case BORDER_TYPES.RUNTIME:
            new_row.setAttribute('class', BORDER_TYPE_CLASSES.RUNTIME);
            $(addButtonCell).append($("#templates > .new-key-btn").clone().click(addNewKey));
            new_row.setAttribute('id', border_type);
            break;
        case BORDER_TYPES.DEFAULT:
            new_row.setAttribute('class', BORDER_TYPE_CLASSES.DEFAULT);
            $(addButtonCell).append($("#templates > .new-key-btn").clone().click(addNewDefaultKey));
            new_row.setAttribute('id', border_type);
            break;
        default:
            new_row.setAttribute('class', BORDER_TYPE_CLASSES.OTHERS);
    }
}

function insertKeyValue(key, value, section, allowXButtons, insertAt) {
    let new_row = table.insertRow(insertAt === undefined ? -1 : insertAt);

    let keyCell = new_row.insertCell(0);
    let valueCell = new_row.insertCell(1);
    let xButtonCell = new_row.insertCell(2);
    let valueInput = document.createElement("input");

    keyCell.setAttribute('class', 'node-key');
    keyCell.setAttribute('id', section)
    valueCell.setAttribute('class', 'node-value');
    valueInput.setAttribute('type', 'text');
    valueInput.setAttribute('id', key);

    if (section === 'generic' && disabledKeys.includes(key) === true) {
        valueInput.setAttribute('disabled', "true");
    }

    let parameter_func = (action_function, argument) => action_function(argument);

    if (allowXButtons === true) {
        let xButton = document.createElement('button');
        let xButtonSpan = document.createElement('span');
        xButtonSpan.setAttribute('class', 'glyphicon glyphicon-remove-circle');
        xButton.setAttribute('class', 'btn btn-danger');
        xButton.setAttribute('title', 'delete parameter');
        xButton.addEventListener('click', () => parameter_func(deleteParameter, key));

        xButton.appendChild(xButtonSpan);
        xButtonCell.appendChild(xButton);
    }

    valueCell.appendChild(valueInput);

    keyCell.innerHTML = key;
    if (value !== null && typeof value === "object") {
        value = JSON.stringify(value);
    }
    if (value !== null) {
        valueInput.setAttribute('value', value);
    }
}

function resetToDefault(input_id) {
    $(`#${input_id}`)[0].value = app.defaults[input_id];
}

function deleteParameter(input_id) {
    let current_index = $(`#${input_id}`).closest('tr').index();
    table.deleteRow(current_index);
}

function addNewKey() {
    let $el = $("#templates .modal-add-new-key").clone();
    popupModal("Add key", $el, () => {
        let current_index = $(`#${BORDER_TYPES.RUNTIME}`).index();
        let $key = $el.find("[name=newKeyInput]");
        let val = $el.find("[name=newValueInput]").val();

        if (!PARAM_KEY_REGEX.test($key.val())) {
            show_error("Parameter names can only be composed of numbers, letters, hiphens and underscores");
            $key.focus();
            return false;
        } else {
            // inserts new value and focus the field
            insertKeyValue($key.val(), val, BORDER_TYPES.RUNTIME, true, current_index + 1);
            // a bootstrap guru or somebody might want to rewrite this line without setTimeout
            setTimeout(() => $('#network-popUp .new-key-btn').closest("tr").next("tr").find("input").focus(), 300);
        }
    });
}
// same as above, with another border type
function addNewDefaultKey() {
    let $el = $("#templates .modal-add-new-key").clone();
    popupModal("Add key", $el, () => {
        let current_index = $(`#${BORDER_TYPES.RUNTIME}`).index();
        let $key = $el.find("[name=newKeyInput]");
        let val = $el.find("[name=newValueInput]").val();

        if (!PARAM_KEY_REGEX.test($key.val())) {
            show_error("Parameter names can only be composed of numbers, letters, hiphens and underscores");
            $key.focus();
            return false;
        } else {
            // inserts new value and focus the field
            insertKeyValue($key.val(), val, BORDER_TYPES.DEFAULT, true, current_index + 1);
            // a bootstrap guru or somebody might want to rewrite this line without setTimeout
            setTimeout(() => $('#network-popUp .new-key-btn').closest("tr").next("tr").find("input").focus(), 300);
        }
    });
}

$(document).keydown(function (event) {
    if (event.keyCode === 27) {
        let $el;
        if (($el = $("body > .modal:not([data-hiding])")).length) {
            // close the most recent modal
            $el.last().attr("data-hiding", true).modal('hide');
            setTimeout(() => $("body > .modal[data-hiding]").first().remove(), 300);
        } else if ($('#network-popUp').is(':visible')) {
            $('#network-popUp-cancel').click();
        }
    }
    if (event.keyCode === 13 && $('#network-popUp').is(':visible') && $('#network-popUp :focus').length) {
        // till network popup is not unified with the popupModal function that can handle Enter by default,
        // let's make it possible to hit "Ok" by Enter as in any standard form
        $('#network-popUp-ok').click();
    }
});

function saveDefaults_tmp(data, callback) {
    app.defaults = {};
    saveFormData();
    set_pending_change();
    clearPopUp(data, callback);
}

function saveFormData() {
    for (let i = 0; i < table.rows.length; i++) {
        let keyCell = table.rows[i].cells[0];
        let valueCell = table.rows[i].cells[1];
        let valueInput = valueCell.getElementsByTagName('input')[0];

        if (valueInput === undefined)
            continue;

        let key = keyCell.innerText;
        let value = null;

        try {
            value = JSON.parse(valueInput.value);
        } catch (err) {
            value = valueInput.value;
        }

        switch (keyCell.id) {
            case 'id':
                node.bot_id = value;
                break;
            case 'generic':
                node[key] = value;
                break;
            case 'runtime':
                node.parameters[key] = value;
                break;
            case 'border':
                break;
            case 'default':
                app.defaults[key] = value;
                break;
            default:
                node.defaults[key] = value;
        }
    }
}

function saveData(data, callback) {
    node = {parameters: {}, defaults: {}};

    saveFormData();

    // check inputs beeing valid
    if (node.bot_id === '' && node.group === '') {
        show_error('fields id and group must not be empty!');
        return;
    }

    if (!BOT_ID_REGEX.test(node.bot_id)) {
        show_error("Bot ID's can only be composed of numbers, letters and hyphens");
        return;
    }

    let current_id = node.bot_id, old_id = app.bot_before_altering.bot_id;

    let old_bot = app.nodes[old_id];
    node.parameters.destination_queues = old_bot ? old_bot.parameters.destination_queues : {};

    if (current_id !== old_id) {
        if (current_id in app.nodes) {
            alert("A bot with this ID already exists, please select a different ID");
            return;
        }

        if (old_id in app.nodes) {
            if (!confirm("You have edited the bot's ID. Proceed with the operation?")) {
                return;
            }

            app.positions[current_id] = app.positions[old_id];
            app.nodes[current_id] = node;
            delete app.positions[old_id];

            app.network_data.nodes.add(convert_nodes([node], true));

            // recreate reverse edges
            for (let edge_id of get_reverse_edges(old_id)) {
                let [from, to, path] = from_edge_id(edge_id);
                let list = app.nodes[from].parameters.destination_queues[path];
                let to_index = list.indexOf(`${old_id}-queue`);

                list[to_index] = `${current_id}-queue`;

                let new_edge_id = to_edge_id(from, current_id, path);
                if (path === '_default') {
                    path = undefined;
                }

                app.network_data.edges.remove({id: edge_id});
                app.network_data.edges.add({id: new_edge_id, from, to: current_id, label: path});
            }

            // recreate forward edges
            for (let [path, path_l] of Object.entries(node.parameters.destination_queues)) {
                for (let to of path_l) {
                    app.network_data.edges.add({
                        id: to_edge_id(current_id, to, path),
                        from: current_id,
                        to: to.replace(/-queue$/, ''),
                        label: path === '_default' ? undefined : path
                    });
                }
            }

            delete app.nodes[old_id];
            app.network_data.nodes.remove(old_id);
        }
    }


    // switch parameters and defaults
    if ('parameters' in node) {
        for (let parameterKey in node.parameters) {
            if (
                node.parameters[parameterKey] !== app.bot_before_altering.parameters[parameterKey]
                && parameterKey in app.defaults
                && node.parameters[parameterKey] === app.defaults[parameterKey]
            ) {
                swapToDefaults(node, parameterKey);
            }
        }
    }

    if ('defaults' in node) {
        for (let defaultsKey in node.defaults) {
            if (node.defaults[defaultsKey] !== app.defaults[defaultsKey]) {
                swapToParameters(node, defaultsKey);
            }
        }
    }

    data.bot_id = node.bot_id;
    data.id = node.bot_id;
    data.label = node.bot_id;
    data.group = node.group;
    data.level = GROUP_LEVELS[data.group];
    data.title = JSON.stringify(node, undefined, 2).replace(/\n/g, '\n<br>').replace(/ /g, "&nbsp;");

    app.nodes[node.bot_id] = node;

    set_pending_change();
    clearPopUp(data, callback);
}

function swapToParameters(node, key) {
    node.parameters[key] = node.defaults[key];
    delete node.defaults[key];
}

function swapToDefaults(node, key) {
    node.defaults[key] = node.parameters[key];
    delete node.parameters[key];
}


/**
 * Popups a custom modal window containing the given body.
 * @example popupModal("Title", $input, () => {$input.val();})
 */
function popupModal(title, body, callback) {
    let $el = $("#templates > .modal").clone().appendTo("body");
    $(".modal-title", $el).text(title);
    $(".modal-body", $el).html(body);
    $el.modal({keyboard: false}).on('shown.bs.modal', e => {
        let $ee;
        if (($ee = $('input,textarea,button', $(".modal-body", e.target)).first())) {
            $ee.focus();
        }
    });
    return $el.on('submit', 'form', e => {
        if (callback() !== false) {
            $(e.target).closest(".modal").modal('hide');
        }
        return false;
    });
}

function create_form(title, data, callback) {
    span.innerHTML = title;

    let okButton = document.getElementById('network-popUp-ok');
    let cancelButton = document.getElementById('network-popUp-cancel');

    if (data === $EDIT_DEFAULT_BUTTON.attr("id")) {
        okButton.onclick = saveDefaults_tmp.bind(window, data, callback);
    } else {
        okButton.onclick = saveData.bind(window, data, callback);
    }

    cancelButton.onclick = clearPopUp.bind(window, data, callback);

    table.innerHTML = "<p>Please select one of the bots on the left</p>";
    popup.style.display = 'block';
    popup.setAttribute('class', "without-bot");
}

function clearPopUp(data, callback) {
    let okButton = document.getElementById('network-popUp-ok');
    let cancelButton = document.getElementById('network-popUp-cancel');
    okButton.onclick = null;
    cancelButton.onclick = null;

    popup.style.display = 'none';
    span.innerHTML = "";

    for (let i = table.rows.length - 1; i >= 0; i--) {
        let position = table.rows[i].rowIndex;

        if (position >= CORE_FIELDS) {
            table.deleteRow(position);
        } else {
            table.rows[i].setAttribute('value', '');
        }
    }

    popup.setAttribute('class', "without-bot");
    if ((callback !== undefined) && (data.label !== 'new')) {
        callback(data);
    }
}

function redrawNetwork() {
    app.options.layout.randomSeed = Math.round(Math.random() * 1000000);
    app.network.destroy();
    app.network = null;
    initNetwork(false);
    set_pending_change();
}

function draw() {
    load_html_elements();

    if (getUrlParameter("configuration") === "new") {
        app.nodes = {};
    }
    initNetwork();
    if (window.location.hash) {
        let node = window.location.hash.substr(1);
        setTimeout(() => { // doesnt work immediately, I don't know why. Maybe a js guru would bind to visjs onready if that exists or sth.
            try {
                fitNode(node);
            } catch (e) {
                show_error(`Bot instance ${node} not found in the current configuration.`);
            }
        }, 100);


    }
}

function fitNode(nodeId) {
    app.network.fit({nodes: [nodeId]});
    app.network.selectNodes([nodeId], true);
    app.network.manipulation.showManipulatorToolbar();
}

function initNetwork(includePositions = true) {
    app.network_data = {
        nodes: new vis.DataSet(convert_nodes(Object.values(app.nodes), includePositions)),
        edges: new vis.DataSet(convert_edges(app.nodes))
    };

    app.network = new vis.Network(app.network_container, app.network_data, app.options);
    $manipulation = $(".vis-manipulation");

    // rename some menu buttons (because we couldn't do that earlier)
    app.network.options.locales.en.addNode = "Add Bot";
    app.network.options.locales.en.addEdge = "Add Queue";
    app.network.options.locales.en.editNode = "Edit Bot";
    app.network.options.locales.en.del = "Delete";

    // 'Live' button (by default on when botnet is not too big) and 'Physics' button
    // initially stopped
    let reload_queues = (new Interval(load_live_info, RELOAD_QUEUES_EVERY * 1000, true)).stop();
    app.network.setOptions({physics: false});

    //
    // add custom button to the side menu
    //

    $("#templates .network-right-menu").clone().insertAfter($manipulation);
    let $nc = $("#network-container");
    $(".vis-live-toggle", $nc).click(e => {
        $(e.target).toggleClass("running", !reload_queues.running);
        reload_queues.toggle(!reload_queues.running);
    }).click();
    let physics_running = true;
    $(".vis-physics-toggle", $nc).click(e => {
        $(e.target).toggleClass("running");
        app.network.setOptions({physics: (physics_running = !physics_running)});
    });

    // 'Save Configuration' button blinks and lists all the bots that should be reloaded after successful save.
    $saveButton = $("#vis-save", $nc);
    $saveButton.children().on('click', save_data_on_files);
    $saveButton.data("reloadables", []);
    $saveButton.blinkOnce = function() {
        $($saveButton).addClass('blinking-once');
        setTimeout(() => $($saveButton).removeClass('blinking-once'), 2000);
    }
    $saveButton.blinking = function (bot_id = null) {
        $($saveButton).addClass('vis-save-blinking')
        if (bot_id) {
            $($saveButton).data("reloadables").push(bot_id);
        }
    };
    $saveButton.unblinking = function () {
        $($saveButton).removeClass('vis-save-blinking');
        let promises = [];
        let bots = $.unique($($saveButton).data("reloadables"));
        for (let bot_id of bots) {
            let url = managementUrl("bot", `action=reload&id=${bot_id}`);
            promises.push(authenticatedGetJson(url));
        }
        if (promises.length) {
            Promise.all(promises).then(() => {
                show_error(`Reloaded bots: ${bots.join(", ")}`);
                bots.length = 0;
            });
        }
    };

    let allow_blinking_once = false; // Save Configuration button will not blink when a button is clicked now automatically
    // list of button callbacks in form ["button/settings name"] => function called when clicked receives true/false according to the clicked state
    let callbacks = [
        ["live", val => reload_queues[val ? "start" : "stop"]()],
        ["physics", val => app.network.setOptions({physics: val})],
    ];
    for (let [name, fn] of callbacks) {
        let $el = $(`.vis-${name}-toggle`, $nc).click(e => {
            // button click will callback and blinks Save Configuration button few times
            fn(settings[name] = !settings[name]);
            $(e.target).toggleClass("running", settings[name]);

            if (allow_blinking_once) {
                $saveButton.blinkOnce();
            }
        });
        // initially turn on/off buttons according to the server-stored settings
        settings[name] = !settings[name];
        $el.click();
    }
    allow_blinking_once = true;

    // 'Clear Configuration' button
    $("#vis-clear").children().on('click', event => window.location.assign('configs.html?configuration=new'));

    // 'Redraw Botnet' button
    $("#vis-redraw").children().on('click', event => redrawNetwork());

    //
    // add custom menu buttons
    // (done by extending self the visjs function, responsible for menu creation
    // so that we are sure our buttons are persistent when vis menu changes)
    //
    app.network.manipulation._showManipulatorToolbar = app.network.manipulation.showManipulatorToolbar;
    app.network.manipulation.showManipulatorToolbar = function () {
        // call the parent function that builds the default menu
        app.network.manipulation._showManipulatorToolbar.call(app.network.manipulation);

        // enable 'Edit defaults' button
        $EDIT_DEFAULT_BUTTON.prop('disabled', false);

        // clicking on 'Add Bot', 'Add Queues' etc buttons disables 'Edit defaults' button
        let fn = () => $EDIT_DEFAULT_BUTTON.prop('disabled', true);
        $(".vis-add", $manipulation).on("pointerdown", fn);
        let $el = $(".vis-edit", $manipulation);
        if ($el.length) { // 'Edit Bot' button is visible only when there is a bot selected
            $el.on("pointerdown", fn);
        }

        // 'Monitor' and 'Duplicate' buttons appear when there is a single node selected
        let nodes = app.network.getSelectedNodes();
        if (nodes.length === 1) { // a bot is focused
            let bot = nodes[0];
            $("#templates .network-node-menu").clone().appendTo($manipulation);
            $(".monitor-button", $manipulation).click((event) => {
                return click_link(MONITOR_BOT_URL.format(bot), event);
            }).find("a").attr("href", MONITOR_BOT_URL.format(bot));
            $(".duplicate-button", $manipulation).click(() => {
                duplicateNode(app, bot);
            }).insertBefore($(".vis-add").hide());

            // insert start/stop buttons
            $(".monitor-button", $manipulation).before(generate_control_buttons(bot, false, refresh_color, true));
        } else {
            let edges = app.network.getSelectedEdges();
            if (edges.length === 1) {
                $("#templates .network-edge-menu").clone().appendTo($manipulation);
                $(".vis-edit", $manipulation).click(() => {
                    editPath(app, edges[0]);
                }).insertBefore($(".vis-delete"));
            }
        }
        // refresh shortcuts
        // (it is so hard to click on the 'Add Node' button we rather register click event)
        // We use 't' for 'Add bot' and 'Duplicate' because that's a common letter.

        let shortcuts = [
            ['t', 'add', 'addNodeMode'],
            ['q', 'connect', 'addEdgeMode'],
            ['d', 'delete', 'deleteSelected'],
            ['e', 'edit', 'editNode'],
        ];

        for (let [letter, tag, callback_name] in shortcuts) {
            $(`.vis-${tag} .vis-label`, $manipulation).attr('data-accesskey', letter).click(app.network[callback_name]);
        }

        accesskeyfie();
    };
    // redraw immediately so that even the first click on the network is aware of that new monkeypatched function
    app.network.manipulation.showManipulatorToolbar();

    // double click action trigger editation
    app.network.on("doubleClick", active => {
        if (active.nodes.length === 1) {
            let ev = document.createEvent('MouseEvent'); // vis-js button need to be clicked this hard way
            ev.initEvent("pointerdown", true, true);
            $(".vis-edit", $manipulation).get()[0].dispatchEvent(ev);
        }
        if (active.edges.length === 1) {
            $(".vis-edit", $manipulation).click();
        }
    });
    /* right button ready for any feature request:
     app.network.on("oncontext", (active)=>{
     let nodeId = app.network.getNodeAt(active.pointer.DOM);
     // what this should do? :)
     });
     */

}

// INTELMQ

/*
 * Application entry point
 */

// Dynamically load available bots
load_file(BOTS_FILE, load_bots);

// Dynamically adapt to fit screen
window.onresize = resize;

/**
 * This function fetches the current info and updates bot nodes on the graph
 */
function refresh_color(bot) {
    if (bot_status_previous[bot] !== bot_status[bot]) { // status changed since last time

        // we use light colour if we expect bot will be running
        // (when reloading from stopped state bot will not be running)
        let col = GROUP_COLORS[app.nodes[bot].group][[
            BOT_STATUS_DEFINITION.running,
            BOT_STATUS_DEFINITION.starting,
            BOT_STATUS_DEFINITION.restarting,
            bot_status_previous[bot] === BOT_STATUS_DEFINITION.running ? BOT_STATUS_DEFINITION.reloading : 0
        ].includes(bot_status[bot]) ? 0 : 1];

        // change bot color if needed
        if (app.network_data.nodes.get([bot])[0].color !== col) {
            app.network_data.nodes.update({id: bot, color: col});
        }

        // we dash the border if the status has to be changed (not running or stopping) or is faulty (error, incomplete)
        if ([BOT_STATUS_DEFINITION.running, BOT_STATUS_DEFINITION.stopped].indexOf(bot_status[bot]) === -1) {
            app.network_data.nodes.update({id: bot, shapeProperties: {borderDashes: [5, 5]}})
        } else if ([BOT_STATUS_DEFINITION.running, BOT_STATUS_DEFINITION.stopped, undefined].indexOf(bot_status_previous[bot]) === -1) {
            // we remove dash border since bot has been in a dash-border state and is no more
            // (that means that bot wasn't either in a running, stopped or initially undefined state)
            app.network_data.nodes.update({id: bot, shapeProperties: {borderDashes: false}});
        }

        bot_status_previous[bot] = bot_status[bot];
    }
}

function load_live_info() {
    $(".navbar").addClass('waiting');
    return authenticatedGetJson(managementUrl('queues-and-status'))
        .done(data => {
            let bot_queues;
            [bot_queues, bot_status] = data;

            for (let [bot, bot_data] of Object.entries(bot_queues)) {
                if ("source_queue" in bot_data) {
                    // we skip bots without source queue (collectors)
                    // Assume an empty internal queue if no data is given (The AMQP pipeline does not have/need internal queues)
                    let c = bot_data.source_queue[1] + (bot_data.internal_queue || 0);
                    let label = (c > 0) ? `${bot}\n${c}✉` : bot;
                    let appbot = app.network_data.nodes.get(bot);
                    if (appbot === null) {
                        show_error(`Non-existent bot ${bot} in pipelines.`);
                    } else if (label !== appbot.label) {
                        // update queue count on bot label
                        app.network_data.nodes.update({id: bot, label});
                    }
                } else {
                    // https://github.com/certtools/intelmq-manager/issues/158
                    app.network_data.nodes.update({id: bot, label: bot});
                }
            }
            for (let bot in bot_status) {
                // bots that are not running are grim coloured
                refresh_color(bot);
            }
        })
        .fail(ajax_fail_callback('Error loading bot queues information'))
        .always(() => {
            $(".navbar").removeClass('waiting');
            this.blocking = false;
        });
}

function set_pending_change(bot_id = null) {
    $saveButton.blinking(bot_id);
    warn_on_close_tab = true;
}

function unset_pending_change() {
    $saveButton.unblinking();
    warn_on_close_tab = false;
}
