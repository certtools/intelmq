#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2019 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

import intelmq.bin.intelmqctl as ctl
import intelmq.lib.utils as utils
import sys


cont = ctl.IntelMQController(interactive=False)
retval, queues = cont.list_queues()
if retval != 0:
    sys.exit(1)

with open('/var/lib/check_mk_agent/spool/70_intelmq-queues.txt', 'w') as handle:
    handle.write("<<<local>>>\nP intelmq-queues ")
    source_queues = set()
    destination_queues = set()

    for botid, value in queues.items():
        if 'source_queue' in value:
            source_queues.add(value['source_queue'])
        if 'destination_queues' in value:
            destination_queues.update(utils.flatten_queues(value['destination_queues']))

    perf = []
    for queuename, queuecount in source_queues.union(destination_queues):
        perf.append("%s=%d" % (queuename.replace('_', '-'), queuecount))
    handle.write("|".join(perf))
    handle.write('\n')
