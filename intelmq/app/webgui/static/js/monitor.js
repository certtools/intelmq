// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>, 2020 Edvard Rejthar <github@edvard.cz>, 2021 Mikk Margus Möll <mikk@cert.ee>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

var ALL_BOTS = 'All Bots';
var bot_logs = {};
var bot_queues = {};
var path_names = {};
var reload_queues = null;
var reload_logs = null;
var app = app || {};
var buffered_bot = null;

var queue_overview = {}; // one-time queue overview to allow traversing
var $dq = $("#destination-queues");

load_configuration(() => {
    // refresh parameters panel when ready
    if (buffered_bot) {
        refresh_configuration_info(buffered_bot);
    }
});



$('#log-table').dataTable({
    lengthMenu: [[5, 10, 25, -1], [5, 10, 25, "All"]],
    pageLength: 10,
    order: [0, 'desc'],
    autoWidth: false,
    columns: ['date', 'bot_id', 'log_level', 'message', 'actions'].map(data => { return {data};})
});

window.onresize = redraw;

$(document).keydown(function (event) {
    if ($("#message-playground").is(":focus")) {
        if ($("[data-role=inject]").attr("data-checked") === "") {
            // when entered a char for first time ever, mark the "inject message" checkbox
            $("[data-role=inject]").prop("checked", true).attr("data-checked", true);
        }
        if (event.ctrlKey && event.keyCode === 13) {
            // ctrl+enter submits
            $("button[data-role=process]").click();
        }
    }
});

function redraw() {
    redraw_logs();
    redraw_queues();
}

function redraw_logs() {
    $('#log-table').dataTable().fnClearTable();

    if (bot_logs == {}) {
        $('#log-table').dataTable().fnAdjustColumnSizing();
        $('#log-table').dataTable().fnDraw();
        return;
    }

    for (let index in bot_logs) {
        let log_row = $.extend(true, {}, bot_logs[index]);
        let has_button = false;

        if (log_row.extended_message) {
            var buttons_cell = `<button type="submit" class="btn btn-default btn-xs" data-toggle="modal" data-target="#extended-message-modal" id="button-extended-message-${index}"><span class="glyphicon glyphicon-plus"></span></button>`;
            has_button = true;
            log_row.actions = buttons_cell;
        } else if (log_row.message.length > MESSAGE_LENGTH) {
            log_row.message = `${escape_html(log_row.message.slice(0, MESSAGE_LENGTH))}<strong>...</strong>`;
            buttons_cell = `<button type="submit" class="btn btn-default btn-xs" data-toggle="modal" data-target="#extended-message-modal" id="button-extended-message-${index}"><span class="glyphicon glyphicon-plus"></span></button>`;
            has_button = true;
            log_row.actions = buttons_cell;
        } else {
            log_row.actions = '';
        }


        log_row.DT_RowClass = LEVEL_CLASS[log_row.log_level];


        $('#log-table').dataTable().fnAddData(log_row);
        if (has_button) {
            var extended_message_func = message_index => show_extended_message(message_index);
            document.getElementById(`button-extended-message-${index}`).addEventListener('click', function (index) {
                return function () {
                    extended_message_func(index)
                }
            }(index))
        }
    }

    $('#log-table').dataTable().fnAdjustColumnSizing();
    $('#log-table').dataTable().fnDraw();
}

