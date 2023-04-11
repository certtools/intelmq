# SPDX-FileCopyrightText: 2023 The Shadowserver Foundation
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import os
import intelmq.bots.parsers.shadowserver._config as config

if __name__ == '__main__':  # pragma: no cover
    exec(open(os.path.join(os.path.dirname(__file__), '../../../version.py')).read())  # defines __version__
    config.update_schema(__version__)
