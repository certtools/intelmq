# SPDX-FileCopyrightText: 2020 Sebastian Wagner <wagner@cert.at>, 2022 CERT.at GmbH <intelmq-team@cert.at>
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# -*- coding: utf-8 -*-
from collections import OrderedDict
from intelmq.lib.upgrade import harmonization, v100_dev7, v110, v111, v112, v200, v202, v210, v213, v220, v221, v222, v230, v233, v300, v301


UPGRADES = OrderedDict([
    ((1, 0, 0, 'dev7'), (v100_dev7.modify_syntax)),
    ((1, 1, 0), (v110.shadowserver_feednames, v110.deprecations)),
    ((1, 1, 1), (v111.defaults_process_manager, )),
    ((1, 1, 2), (v112.feodo_tracker_ips, v112.feodo_tracker_domains, )),
    ((2, 0, 0), (v200.defaults_statistics, v200.defaults_broker,
                 v200.defaults_ssl_ca_certificate)),
    ((2, 0, 1), ()),
    ((2, 0, 2), (v202.fixes, )),
    ((2, 1, 0), (v210.deprecations, )),
    ((2, 1, 1), ()),
    ((2, 1, 2), ()),
    ((2, 1, 3), (v213.deprecations, v213.deprecations)),
    ((2, 2, 0), (v220.configuration, v220.azure_collector, v220.feed_changes)),
    ((2, 2, 1), (v221.feed_changes, )),
    ((2, 2, 2), (v222.feed_changes, )),
    ((2, 2, 3), ()),
    ((2, 3, 0), (v230.csv_parser_parameter_fix, v230.feed_changes, v230.deprecations,)),
    ((2, 3, 1), ()),
    ((2, 3, 2), ()),
    ((2, 3, 3), (v233.feodotracker_browse, )),
    ((3, 0, 0), (v300.bots_file_removal, v300.defaults_file_removal, v300.pipeline_file_removal, )),
    ((3, 0, 1), (v301.deprecations, )),
    ((3, 0, 2), ()),
    ((3, 1, 0), ()),
])

ALWAYS = (harmonization.harmonization, )
