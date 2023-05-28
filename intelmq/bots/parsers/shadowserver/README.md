<!--
SPDX-FileCopyrightText: 2022 The Shadowserver Foundation
SPDX-License-Identifier: AGPL-3.0-or-later
-->

This module is maintained by [The Shadowserver Foundation](https://www.shadowserver.org/).  

Please contact intelmq@shadowserver.org with any issues or concerns.

The report configuration is now stored in a _schema.json_ file downloaded from https://interchange.shadowserver.org/intelmq/v1/schema.

For environments that have internet connectivity the `update_schema.py` script should be called from a cron job to obtain the latest revision.
The parser will attempt to download a schema update on startup unless INTELMQ_SKIP_INTERNET is set.

For air-gapped systems automation will be required to download and copy the _schema.json_ file into this directory.

The parser will automatically reload the configuration when the file changes.


## Sample configuration:

```
shadowserver-collector:
  description: Our bot responsible for getting reports from Shadowserver
  enabled: true
  group: Collector
  module: intelmq.bots.collectors.shadowserver.collector_reports_api
  name: Shadowserver_Collector
  parameters:
    destination_queues:
      _default: [shadowserver-parser-queue]
    file_format: csv
    api_key: "$API_KEY_received_from_the_shadowserver_foundation"
    secret: "$SECRET_received_from_the_shadowserver_foundation"
  run_mode: continuous
```

```
shadowserver-parser:
  bot_id: shadowserver-parser
  name: Shadowserver Parser
  enabled: true
  group: Parser
  groupname: parsers
  module: intelmq.bots.parsers.shadowserver.parser
  parameters:
    destination_queues:
      _default: [file-output-queue]
  run_mode: continuous
```

