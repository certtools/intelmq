// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>, 2020 Edvard Rejthar <github@edvard.cz>, 2021 Mikk Margus Möll <mikk@cert.ee>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

var CORE_FIELDS = 5;

var ACCEPTED_NEIGHBORS = {
    Collector: ['Parser', 'Expert', 'Output'],
    Parser: ['Expert', 'Output'],
    Expert: ['Parser', 'Expert', 'Output'],
    Output: []
}

var REVERSE_ACCEPTED_NEIGHBORS = Object.fromEntries(Object.keys(ACCEPTED_NEIGHBORS).map(key => [key, []]));

for (let [from, to_list] of Object.entries(ACCEPTED_NEIGHBORS)) {
    for (let to of to_list) {
        REVERSE_ACCEPTED_NEIGHBORS[to].push(from);
    }
}

var CAUTIOUS_NEIGHBORS = {
    Collector: ['Expert'],
    Expert: ['Parser']
}

var GROUP_LEVELS = {
    Collector: 0,
    Parser: 1,
    Expert: 2,
    Output: 3
};
var GROUPNAME_TO_GROUP = {
    Collector: "collectors",
    Parser: "parsers",
    Expert: "experts",
    Output: "outputs"
};

/**
 * 1st value is default color of running bot, latter of a stopped bot
 */
var GROUP_COLORS = {
    Collector: ['#ff6666', '#cc6666'],
    Parser: ['#66ff66', '#66cc66'],
    Expert: ['#66a3ff', '#66a3aa'],
    Output: ['#ffff66', '#cccc66']
}

var LEVEL_CLASS = {
    DEBUG: 'success',
    INFO: 'info',
    WARNING: 'warning',
    ERROR: 'danger',
    CRITICAL: 'danger'
}

var STARTUP_KEYS = ['group', 'name', 'module', 'description', 'enabled', 'run_mode'];

var BOT_ID_REGEX = /^[0-9a-zA-Z.-]+$/;
var PARAM_KEY_REGEX = /^[0-9a-zA-Z._-]+$/;

var LOAD_CONFIG_SCRIPT = API + "config";
var MANAGEMENT_SCRIPT = API + "controller";

var BOTS_FILE = API + "bots";
var HARMONIZATION_FILE = API + "harmonization";
var RUNTIME_FILE = API + "runtime";
var POSITIONS_FILE = API + "positions";

var RELOAD_QUEUES_EVERY = 1; /* 1 seconds */
var RELOAD_LOGS_EVERY = 3; /* 3 seconds */
var RELOAD_STATE_EVERY = 3; /* 3 seconds */
var LOAD_X_LOG_LINES = 30;

var MESSAGE_LENGTH = 200;

var MONITOR_BOT_URL = "monitor.html?bot_id={0}";

var page_is_exiting = false;

var settings = {
    physics: null, // by default, physics is on depending on bot count
    live: true, // by default on
};

$(window).on('unload', () => page_is_exiting = true);

function sortObjectByPropertyName(obj) {
    return Object.keys(obj).sort().reduce((c, d) => (c[d] = obj[d], c), {});
}

// String formatting function usage "string {0}".format("1") => "string 1"
if (!String.prototype.format) {
    String.prototype.format = function () {
        let args = arguments;
        return this.replace(/{(\d+)}/g, (match, number) => typeof args[number] === 'undefined' ? match : args[number]);
    };
}

/*
 * error reporting
 */
let lw_tips = new Set();
$(function () {
    let $lw = $("#log-window");
    let closeFn = () => {
        $lw.hide();
        $(".contents", $lw).html("");
        lw_tips.clear(); // no tips displayed
        return false;
    };

    $lw.on("click", e => { // clicking enlarges but not shrinks so that we may copy the text
        let btn = $(e.target);
        if (!btn.hasClass("extended")) {
            btn.toggleClass("extended");

            //$(".alert", this).prependTo(btn);

            $(document).on('keydown.close-log-window', event => {
                if (event.key == "Escape") {
                    $(document).off('keydown.close-log-window');
                    $lw.removeClass("extended");
                }
            });
        }
    });
    $("#log-window [role=close]").click(closeFn);
});