function redraw_queues() {
    let bot_id = getUrlParameter('bot_id') || ALL_BOTS;

    let source_queue_element = document.getElementById('source-queue');
    let internal_queue_element = document.getElementById('internal-queue');
    //let destination_queues_element = document.getElementById('destination-queues');

    source_queue_element.innerHTML = '';
    internal_queue_element.innerHTML = '';
    //destination_queues_element.innerHTML = '';

    let bot_info = {
        source_queues: {},
        destination_queues: {},
        fetched: true
    };

    if (bot_id === ALL_BOTS || !queue_overview.fetched) {
        for (let [bot_name, bot] of Object.entries(bot_queues)) {
            let source_queue = bot.source_queue;
            let destination_queues = bot.destination_queues;
            let internal_queue = bot.internal_queue;

            if (source_queue) {
                bot_info.destination_queues[source_queue[0]] = source_queue;
                bot_info.destination_queues[source_queue[0]].parent = bot_name;
            }

            if (internal_queue !== undefined) {
                let queue_name = `${bot_name}-queue-internal`;
                bot_info.destination_queues[queue_name] = [queue_name, internal_queue];
                bot_info.destination_queues[queue_name].parent = bot_name;
            }
        }
    }

    if (!queue_overview.fetched) {
        // we build queue_overview only once; on bot detail, we spare this block
        queue_overview = bot_info;
    }

    if (bot_id !== ALL_BOTS) {
        bot_info = bot_queues[bot_id];
    }
    if (bot_info) {
        if (bot_info.source_queue) {
            let source_queue = source_queue_element.insertRow();
            let cell0 = source_queue.insertCell(0);
            cell0.innerText = bot_info.source_queue[0];

            let cell1 = source_queue.insertCell(1);
            cell1.innerText = bot_info.source_queue[1];

            let buttons_cell = source_queue.insertCell(2);
            buttons_cell.appendChild(generateClearQueueButton(bot_info.source_queue[0]));
        }

        if (bot_info.internal_queue !== undefined) {
            let internal_queue = internal_queue_element.insertRow();
            let cell0 = internal_queue.insertCell(0);
            cell0.innerText = 'internal-queue';

            let cell1 = internal_queue.insertCell(1);
            cell1.innerText = bot_info.internal_queue;

            let buttons_cell = internal_queue.insertCell(2);
            buttons_cell.appendChild(generateClearQueueButton(`${bot_id}-queue-internal`));
        }

        let dst_queues = Object.values(bot_info.destination_queues).sort();

        for (let bot of dst_queues) {
            let [queue, count] = bot;
            if ($(`tr:eq(${bot}) td:eq(0)`, $dq).text() === queue) {
                // row exist, just update the count
                $(`tr:eq(${bot}) td:eq(2)`, $dq).text(count);
            } else {
                // for some reason, dst_queues from server changed from the table
                // let's find the table row
                let o = $("tr td:first-child", $dq).filter(function () {
                    return $(this).text() === queue;
                });
                if (o.length) { // successfully found
                    o.next().text(count);
                } else { // not present in the table
                    // make unknown queue a new row
                    let $tr = $("<tr/>").data("bot-id", queue_overview.destination_queues[queue].parent).appendTo($dq);
                    $("<td/>").appendTo($tr).text(queue).click(function () {
                        let selectBot = $(this).closest("tr").data("bot-id");
                        if (selectBot) {
                            select_bot(selectBot, true);
                        }
                    });
                    $("<td/>").appendTo($tr).text("");
                    $("<td/>").appendTo($tr).text(count);
                    $("<td/>").appendTo($tr).html(generateClearQueueButton(queue)); // regenerate thrash button
                }
                refresh_path_names();
            }
        }
    }
}

function generateClearQueueButton(queue_id) {
    let spanHolder = document.createElement('span');
    spanHolder.className = 'fa fa-trash-o';

    let clearQueueButton = document.createElement('button');
    clearQueueButton.queue = queue_id;
    clearQueueButton.type = 'submit';
    clearQueueButton.class = 'btn btn-default';
    clearQueueButton.title = 'Clear';
    clearQueueButton.appendChild(spanHolder);
    clearQueueButton.addEventListener("click", function (event) {
        clearQueue(this.queue);
    });

    return clearQueueButton;
}

function clearQueue(queue_id) {
    authenticatedGetJson(managementUrl('clear', `id=${queue_id}`))
            .done(function (data) {
                redraw_queues();
                $('#queues-panel-title').removeClass('waiting');
            })
            .fail(ajax_fail_callback(`Error clearing queue ${queue_id}`));
}

function load_bot_log() {
    $('#logs-panel-title').addClass('waiting');

    let number_of_lines = LOAD_X_LOG_LINES;

    let bot_id = getUrlParameter('bot_id') || ALL_BOTS;
    let level = document.getElementById('log-level-indicator').value;
    if(bot_id === ALL_BOTS) {
         return;
    }
    // NOTE: The URL to fetch the log used to be "...?scope=log&...".
    // It's now ".../getlog" instead of ".../log" because for some
    // reason, the client (at least the Firefox versions I tested) did
    // not even try to fetch the URL in the latter case. Switching from
    // "log" to "getlog" made it work.
    authenticatedGetJson(managementUrl('getlog', `id=${bot_id}&lines=${number_of_lines}&level=${level}`))
            .done(function (data) {
                if(JSON.stringify(data) != JSON.stringify(bot_logs)) { // redraw only if content changed
                    bot_logs = data;
                    redraw_logs();
                }
            })
            .fail(ajax_fail_callback('Error loading bot log information'))
            .always(() => {
                $('#logs-panel-title').removeClass('waiting');
                if (this instanceof Interval) {
                    this.blocking = false;
                }
            });
}

