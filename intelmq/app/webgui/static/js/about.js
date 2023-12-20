// SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
//
// SPDX-License-Identifier: AGPL-3.0-or-later
'use strict';

function get_versions() {
    let intelmq_version_element = document.getElementById('intelmq-version');
    let intelmq_api_version_element = document.getElementById('intelmq-api-version');
    let intelmq_manager_version_element = document.getElementById('intelmq-manager-version');

    authenticatedGetJson(managementUrl('version'))
        .done(function (data) {
            intelmq_version_element.innerHTML = data.intelmq;
            intelmq_api_version_element.innerHTML = data['intelmq-api'];
            intelmq_manager_version_element.innerHTML = '3.2.0';
        })
        .fail(function (jqxhr, textStatus, error) {
            let err = `${textStatus}, ${error}`;
            console.error(`Request Failed: ${err}`);
            alert('error getting version');
        });
}
function get_debug() {
    let section_element = document.getElementById('debugging');

    authenticatedGetJson(managementUrl('debug'))
        .done(function (data) {
            for (const section in data) {
                let section_heading = document.createElement("h3");
                section_heading.innerHTML = section;
                section_element.appendChild(section_heading);
                let table = document.createElement("table");
                let tbody = document.createElement("table");

                for (const [key, value] of Object.entries(data[section])) {
                    let row = tbody.insertRow(-1);
                    let cell0 = row.insertCell(0);
                    cell0.innerHTML = `<pre>${key}</pre>`;
                    let cell1 = row.insertCell(1);
                    cell1.innerHTML = `<pre>${value}</pre>`;
                }
                table.appendChild(tbody);
                section_element.appendChild(table);
            }
            $('#debugging-heading').removeClass('waiting');
        })
        .fail(function (jqxhr, textStatus, error) {
            let err = `${textStatus}, ${error}`;
            console.error(`Request Failed: ${err}`);
            alert('Error getting debugging information. Do you have IntelMQ >= 2.2.0?');
        });
}

get_versions();
get_debug();
