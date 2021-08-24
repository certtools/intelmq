# SPDX-FileCopyrightText: 2018 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import os

if os.environ.get('INTELMQ_TEST_EXOTIC'):
    import intelmq.bots.experts.mcafee.expert_mar
