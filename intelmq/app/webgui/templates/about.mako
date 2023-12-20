## SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
## SPDX-License-Identifier: AGPL-3.0-or-later

<%inherit file="base.mako" />

<!-- Page Content -->
<div id="page-wrapper">
    <div class="row" style="padding: 20px">
        <div class="col-md-1">&nbsp;</div>
        <div class="col-md-10" style="font-size: 16px">
            <img src="./images/logo.png" alt="IntelMQ" style="float: right">
            <p><a href="https://intelmq.org/"><strong>IntelMQ</strong></a> is a solution for IT security teams (CERTs, CSIRTs, abuse departments,...)
                for collecting and processing security feeds (such as log files) using a message queuing
                protocol. It's a community driven initiative called <strong>IHAP</strong> (Incident
                Handling Automation Project) which was conceptually designed by European
                CERTs/CSIRTs during several InfoSec events. Its main goal is to give to
                incident responders an easy way to collect &amp; process threat intelligence
                thus improving the incident handling processes of CERTs.</p>
            <p>IntelMQ's design was influenced by
                <a href="https://github.com/abusesa/abusehelper">AbuseHelper</a>,
                however it was re-written from scratch and aims at:</p>
            <ul>
                <li>Reduce the complexity of system administration</li>
                <li>Reduce the complexity of writing new bots for new data feeds</li>
                <li>Reduce the probability of events lost in all process with persistence
                    functionality (even system crash)</li>
                <li>Use and improve the existing Data Harmonization Ontology</li>
                <li>Use JSON format for all messages</li>
                <li>Integration of the existing tools (AbuseHelper, CIF)</li>
                <li>Provide easy way to store data into Log Collectors like
                    ElasticSearch, Splunk, databases (such as PostgreSQL)</li>
                <li>Provide easy way to create your own black-lists</li>
                <li>Provide easy communication with other systems via HTTP RESTFUL API</li>
            </ul>
            <p>It follows the following basic meta-guidelines:</p>
            <ul>
                <li>Don't break simplicity - KISS</li>
                <li>Keep it open source - forever</li>
                <li>Strive for perfection while keeping a deadline</li>
                <li>Reduce complexity/avoid feature bloat</li>
                <li>Embrace unit testing</li>
                <li>Code readability: test with unexperienced programmers</li>
                <li>Communicate clearly</li>
            </ul>
        </div>
        <div class="col-md-1">&nbsp;</div>
    </div>
    <div class="row">
        <div class="col-md-1">&nbsp;</div>
        <div class="col-md-10" style="font-size: 16px">
            <h2>Version</h2>
            <table class="table">
                <tr><td>IntelMQ<td><td id="intelmq-version"></td></tr>
                <tr><td>IntelMQ API<td><td id="intelmq-api-version"></td></tr>
                <tr><td>IntelMQ Manager<td><td id="intelmq-manager-version"></td></tr>
            </table>
        </div>
    </div>
    <div class="row">
        <div class="col-md-1">&nbsp;</div>
        <div class="col-md-10" style="font-size: 16px" id="debugging">
            <h2 id="debugging-heading" class="waiting">Debugging</h2>
        </div>
    </div>
</div>
