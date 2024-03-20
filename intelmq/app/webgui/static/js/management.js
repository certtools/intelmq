// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

var BOT_STATUS_DEFINITION = BOT_STATUS_DEFINITION || {};
var BOT_CLASS_DEFINITION = BOT_CLASS_DEFINITION || {};
var bot_status = bot_status || {};
var botnet_status = botnet_status || {};
var reload_interval;

$('#bot-table').dataTable({
    lengthMenu: [[5, 10, 25, -1], [5, 10, 25, "All"]],
    pageLength: -1,
    columns: ['bot_id', 'bot_status', 'actions'].map(data => {return {data}}),
    createdRow: (row, data) => $("td:eq(2)", row).append(generate_control_buttons(data.bot_id, false, refresh_status)),

});

window.onresize = function () {
    $('#bot-table').dataTable().fnAdjustColumnSizing();
    $('#bot-table').dataTable().fnDraw();
};

var $bt = $('#bot-table');
$(function () {
    load_file(RUNTIME_FILE, config => read_runtime_conf(config));

    $bt.dataTable().fnClearTable();

    // generate control buttons for every panel
    $("#botnet-panels [data-botnet-group]").each(function () {
        $(this).find("h4").data().waiting_count = 0;
        $(".panel-body .panel-div", $(this)).after(generate_control_buttons(false, $(this).attr("data-botnet-group"), refresh_status, true));
    });

    // fetch info from server
    reload_interval = new Interval(() => {
        $('#botnet-panels [data-botnet-group=botnet] [data-url=status]').click();
    }, RELOAD_STATE_EVERY * 1000, true).call_now();

    //
    $bt.on("click", 'tr td:first-child', event => click_link(MONITOR_BOT_URL.format(event.target.innerText), event));
});


function refresh_status(bot, finished) {
    if (reload_interval) {
        reload_interval.stop();
    }

    // Refresh bot table
    let redraw_table = false;
    let pending = false; // any bot is in an unknown state
    for (let bot_id in bot_status) {
        let class_ = BOT_CLASS_DEFINITION[bot_status[bot_id]];
        let status = bot_status[bot_id];
        let $bot = $(`tr[data-bot-id=${bot_id}]`, $bt);
        if ($bot.length) {
            // row exist, just update the status
            if (!$bot.text() !== status) {// class of this bot changes (note that multiple statuses may share the same class ".warning")
                for (let state of Object.values(BOT_CLASS_DEFINITION)) { // remove any other status-class
                    $bot.removeClass(state);
                }
                $bot.addClass(class_);
                $("td:eq(1)", $bot).text(status);
            }
        } else {
            $bt.dataTable().api().row.add({
                bot_id,
                bot_status: status,
                actions: "",
                DT_RowClass: class_,
                DT_RowAttr: {"data-bot-id": bot_id}
            });
            redraw_table = true;
        }
        if (status === BOT_STATUS_DEFINITION.unknown) {
            pending = true;
        }

    }
    if (finished) {
        // If there is some unknown bots, we re-ask the server to get current information immediately, else re-start the fetching interval.
        // (in case of botnets of 100 bots, intelmqctl returns 'unknown' state when bot couldn't start/stop in time)
        if (pending) {
            reload_interval.call_now();
        } else {
            reload_interval.start();
        }
    }

    // If there is a new row in the table, we ll redraw
    if (redraw_table) {
        $bt.dataTable().fnAdjustColumnSizing();
        $bt.dataTable().fnDraw();
        $('#botnet-panels [data-botnet-group]').show(); // showed on the first run
    }


    // Analyze botnet panels
    let atLeastOneStopped = {};
    let atLeastOneRunning = {};
    for (let bot_id in bot_status) { // analyze all bots status
        if (bot_status[bot_id] === BOT_STATUS_DEFINITION.stopped || bot_status[bot_id] === BOT_STATUS_DEFINITION.unknown) {
            atLeastOneStopped.botnet = atLeastOneStopped[bot_definition[bot_id].groupname] = true;
        } else if (bot_status[bot_id] === BOT_STATUS_DEFINITION.running) {
            atLeastOneRunning.botnet = atLeastOneRunning[bot_definition[bot_id].groupname] = true;
        }
    }
    let get_group_status = function (stopped, running) {
        if (stopped && running || !stopped && !running) {
            return BOT_STATUS_DEFINITION.incomplete;
        } else if (stopped && !running) {
            return BOT_STATUS_DEFINITION.stopped;
        } else if (!stopped && running) {
            return BOT_STATUS_DEFINITION.running;
        }
    };

    // Highlight waiting icon of current panel if any operation is pending (we may click "start" and "stop", waiting both operations resolve)
    let $el;
    if (bot in botnet_status) { // bot button was clicked: highlight its panel (ex: Parsers)
        $el = $(this).closest(".panel").find("h4");
    } else { // panel button was clicked
        $el = $(`.panel[data-botnet-group=${bot_definition[bot].groupname}]`).find("h4");
    }
    $el.toggleClass("waiting", ($el.data().waiting_count += (finished === 0) ? 1 : -1) > 0);

    // Refresh botnet panels
    let waiting_total = 0;
    $("#botnet-panels > [data-botnet-group]").each(function () {
        waiting_total += $(this).find("h4").data().waiting_count;
        let botnet = $(this).attr("data-botnet-group");
        botnet_status[botnet] = get_group_status(atLeastOneStopped[botnet], atLeastOneRunning[botnet]);
        $('[data-role=control-status]', this).trigger("update");

        // due to esthetics, fetch the status-info to the line above
        if (($el = $(".control-buttons [data-role=control-status]", $(this)).clone())) {
            if ($el.text()) {
                $(".panel-div", $(this)).html("Status: " + ($el[0].outerHTML || '<span data-role="botnet-status" class="bg-warning">Unknown</span>'));
            }
        }
    });

    // Highlight "Whole Botnet Status" operation in any panel is pending
    $('#botnet-panels [data-botnet-group=botnet] h4').toggleClass('waiting', waiting_total > 0);
}
