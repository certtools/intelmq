<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


#### Botnet Concept

The \"botnet\" represents all currently configured bots which are explicitly enabled. It is, in essence, the graph of
the bots which are connected together via their input source queues and destination queues.

To get an overview which bots are running, use `intelmqctl status` or use the IntelMQ Manager. Set `"enabled": true` in
the runtime configuration to add a bot to the botnet. By default, bots will be configured as `"enabled": true`.
See `bots`{.interpreted-text role="doc"} for more details on configuration.

Disabled bots can still be started explicitly using
`intelmqctl start <bot_id>`, but will remain in the state `disabled` if stopped (and not be implicitly enabled by
the `start` command). They are not started by `intelmqctl start` in analogy to the behavior of widely used
initialization systems.