function load_bot_queues() {
    $('#queues-panel-title').addClass('waiting');
    authenticatedGetJson(managementUrl('queues'))
            .done(function (data) {
                bot_queues = data;
                redraw_queues();
                $('#queues-panel-title').removeClass('waiting');
            })
            .fail(ajax_fail_callback('Error loading bot queues information'))
            .always(() => {
                if (this instanceof Interval) {
                    this.blocking = false;
                }
            });
}

function select_bot(bot_id, history_push = false) {
    if (history_push) {
        window.history.pushState(null, null, MONITOR_BOT_URL.format(bot_id));
    }

    $("tr", $dq).remove(); // make destination table rebuild itself

    if (reload_queues) {
        reload_queues.stop();
    }

    if (reload_logs) {
        reload_logs.stop();
    }

    $('#monitor-target').text(bot_id);

    load_bot_queues();

    reload_queues = new Interval(load_bot_queues, RELOAD_QUEUES_EVERY * 1000, true);

    $("#destination-queues-table").addClass('highlightHovering');
    if (bot_id !== ALL_BOTS) {
        $("#logs-panel, #inspect-panel, #parameters-panel").css('display', 'block');
        $("#source-queue-table-div").css('display', 'block');
        $("#internal-queue-table-div").css('display', 'block');
        //$("#destination-queues-table").removeClass('highlightHovering');
        $("#destination-queues-table-div").removeClass().addClass('col-md-4'); // however, will be reset in refresh_path_names
        $("#destination-queue-header").text("Destination Queues");

        load_bot_log();
        reload_logs = new Interval(load_bot_log, RELOAD_LOGS_EVERY * 1000, true);

        // control buttons in inspect panel
        $("#inspect-panel .panel-heading .control-buttons").remove();
        $("#inspect-panel .panel-heading").prepend(generate_control_buttons(bot_id, false, load_bot_log, true));

        // connect to configuration panel
        $('#monitor-target').append(` <a title="show in configuration" href="configs.html#${escape(bot_id)}"><img src="./images/config.png" width="24" height="24" /></a>`);

    } else {
        $("#logs-panel, #inspect-panel, #parameters-panel").css('display', 'none');
        $("#source-queue-table-div").css('display', 'none');
        $("#internal-queue-table-div").css('display', 'none');
        //$("#destination-queues-table").addClass('highlightHovering');
        $("#destination-queues-table-div").removeClass().addClass('col-md-12');
        $("#destination-queue-header").text("Queue");
    }
    // refresh additional information
    refresh_configuration_info(bot_id);
}

function refresh_path_names() {
    let parent = $dq.parent();
    if ($.isEmptyObject(path_names)) {
        // expand the columns
        //parent.find("col:eq(1)").css("visibility", "collapse");
        parent.find("col:eq(1)").css("display", "none");
        $("td:nth-child(2), th:nth-child(2)", parent).css("display", "none");

        parent.find("th:eq(0)").removeClass().addClass("width-80");
        parent.find("th:eq(1)").removeClass();
        if ($("#destination-queues-table-div").hasClass('col-md-12')) {
            // in full width display of all bots, there is no need of another hassling
            return;
        }
        $("#destination-queues-table-div").removeClass("col-md-5").addClass("col-md-4");
        $("#internal-queue-table-div").removeClass("col-md-3").addClass("col-md-4");
        return;
    }

    // fold the columns to make more space on the line due to the Path column
    //parent.find("col:eq(1)").css("visibility", "inherit");
    //parent.find("col:eq(1)").css("display", "inherit");
    $("td:nth-child(2), th:nth-child(2)", parent).css("display", "revert");


    parent.find("th:eq(0)").removeClass().addClass("width-60");
    parent.find("th:eq(1)").addClass("width-20");
    $("#destination-queues-table-div").removeClass("col-md-4").addClass("col-md-5");
    $("#internal-queue-table-div").removeClass("col-md-4").addClass("col-md-3");

    $("tr td:first-child", $dq).each(function () {
        let path = path_names[$(this).text()] || null;
        let $el = $(this).next("td");
        $el.text(path || "_default");
        if (!path) {
            $el.css({color: "gray", "font-style": "italic"});
        }
    });
}

