# SPDX-FileCopyrightText: 2016 aaronkaplan
#
# SPDX-License-Identifier: AGPL-3.0-or-later

DATE:=$(shell date +"%Y%m%d-%H%M%S")

backup:
        cp -a etc config_backups/etc.bak$(DATE)
        cp -a var/lib/bots/modify config_backups/modify.bak$(DATE)