function show_error(string, permit_html=false) {
    if (!permit_html) {
        string = escape_html(string);
    }

    let d = new Date();
    let time = new Date().toLocaleTimeString().replace(/:\d+ /, ' ');
    let $lwc = $("#log-window .contents");
    let $el = $(`<p><span>${time}</span> <span></span> <span>${string}</span></p>`);
    let found = false;
    $("p", $lwc).each((i, v) => {
        if ($("span:eq(2)", $(v)).text() === $("span:eq(2)", $el).text()) {
            // we've seen this message before
            found = true;
            // put it in front of the other errors
            // only if the error window is not expanded (so that it does not shuffle when the user read the details)
            if (!$(v).closest("#log-window").hasClass("extended")) {
                $(v).prependTo($lwc);
            }
            //blink
            let blink_e = v.children[0];
            $(blink_e, $(v)).text(time).stop().animate({opacity: 0.1}, 100, () => {
                $(blink_e).animate({opacity: 1}, 100);
            });
            // increment 'seen' counter
            let counter = parseInt($("span:eq(1)", $(v)).text()) || 1;
            $("span:eq(1)", $(v)).text(`${counter + 1}×`);
            return false;
        }
    });
    if (!found) {
        $("#log-window").show().find(".contents").prepend($el);
    }
    /*if(!page_is_exiting) {
     alert(string);
     }*/
}


function ajax_fail_callback(str) {
    return function (jqXHR, textStatus, message) {
        if (textStatus === "timeout") {
            // this is just a timeout, no other info needed
            show_error(`${str} timeout`);
            return;
        }
        if (jqXHR.status === 0) { // page refreshed before ajax finished
            return;
        }

        let command = "", tip = "", report = "";
        try {
            let data = JSON.parse(jqXHR.responseText);
            report = data.message;
            command = ` <span class='command'>${escape_html(data.command)}</span>`;
            if (data.tip && !lw_tips.has(data.tip)) {
                // display the tip if not yet displayed on the screen
                lw_tips.add(data.tip);
                tip = ` <div class='alert alert-info'>TIP: ${escape_html(data.ip)}</div>`;
            }
            if (message === "Internal Server Error") {
                message = ""; // this is expected since we generated this in PHP when an error was spot, ignore
            }
        } catch (e) {
            report = jqXHR.responseText;
        }
        if (report) {
            // include full report but truncate the length to 2000 chars
            // (since '.' is not matching newline characters, we're using '[\s\S]' so that even multiline string is shortened)
            let report_text = escape_html(report.replace(/^(.{2000})[\s\S]+/, "$1..."));
            report_text = report_text.replace(/(?:\r\n|\r|\n)/g, '<br>');
            report = ` <b>${report_text}</b>`;
        }

        if (typeof message === 'object') {
            message = JSON.stringify(message);
        }

        show_error(`${str}:${report}${command}${tip} ${escape_html(message)}`, true);
    };
}


/**
 * Handy interval class, waiting till AJAX request finishes (won't flood server if there is a lag).
 */
class Interval {
    /**
     *  Class for managing intervals.
     *  Auto-delaying/boosting depending on server lag.
     *  Faking intervals by timeouts.
     *
     * @param {type} fn
     * @param {type} delay
     * @param {bool} blocking If true, the fn is an AJAX call. The fn will not be called again unless it calls `this.blocking = false` when AJAX is finished.
     *      You may want to include `.always(() => {this.blocking = false;})` after the AJAX call. (In 'this' should be instance of the Interval object.)
     *
     *      (Note that we preferred that.blocking setter over method unblock() because interval function
     *      can be called from other sources than this class (ex: at first run) and a non-existent method would pose a problem.)
     * @returns {Interval}
     */
    constructor(fn, delay, ajax_wait) {
        this.fn = fn;
        this.delay = this._delay = delay;
        this._delayed = function () {
            this.time1 = +new Date();
            this.fn.call(this);
            if (ajax_wait !== true && this.running) {
                this.start();
            }
        }.bind(this);
        this.start();
    }

    start() {
        this.stop();
        this.running = true;
        this.instance = setTimeout(this._delayed, this._delay);
        return this;
    }

    stop() {
        clearTimeout(this.instance);
        this.running = false;
        return this;
    }

    /**
     * Launch callback function now, reset and start the interval.
     * @return {Interval}
     */
    call_now() {
        this.stop();
        this._delayed();
        this.start();
        return this;
    }

    /**
     * Start if stopped or vice versa.
     * @param start If defined, true to be started or vice versa.
     */
    toggle(start = null) {
        if (start === null) {
            this.toggle(!this.running);
        } else if (start) {
            this.start();
        } else {
            this.stop();
        }
        return this;
    }

    set blocking(b) {
        if (b === false) {
            let rtt = +new Date() - this.time1;
            if (rtt > this._delay / 3) {
                if (this._delay < this.delay * 10) {
                    this._delay += 100;
                }
            } else if (rtt < this._delay / 4 && this._delay >= this.delay) {
                this._delay -= 100;
            }
            if (this.running) {
                this.start();
            }
        }
    }
}

/**
 * JS-click on a link that supports Ctrl+clicking for opening in a new tab.
 * @param {string} url
 * @returns {Boolean} False so that js-handled click is not followed further by the browser.
 */
