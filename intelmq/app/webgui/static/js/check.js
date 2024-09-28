// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

let colors = {info: "alert-info", warning: "alert-warning", error: "alert-danger"};
let statuses = {success: "No error found.", error: "Some issues have been found, please check the output."}


function get_check_output() {
    let tableEl = document.getElementById('check-output-table');

    authenticatedGetJson(managementUrl('check'))
        .done(data => {
            //data = {"status": "error","lines": [["info", "Reading configuration files."], ["info", "Checking runtime configuration."], ["info", "Checking pipeline configuration."], ["warning", "Bot 'cert-bund-avalanche-parser' has no 'description'."], ["warning", "Bot 'mailsend-output-cz' has no 'name'."], ["error", "Misconfiguration: No source queue for 'mailsend-output-cz'."], ["error", "Misconfiguration: No pipeline configuration found for 'vxvault-collector'."], ["error", "Misconfiguration: No pipeline configuration found for 'vxvault-parser'."], ["info", "Checking harmoization configuration."], ["info", "Checking for bots."]]};
            tableEl.innerHTML = `<tr><td>Status<td><td>${statuses[data.status]}</td></tr>`;
            for (let line of data.lines) {
                tableEl.innerHTML += `<tr class='${colors[line[0]]}'><td>${line[0]}<td><td>${line[1]}</td></tr>`;
            }
        })
        .fail((jqxhr, textStatus, error) => {
            let err = `${textStatus}, ${error}`;
            console.error(`Request Failed: ${err}`);
            alert('error getting check command output');
        });
}

get_check_output();
