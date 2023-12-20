## SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
## SPDX-License-Identifier: AGPL-3.0-or-later

<%inherit file="base.mako" />

<div class="navbar-default sidebar" role="navigation">
    <div class="sidebar-nav navbar-collapse">
        <ul class="nav" id="side-menu">
        </ul>
    </div>
</div>


<!-- Page Content -->
<div id="page-wrapper-with-sidebar">
    <div class="row">
        <div class="col-md-12"><h3>Monitoring: <span id="monitor-target">All</span></h3></div>
        <div id="graph-container" class="col-md-12">
            <div class="col-md-12">
                <div class="panel panel-default" id="queues-panel">
                    <div class="panel-heading">
                        <h4 id="queues-panel-title">Queues</h4>
                    </div>
                    <div class="panel-body">
                        <div id="source-queue-table-div" class="col-md-4">
                            <table class="table">
                                <thead>
                                    <tr><th class="width-80">Source Queue</th><th class="width-20">Count</th></tr>
                                </thead>
                                <tbody id="source-queue">
                                </tbody>
                            </table>
                        </div>
                        <div id="internal-queue-table-div" class="col-md-3">
                            <table class="table">
                                <thead>
                                    <tr><th class="width-80">Internal Queue</th><th class="width-20">Count</th></tr>
                                </thead>
                                <tbody id="internal-queue">
                                </tbody>
                            </table>
                        </div>
                        <div id="destination-queues-table-div" class="col-md-5">
                            <table class="table" id="destination-queues-table">
                                <colgroup>
                                    <col><col>
                                </colgroup>
                                <thead>
                                    <tr><th class="width-60" id="destination-queue-header">Destination Queue</th>
                                        <th class="width-20">Path</th>
                                        <th class="width-20">Count</th>
                                    </tr>
                                </thead>
                                <tbody id="destination-queues">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="panel panel-default" id="inspect-panel">
                    <div class="panel-heading">
                        <h4 id="inspect-panel-title">Inspect</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Message

                            <button data-role="get" title="See the message that waits in the input (source or internal) queue">Get</button>
                            <button data-role="pop" title="See the message that waits in the input (source or internal) queue and pop it from there">Pop</button>
                            <button data-role="send" title="Send directly, without processing) to the bot's ouput queue, just as it was sent by self.send_message() in bot's  process() method">Send</button>
                            <br>
                            <textarea  class="form-control" rows="3" placeholder='json message {"feed.name": "example", ...}&#10;Ctrl+Enter to process' id="message-playground"></textarea>
                            <br>
                            <button  class="btn btn-success" data-role="process" title="Bot's process() method will be run one time">Process</button>
                            <label>
                                <input data-role="inject" data-checked="" type="checkbox">
                                Inject message from above
                            </label>
                            <label>
                                <input checked="" data-role="show-sent" type="checkbox">
                                Fetch processed message back here
                            </label>
                            <label>
                                <input data-role="dry" type="checkbox">
                                Dry-run
                            </label>
                            <button data-role="clear" class="btn btn-secondary" title="just clear the textareas">Clear</button>
                            <br><br>
                            <code id="command-show"></code>
                            <textarea  class="form-control" readonly="readonly" rows="3" placeholder="running log" id="run-log"></textarea>

                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="panel panel-default" id="logs-panel">
                    <div class="panel-heading">
                        <h4 id="logs-panel-title">Logs</h4>
                    </div>
                    <div class="panel-body">
                        <div class="panel-div">Log Level: <select id="log-level-indicator">
                                <option value="ALL">All</option>
                                <option value="DEBUG">Debug</option>
                                <option value="INFO">Info</option>
                                <option value="WARNING">Warning</option>
                                <option value="ERROR">Error</option>
                                <option value="CRITICAL">Critical</option>
                            </select></div>
                        <br>
                        <div class="table-responsive">
                            <table class="table" id="log-table">
                                <thead>
                                    <tr><th>Time</th><th>ID</th><th>Level</th><th>Message</th><th></th></tr>
                                </thead>
                                <tbody id="log-table-body">
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
            <div class="col-md-12">
                <div class="panel panel-default" id="parameters-panel">
                    <div class="panel-heading">
                        <h4 id="parameters-panel-title">Parameters</h4>
                    </div>
                    <div class="panel-body">
                        .. loading ..
                    </div>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Modal -->
<div class="modal fade" id="extended-message-modal" tabindex="-1" role="dialog" aria-labelledby="modal-title" aria-hidden="true">
    <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
                <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>
                <h4 class="modal-title" id="modal-title">Entire message</h4>
            </div>
            <div class="modal-body" id="modal-body" style="overflow: auto">
            </div>
        </div>
    </div>
</div>