function click_link(url, event) {
    if (event && event.ctrlKey) { // we want open a new tab
        let win = window.open(url, '_blank');
        if (win) {
            win.focus();
        } else { // popups disabled
            window.location = url;
        }
    } else {
        window.location = url;
    }
    return false;
}


/**
 * Control buttons to start/stop/... a bot, group or whole botnet
 */
var BOT_CLASS_DEFINITION = {
    starting: 'warning',
    running: 'success',
    stopping: 'warning',
    stopped: 'danger',
    reloading: 'warning',
    restarting: 'warning',
    incomplete: 'warning',
    error: 'danger',
    disabled: 'ligth',
    unknown: 'warning'
};
var BOT_STATUS_DEFINITION = {
    starting: 'starting',
    running: 'running',
    stopping: 'stopping',
    stopped: 'stopped',
    reloading: 'reloading',
    restarting: 'restarting',
    incomplete: 'incomplete',
    error: 'error',
    unknown: 'unknown'
};

var botnet_status = {}; // {group | true (for whole botnet) : BOT_STATUS_DEFINITION}
var bot_status = {}; // {bot-id : BOT_STATUS_DEFINITION}
var bot_status_previous = {}; // we need a shallow copy of bot_status, it's too slow to ask `app` every time
var bot_definition = {}; // {bot-id : runtime information (group, ...)}; only management.js uses this in time

$(document).on("click", ".control-buttons button", e => {
    let btn = $(e.target);

    let parent = btn.parent();
    if (parent.hasClass('btn')) { // clicked on glyphicon, shift up by one level
        btn = parent;
        parent = parent.parent();
    }

    let bot = parent.attr("data-bot-id");
    let botnet = parent.attr("data-botnet-group");
    let callback_fn = parent.data("callback_fn");
    let url;
    if (bot) {
        bot_status[bot] = btn.attr("data-status-definition");
        url = managementUrl("bot", `action=${btn.attr("data-url")}&id=${bot}`);
    } else {
        botnet_status[botnet] = btn.attr("data-status-definition");
        url = managementUrl('botnet', `action=${btn.attr("data-url")}&group=${botnet}`);
        for (let bot_d of Object.values(bot_definition)) {
            if (bot_d.groupname === botnet) {
                bot_status[bot_d.bot_id] = btn.attr("data-status-definition");
            }
        }

    }

    callback_fn.call(e.target, bot || botnet, 0);
    btn.siblings("[data-role=control-status]").trigger("update");

    authenticatedGetJson(url)
        .done(data => {
            if (bot) { // only restarting action returns an array of two values, the latter is important; otherwise, this is a string
                bot_status[bot] = Array.isArray(data) ? data.slice(-1)[0] : data;
            } else { // we received a {bot => status} object
                Object.assign(bot_status, data); // merge to current list
            }
        })
        .fail(() => {
            ajax_fail_callback(`Error ${bot_status[bot] || botnet_status[botnet]} bot${!bot ? "net" : ""}`).apply(null, arguments);
            bot_status[bot] = BOT_STATUS_DEFINITION.error;
        }).always(() => {
        btn.siblings("[data-role=control-status]").trigger("update");
        callback_fn.call(e.target, bot || botnet, 1);
    });
});

/**
 * Public method to include control buttons to DOM.
 * @param {string|null} bot id
 * @param {string|null} botnet Manipulate the whole botnet or a group. Possible values: "botnet", "collectors", "parsers", ... Parameter bot_id should be null.
 * @param {bool} status_info If true, dynamic word containing current status is inserted.
 * @param {fn} Fn (this = button clicked, bot-id|botnet, finished = 0|1)
 *              Launched when a button is clicked (finished 0) and callback after AJAX completed (finished 1).
 * @returns {$jQuery}
 */
function generate_control_buttons(bot = null, botnet = null, callback_fn = null, status_info = false) {
    let $el = $("#common-templates .control-buttons").clone()
        .data("callback_fn", callback_fn || (() => {
        }));
    if (bot) {
        $el.attr("data-bot-id", bot);
        $el.attr("data-botnet-group", bot in bot_definition ? bot_definition[bot].groupname : null); // specify group (ignore in Monitor, not needed and might not be ready)
    } else {
        $el.attr("data-botnet-group", botnet);
    }
    if (status_info) {
        $("<span/>", {"data-role": "control-status"}).bind("update", e => {
            let btn = $(e.target);
            let bot = btn.closest(".control-buttons").attr("data-bot-id");
            let botnet = btn.closest(".control-buttons").attr("data-botnet-group");
            let status = bot ? bot_status[bot] : botnet_status[botnet];
            btn.text(status).removeClass().addClass(`bg-${BOT_CLASS_DEFINITION[status]}`);
        }).prependTo($el).trigger("update");
    }
    return $el;
}