/**
 * Refresh information dependent on the loaded config files: parameters panel + named queues
 * Only when configuration has already been loaded.
 * @param {type} bot_id
 * @returns {undefined}
 */
function refresh_configuration_info(bot_id) {
    if (!app.nodes) {
        // we're not yet ready, buffer the bot for later
        buffered_bot = bot_id;
        return;
    }

    // search for named queue paths
    path_names = {};

    let bots = bot_id === ALL_BOTS ? Object.values(app.nodes) : [app.nodes[bot_id]];

    for (let node of bots) {
        for (let path in node.parameters.destination_queues) {
            if (path !== '_default') {
                for (let to of node.parameters.destination_queues[path]) {
                    path_names[to] = path;
                }
            }
        }
    }

    refresh_path_names();

    // refresh parameters panel
    let $panel = $("#parameters-panel .panel-body");
    $panel.text("");
    if (!app.nodes[bot_id] || !app.nodes[bot_id].parameters) {
        $panel.text("Failed to fetch the information.");
        return;
    }
    let params = app.nodes[bot_id].parameters;
    for (let [key, param] of Object.entries(params)) {
        if (typeof param !== 'string') { // display json/list instead of "[Object object]"
            param = JSON.stringify(param);
        }
        let $el = $(`<li><b>${escape_html(key)}</b>: ${escape_html(param)}</li>`);
        if (param && param.indexOf && param.indexOf(ALLOWED_PATH) === 0) {
            let url = `${LOAD_CONFIG_SCRIPT}?file=${param}`;
            authenticatedGetJson(url, data => {
                let html = "";
                if (data.directory) {
                    html += `<h3>Directory ${escape_html(data.directory)}</h3>`;
                }

                for (let file in data.files) {
                    let size = data.files[file].size ? `<a data-role=fetchlink href='${LOAD_CONFIG_SCRIPT}?fetch=1&file=${escape_html(data.files[file].path)}'>fetch ${escape_html(data.files[file].size)} B</a>` : "";
                    html += `<h4>File ${file}</h4>${size}`;
                    if (data.files[file].contents) {
                        html += `<pre>${escape_html(data.files[file].contents)}</pre>`;
                    }
                }
                $("<div/>", {html: html}).appendTo($el);
            });
        }
        $el.appendTo($panel);
    }
    if (!Object.keys(params).length) {
        $panel.text("No parameters.");
    }
}
$("#parameters-panel").on("click", "a[data-role=fetchlink]", function () {
    $.get($(this).attr("href"), data => {
        $(this).after(`<pre>${escape_html(data)}</pre>`).remove();
    });
    return false;
});

function show_extended_message(index) {
    let modal_body = document.getElementById('modal-body');

    let message = bot_logs[index].message;

    if (bot_logs[index].extended_message) {
        message += '<br>\n' +
                bot_logs[index].extended_message.replace(/\n/g, '<br>\n').replace(/ /g, '&nbsp;');
    }

    modal_body.innerHTML = message;
}

authenticatedGetJson(managementUrl('botnet', 'action=status'))
        .done(function (data) {
            let sidemenu = document.getElementById('side-menu');

            let select_bot_func = function (bot_id) {
                return function (event) {
                    event.preventDefault();
                    select_bot(bot_id, true);
                    return false;
                };
            };

            // Insert link for special item 'All Bots'
            let li_element = document.createElement('li');
            let link_element = document.createElement('a');
            link_element.innerText = ALL_BOTS;
            link_element.setAttribute('href', `#${MONITOR_BOT_URL.format(ALL_BOTS)}`);
            link_element.addEventListener('click', select_bot_func(ALL_BOTS));

            li_element.appendChild(link_element);
            sidemenu.appendChild(li_element);

            // Insert link for every bot
            bot_status = data;
            $(".control-buttons [data-role=control-status]").trigger("update");
            let bots_ids = Object.keys(data);
            bots_ids.sort();

            for (let index in bots_ids) {
                let bot_id = bots_ids[index];
                li_element = document.createElement('li');
                link_element = document.createElement('a');

                link_element.innerText = bot_id;
                link_element.setAttribute('href', `#${MONITOR_BOT_URL.format(bot_id)}`);
                link_element.addEventListener('click', select_bot_func(bot_id));

                li_element.appendChild(link_element);
                sidemenu.appendChild(li_element);
            }
        })
        .fail(ajax_fail_callback('Error loading botnet status'));



