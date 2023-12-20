/* intelmq-manager.js javascript file for intelmq-manager
 *
 * SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * Do not change this file! If you want to customize the settings,
 * create a 'var.js' file and define the custom settings there with
 * var VARIABLENAME = value
 */

/*
 * ROOT points to the URI of the API service.
 * Set this for example to `https://intelmq.organization.tld/`
 * By default ROOT points to the host the manager runs on, but the path '/intelmq'
 */
'use strict';

var arr = window.location.href.split('/');
var ROOT = ROOT ?? `${arr[0]}//${arr[2]}/intelmq`;

/*
 * If there are multiple versions of the API, they can be defined here
 */
var API_V1 = ROOT + '/v1/api/'

/*
 * use a specific version when accessing the API variable
 */
var API = API_V1
