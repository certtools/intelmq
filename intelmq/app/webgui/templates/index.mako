## SPDX-FileCopyrightText: 2020 IntelMQ Team <intelmq-team@cert.at>
## SPDX-License-Identifier: AGPL-3.0-or-later

<%inherit file="base.mako" />


<div id="wrapper">
    <div id="page-wrapper">
        <!-- Jumbotron Header -->
        <div class="row jumbotron-row">
            <div class="col-md-12">
                <header class="jumbotron header-img">
                    <img height="100%" src="images/logo2.png" alt="Logo">
                    <img height="100%" src="images/logo_no_margin_6.png" alt="IntelMQ Manager">
                </header>
            </div>
        </div>

        <!-- Page Features -->
        <div class="row center-row">
            <div class="col-md-9 col-sm-12 center-row-content">
                <div class="col-md-4 col-sm-12">
                    <a class="index-link" href="configs.html">
                        <div class="thumbnail">
                            <img src="./images/config.png" alt="" width="100%" height="100%">
                            <div class="caption">
                                <h3>Configuration</h3>
                                <p>To either change the currently deployed configuration or to create a new one in a graphical fashion.</p>
                            </div>
                        </div>
                    </a>
                </div>

                <div class="col-md-4 col-sm-12">
                    <a class="index-link" href="management.html">
                        <div class="thumbnail">
                            <img src="./images/botnet.png" alt="">
                            <div class="caption">
                                <h3>Management</h3>
                                <p>This is where you go to start/stop your bots or check on their status.</p>
                            </div>
                        </div>
                    </a>
                </div>

                <div class="col-md-4 col-sm-12">
                    <a class="index-link" href="monitor.html">
                        <div class="thumbnail">
                            <img src="./images/monitor.png" alt="" >
                            <div class="caption">
                                <h3>Monitor</h3>
                                <p>This feature is meant to allow you to check on the overall status of your botnet. You can read the bot logs, see how the queues are behaving and other features that allow you to have a better overview of the overall health of the system.</p>
                            </div>
                        </div>
                    </a>
                </div>

            </div>
        </div>
        <div class="row center-row">
            <div class="col-md-9 col-sm-12 center-row-content">
                <div class="col-md-6 col-sm-12">
                    <a class="index-link" href="check.html">
                        <div class="thumbnail">
                            <img src="./images/check.png" alt="" >
                            <div class="caption">
                                <h3>Check</h3>
                                <p>Check IntelMQ is running properly.</p>
                            </div>
                        </div>
                    </a>
                </div>

                <div class="col-md-6 col-sm-12">
                    <a class="index-link" href="about.html">
                        <div class="thumbnail">
                            <img src="./images/about.png" alt="" >
                            <div class="caption">
                                <h3>About</h3>
                                <p>To learn more about the project's goals and contributors.</p>
                            </div>
                        </div>
                    </a>
                </div>

            </div>
        </div>
        <!-- /.row -->
    </div>
</div>
