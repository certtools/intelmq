#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2021 Sebastian Wagner
# SPDX-License-Identifier: AGPL-3.0-or-later
#

find /home/runner/work/intelmq/intelmq/docs/ /home/runner/work/intelmq/intelmq/intelmq/ -name '*.py' -exec /home/runner/.local/bin/regexploit-py {} \+
find /home/runner/work/intelmq/intelmq/intelmq/ -name '*.json' -exec /home/runner/.local/bin/regexploit-json {} \+
find /home/runner/work/intelmq/intelmq/intelmq/ -name '*.yaml' -exec /home/runner/.local/bin/regexploit-yaml {} \+
