<!--
SPDX-FileCopyrightText: 2022 The Shadowserver Foundation
SPDX-License-Identifier: AGPL-3.0-or-later
-->

This module is maintained by [The Shadowserver Foundation](https://www.shadowserver.org/).  

Please contact intelmq@shadowserver.org with any issues or concerns.

The report configuration is now stored in a _schema.json_ file downloaded from https://interchange.shadowserver.org/intelmq/_version_.

For environments that have internet connectivity the `update_schema.py` script should be setup as a cron job to obtain the latest revision.

For air-gapped systems automation will be required to download and copy the  _schema.json_ file into this directory

The parser will automatically reload the configuration when the file changes.
