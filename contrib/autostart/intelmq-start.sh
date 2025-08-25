#!/bin/bash
# SPDX-FileCopyrightText: 2025 Institute for Common Good Technology
# SPDX-License-Identifier: AGPL-3.0-or-later

# suppress stdout output. Errors go to stderr and are kept

if [ "$UID" -eq 0 ]; then
    sudo -u intelmq intelmqctl start > /dev/null
else
    nohup intelmqctl start > /dev/null
fi
