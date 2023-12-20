## SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
## SPDX-License-Identifier: AGPL-3.0-or-later

<%inherit file="base.mako" />

<!-- Page Content -->
<div id="page-wrapper">
    <div class="row">
        <div id="graph-container">
            <div class="col-md-2" id="botnet-panels">
                <div class="panel panel-default" data-botnet-group="botnet" data-botnet-url="">
                    <div class="panel-heading">
                        <h4>Whole Botnet Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Status: <span data-role="botnet-status" class="bg-warning">Unknown</span></div><div data-role="botnet-buttons"></div>
                    </div>
                </div>
            <!-- may be implemented. But should be the list of bots completed on JS or Python side?-->
                <div class="panel panel-default" data-botnet-group="collectors">
                    <div class="panel-heading">
                        <h4>Collectors Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Status: <span data-role="botnet-status" class="bg-warning">Unknown</span></div><div data-role="botnet-buttons"></div>
                    </div>
                </div>

                <div class="panel panel-default" data-botnet-group="parsers">
                    <div class="panel-heading">
                        <h4>Parsers Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Status: <span data-role="botnet-status" class="bg-warning">Unknown</span></div><div data-role="botnet-buttons"></div>
                    </div>
                </div>

                <div class="panel panel-default" data-botnet-group="experts">
                    <div class="panel-heading">
                        <h4>Experts Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Status: <span data-role="botnet-status" class="bg-warning">Unknown</span></div><div data-role="botnet-buttons"></div>
                    </div>
                </div>

                <div class="panel panel-default" data-botnet-group="outputs">
                    <div class="panel-heading">
                        <h4>Outputs Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Status: <span id="botnet-status" class="bg-warning">Unknown</span></div><div data-role="botnet-buttons"></div>
                    </div>
                </div>
            </div>
            <div class="col-md-10">
                <div class="panel panel-default" id="bot-table-panel">
                    <div class="panel-heading">
                        <h4 id="bot-status-panel-title">Individual Bot Status:</h4>
                    </div>
                    <div class="panel-body">
                        <div class="table-responsive">
                            <table class="table" id="bot-table">
                                <thead>
                                    <tr><th>Bot ID</th><th>Status</th><th>Actions</th></tr>
                                </thead>
                                <tbody id="bot-table-body">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>
