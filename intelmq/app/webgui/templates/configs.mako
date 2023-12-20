## SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
## SPDX-License-Identifier: AGPL-3.0-or-later

<%inherit file="base.mako" />

<div class="navbar-default sidebar" role="navigation">
    <div class="sidebar-nav navbar-collapse">
        <ul class="nav" id="side-menu">
            <li id="customListItem"><button class="btn btn-warning" style="text-align: center;" id="editDefaults">Edit Defaults</button></li>
        </ul>
    </div>
</div>


<!-- Page Content -->
<div id="page-wrapper-with-sidebar">
    <div class="row">
        <div id="network-container" class="col-md-12">
            Loading...
        </div>
    </div>
</div>

<div id="network-popUp" class="without-bot">
    <span id="network-popUp-title">node</span>
    <a id="documentationButton" class="btn btn-default" title="open documentation" href="" target="_blank">
	<span class="glyphicon glyphicon-question-sign"></span>
    </a>
    <table id="network-popUp-fields" class="table table-striped" style="margin:auto;">
        <tr>
            <td>id</td><td><input id="node-id" value="new value"></td>
        </tr>
        <tr>
            <td>name</td><td><input id="node-name" value=""></td>
        </tr>
        <tr>
            <td>group</td><td><input id="node-group" value=""></td>
        </tr>
        <tr>
            <td>module</td><td><input id="node-module" value=""></td>
        </tr>
        <tr>
            <td>description</td><td><input id="node-description" value=""></td>
        </tr>
        <tr>
            <td>run_mode</td><td><input id="node-run_mode" value=""></td>
        </tr>
    </table>
    <div>
        <form>
            <input type="button" class="btn-danger btn-block" value="cancel" id="network-popUp-cancel">
        </form>
        <form>
            <input type="button" class="btn-success btn-block" value="ok" id="network-popUp-ok">
        </form>
    </div>
</div>

<!-- HTML templates -->
<div id='templates'>
    <ul class="side-menu">
        <li>
            <a><span class="fa arrow"></span></a>
            <ul class="nav nav-second-level collapse">
                <li draggable="true">
                    <a href="#" data-toggle="tooltip" data-placement="right"></a>
                </li>
            </ul>
        </li>
    </ul>
    <button class="btn btn-warning new-key-btn" title="add new key"><span class="glyphicon glyphicon-plus-sign"></span></button>
    <div class="modal fade" tabindex="-1" role="dialog">
        <div class="modal-dialog" role="document">
            <form class="modal-content">
                <div class="modal-header">
                    <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
                    <h4 class="modal-title">Modal title</h4>
                </div>
                <div class="modal-body">
                    <p>One fine body&hellip;</p>
                </div>
                <div class="modal-footer">
                    <button type="submit" class="btn-success btn btn-primary">Ok</button>
                    <button type="button" class="btn-danger btn btn-default" data-dismiss="modal">Cancel</button>
                </div>
            </form>
        </div>
    </div>
    <div class="modal-add-new-key">
        <div class="form-group">
            <label  class="col-sm-2 control-label">Key</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" name="newKeyInput" required/>
            </div>
        </div>
        <div class="form-group">
            <label class="col-sm-2 control-label">Value</label>
            <div class="col-sm-10">
                <input type="text" class="form-control" name="newValueInput" required/>
            </div>
        </div>
    </div>

    <div class="network-edge-menu">
        <div class="vis-button vis-edit">
            <div data-accesskey="e" class="vis-label">
                Edit Path
            </div>
        </div>
    </div>
    <div class="network-node-menu">
        <div class="vis-button duplicate-button ">
            <div data-accesskey="t" class="vis-label">
                Duplicate
            </div>
        </div>
        <div class="vis-separator-line"></div>
        <div class="vis-button monitor-button">
            <div title="Monitor bot">
                <a data-accesskey="m" href="#">
                    <img src="./images/monitor.png" width="24" height="24" />
                </a>
            </div>
        </div>
    </div>
    <div class="network-right-menu">
        <div class="vis-live-toggle">
            <div data-accesskey="l" class="icon">
                Live
            </div>
        </div>
        <div class="vis-physics-toggle">
            <div data-accesskey="p" class="icon fa-align-right fa">
                Physics
            </div>
        </div>
        <div class="vis-save" id="vis-save">
            <div class="vis-save-icon">
                <span data-accesskey="s" class="vis-save-label">Save Configuration</span>
            </div>
        </div>
        <div class="vis-clear" id="vis-clear">
            <div class="vis-clear-icon">
                <span class="vis-clear-label">Clear Configuration</span>
            </div>
        </div>
        <div class="vis-redraw" id="vis-redraw">
            <div class="vis-redraw-icon">
                <span class="vis-redraw-label">Redraw Botnet</span>
            </div>
        </div>

    </div>
</div>