$(document).ready(popState);
window.addEventListener("popstate", popState);
document.addEventListener('DOMContentLoaded', function () {
    document.getElementById('log-level-indicator').addEventListener('change', load_bot_log);

    // Inspect panel functionality
    let $insp = $("#inspect-panel");
    $("button[data-role=clear]", $insp).click(function () {
        $("#message-playground").val("");
        $("#run-log").attr("rows", 3).val("");
    });
    $("button[data-role=get]",  $insp).click(() => run_command("message get", "get"));
    $("button[data-role=pop]",  $insp).click(() => run_command("message pop", "pop"));
    $("button[data-role=send]", $insp).click(() => run_command("message send", "send", $("#message-playground").val()));
    $("button[data-role=process]", $insp).click(function () {
        let msg;
        if ($("[data-role=inject]", $insp).prop("checked")) {
            if (!$("#message-playground").val()) {
                show_error("Can't inject message from above – you didn't write any message");
                $("#message-playground").focus();
                return false;
            }
            msg = $("#message-playground").val();
        }
        let dry = $("[data-role=dry]", $insp).prop("checked");
        let show = $("[data-role=show-sent]", $insp).prop("checked");
        run_command("process" + (show ? " --show-sent" : "") + (dry ? " --dryrun" : "") + (msg ? " --msg" : ""), "process", msg, dry, show);
    });
});

/**
 * For purpose of better learning curve, we build intelmq command here at client
 * (however we won't upload it on server, we prefer have a whitelisted set of commands due to security
 * @param {string} bot
 * @param {string} cmd
 * @param {type} msg
 * @param {type} dry
 * @returns {undefined}
 */
function run_command(display_cmd, cmd, msg = "", dry = false, show = false) {
    let bot_id = getUrlParameter('bot_id') || ALL_BOTS;
    let tmp = msg ? `'${msg.replaceAll("'", "'\\''")}'` : "";
    $("#command-show").show().text(`${CONTROLLER_CMD} run ${bot_id} ${display_cmd} ${tmp}`); //XX dry are not syntax-correct
    $("#run-log").val("loading...");
    $('#inspect-panel-title').addClass('waiting');
    let call = authenticatedAjax({
        method: "post",
        data: {msg},
        url: managementUrl('run', `bot=${bot_id}&cmd=${cmd}&dry=${dry}&show=${show}`),
    }).done(function (data) {
        // Parses the received data to message part and to log-only part
        let logs = [];
        let msg = [];
        let logging = logs;
        for (let line of data.split("\n")) {
            if (logging === logs) {
                if (line === "{") {
                    logging = msg;
                }
            } else {
                if (line === "}") {
                    msg.push(line);
                    logging = logs;
                    continue;
                }
            }

            logging.push(line); //write either to logs or msgs
        }
        if (msg.length) { // we won't rewrite an old message if nothing came
            $("#message-playground").attr("rows", msg.length).val(msg.join("\n"));
        }
        $("#run-log").attr("rows", logs.length).val(logs.join("\n"));
    }).fail(ajax_fail_callback('Error getting message'))
            .always(() => {
                $('#inspect-panel-title').removeClass('waiting');
                $("#run-log").data("call", null);
            });

    // informate user if there is a lag
    $("#run-log").data("call", call);
    setTimeout(() => {
        if ($("#run-log").data("call") === call) {
            $("#run-log").val("loading... or timeouting...");
        }
    }, 3000);
}


/**
 * Select correct bot when browsing in history or coming from an external link etc.
 */
function popState() {
    $("#run-log").val("");
    let bot_id = getUrlParameter('bot_id') || ALL_BOTS;
    if (typeof (bot_id) !== 'undefined') {
        //window.history.replaceState(null, null, MONITOR_BOT_URL.format(bot_id));
        select_bot(bot_id);
    } else {
        select_bot(ALL_BOTS);
    }
}
