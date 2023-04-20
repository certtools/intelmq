# SPDX-FileCopyrightText: 2022 REN-ISAC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
import os
#  import unittest

#  import intelmq.lib.test as test
if os.environ.get('INTELMQ_TEST_EXOTIC'):
    from intelmq.bots.outputs.cif3.output import CIF3OutputBot  # noqa

# This file is a stub
# We cannot do much more as we are missing a mock CIFv3 instance to use
# to initialise cifsdk