/**
 * Reads the parameter from URL
 */
function getUrlParameter(sParam) {
    let sPageURL = decodeURIComponent(window.location.search.substring(1)), sURLVariables = sPageURL.split('&'), sParameterName, i;
    for (let i = 0; i < sURLVariables.length; i++) {
        let sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
}

/**
 * Accesskeyfie
 * Turns visible [data-accesskey] to elements with accesskey and shows the accesskey with an underscore if possible.
 */
function accesskeyfie() {
    let seen = new Set();
    $("[data-accesskey]").attr("accesskey", ""); // reset all accesskeys. In Chrome, there might be only one accesskey 'e' on page.
    $("[data-accesskey]:visible").each((i, v) => {
        let btn = $(v);
        let key = btn.attr("data-accesskey");
        if (seen.has(key)) {
            return false; // already defined at current page state
        }
        seen.add(key);
        btn.attr("accesskey", key);
        // add underscore to the accesskeyed letter if possible (can work badly with elements having nested DOM children)
        let t1 = escape_html(btn.text());
        let t2 = t1.replace(new RegExp(key, "i"), match => `<u>${match}</u>`);
        if (t1 !== t2) {
            btn.html(t2);
        }
    });
}


/**
 * Determine the URL for management commands.
 */
function managementUrl(cmd, params) {
    let url = API + cmd;
    if (params !== undefined) {
	url += "?" + params;
    }
    return url;
}


/**
 * Login/session handling
 */


function authenticatedGetJson(url) {
    return authenticatedAjax({
        dataType: "json",
        url,
    });
}

function authenticatedAjax(settings) {
    let token = sessionStorage.getItem("login_token");
    if (token !== null) {
        settings.headers = {
            Authorization: token
        };
    }
    return $.ajax(settings);
}



// Intercept the login submit and send an Ajax request instead.
$(document).ready(function() {
    updateLoginStatus();

    $('#loginForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: managementUrl("login"),
            // Specifies exactly which data is sent.
            data: {
                username: $('#loginForm #username').val(),
                password: $('#loginForm #password').val(),
            },
            // Specifies which formart is expected as response.
            dataType: "json",
            // sets timeout to 3 seconds
            timeout: 3000,
            // Deletes the content of the password field when the request is
            // finished. (after success and error callbacks are executed)
            complete: () => $('#loginForm #password').val(""),
            // Executes this if the request was successful.
        }).done(data => {
            // Check if login_token and username came back and store them in
            // sessionStorage.
            if (typeof data.login_token !== 'undefined' &&
                typeof data.username !== 'undefined') {
                sessionStorage.setItem("login_token", data.login_token);
                sessionStorage.setItem("username", data.username);

                $('#loginErrorField').text("")
                $('#modalLoginForm').modal('hide');
                updateLoginStatus();
                window.location.reload();
            } else if (typeof data.error !== 'undefined') {
                // If authentication failed, the returned error message is displayed.
                $('#loginErrorField').text(data.error);
            } else {
                // Other error, display the response for easier debugging.
                $('#loginErrorField').text("Login failed, server response was " + data);
            }
        })
        .fail(function(jqXHR, textStatus) {
            if (typeof jqXHR.responseJSON !== 'undefined' && typeof jqXHR.responseJSON.errors !== 'undefined') {
                let concatenated = "";
                for (let key in jqXHR.responseJSON.errors) {
                    concatenated += jqXHR.responseJSON.errors[key] + ". "
                }
                $('#loginErrorField').text("Login failed, server response was: " + concatenated);
            } else {
                $('#loginErrorField').text("Login failed with unknown reason. Please report this bug.");
                console.log(jqXHR.responseText)
                console.log(jqXHR.responseJson)
            }
        });
    });

    $('#logOut').click(logout);
});

function logout() {
    sessionStorage.removeItem("login_token");
    sessionStorage.removeItem("username");

    updateLoginStatus();
}

function updateLoginStatus() {
    let status = document.getElementById('login-status');
    let loginButton = document.getElementById('signUp');
    let logoutButton = document.getElementById('logOut');
    let username = sessionStorage.getItem("username");
    if (username !== null) {
        status.textContent = `Logged in as: ${username}`;
        loginButton.style.display = "none";
        logoutButton.style.removeProperty("display");
    } else {
        status.textContent = "Not logged in";
        loginButton.style.removeProperty("display");
        logoutButton.style.display = "none";
    }
}

var html_characters = [
        ['&', '&amp;'],
        ['<', '&lt;'],
        ['>', '&gt;'],
        ['"', '&quot;'],
        ["'", "&#39;"],
];

function escape_html(text) {
    return html_characters.reduce((s, [character, replacement]) => s.replaceAll(character, replacement), text);
}
