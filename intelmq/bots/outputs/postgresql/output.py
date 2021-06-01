# SPDX-FileCopyrightText: 2015 National CyberSecurity Center
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
Compatibility shim
"""

from intelmq.bots.outputs.sql.output import SQLOutputBot


class PostgreSQLOutputBot(SQLOutputBot):
    engine = 'postgresql'

    def init(self):
        self.logger.warning("The output bot 'intelmq.bots.outputs.postgresql.output' "
                            "is deprecated and replaced by "
                            "'intelmq.bots.outputs.sql.output' with the parameter "
                            "'engine' = 'postgresql'. "
                            "The fallback compatibility will be removed in version 3.0.")
        super().init()


BOT = PostgreSQLOutputBot
