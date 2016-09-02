#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""


TODO: check if action is allowed when called
"""
import argparse
import glob
import json
import os.path
import pprint
import readline  # hooks into input()
import traceback

from termstyle import bold, green, inverted, red

import intelmq.bin.intelmqctl as intelmqctl
import intelmq.lib.exceptions as exceptions
import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
from intelmq import DEFAULT_LOGGING_PATH, DEFAULTS_CONF_FILE, RUNTIME_CONF_FILE

APPNAME = "intelmqdump"
DESCRIPTION = """
intelmqdump can inspect dumped messages, show, delete or reinject them into
the pipeline. It's an interactive tool, directly start it to get a list of
available dumps or call it with a known bot id as parameter."""
EPILOG = """
Interactive actions after a file has been selected:
- r, Recover by IDs
  > r id{,id} [queue name]
  > r 3,4,6
  > r 3,7,90 modify-expert-queue
  The messages identified by a consecutive numbering will be stored in the
  original queue or the given one and removed from the file.
- a, Recover all
  > a [queue name]
  > a
  > a modify-expert-queue
  All messages in the opened file will be recovered to the stored or given
  queue and removed from the file.
- e, Delete entries by IDs
  > e id{,id}
  > e 3,5
  The entries will be deleted from the dump file.
- d, Delete file
  > d
  Delete the opened file as a whole.
- s, Show by IDs
  > s id{,id}
  > s 0,4,5
  Show the selected IP in a readable format. It's still a raw format from
  repr, but with newlines for message and traceback.
- q, Quit
  > q
"""
USAGE = '''
    intelmqdump [botid]
    intelmqdump [-h|--help]'''
# shortcut: description, takes ids, available for corrupted files
ACTIONS = {'r': ('(r)ecover by ids', True, False),
           'a': ('recover (a)ll', False, False),
           'e': ('delete (e)ntries', True, False),
           'd': ('(d)elete file', False, True),
           's': ('(s)how by ids', True, False),
           'q': ('(q)uit', False, True),
           }
AVAILABLE_IDS = [key for key, value in ACTIONS.items() if value[1]]


def dump_info(fname):
    info = red('unknwon error')
    if not os.path.getsize(fname):
        info = red('empty file')
    else:
        try:
            handle = open(fname, 'rt')
        except OSError as exc:
            info = red('unable to open file: {!s}'.format(exc))
        else:
            try:
                content = json.load(handle)
            except ValueError as exc:
                info = red('unable to load JSON: {!s}'.format(exc))
            else:
                try:
                    info = "{!s} dumps".format(len(content.keys()))
                except AttributeError as exc:
                    info = red("unable to count dumps: {!s}".format(exc))
        finally:
            try:
                handle.close()
            except NameError:
                pass
    return info


def save_file(fname, content):
    with open(fname, 'wt') as handle:
        json.dump(content, handle)


def load_meta(dump):
    retval = []
    for key, value in dump.items():
        error = value['traceback'].splitlines()[-1]
        if len(error) > 200:
            error = error[:100] + '...' + error[-100:]
        retval.append((key, error))
    return retval


def main():
    parser = argparse.ArgumentParser(
        prog=APPNAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=USAGE,
        description=DESCRIPTION,
        epilog=EPILOG,
    )

    parser.add_argument('botid', metavar='botid', nargs='?',
                        default=None, help='botid to inspect dumps of')
    args = parser.parse_args()
    ctl = intelmqctl.IntelMQContoller()

    if args.botid is None:
        filenames = glob.glob(os.path.join(DEFAULT_LOGGING_PATH, '*.dump'))
        if not len(filenames):
            print(green('Nothing to recover from, no dump files found!'))
            exit(0)
        filenames = [(fname, fname[len(DEFAULT_LOGGING_PATH):-5])
                     for fname in sorted(filenames)]

        length = max([len(value[1]) for value in filenames])
        print(bold("{c:>3}: {s:{l}} {i}".format(c='id', s='name (bot id)',
                                                i='content', l=length)))
        for count, (fname, shortname) in enumerate(filenames):
            info = dump_info(fname)
            print("{c:3}: {s:{l}} {i}".format(c=count, s=shortname, i=info,
                                              l=length))
        botid = input(inverted('Which dump file to process (id or name)?') +
                      ' ')
        botid = botid.strip()
        if botid == 'q' or not botid:
            exit(0)
        try:
            fname, botid = filenames[int(botid)]
        except ValueError:
            fname = os.path.join(DEFAULT_LOGGING_PATH, botid) + '.dump'
    else:
        botid = args.botid
        fname = os.path.join(DEFAULT_LOGGING_PATH, botid) + '.dump'

    if not os.path.isfile(fname):
        print(bold('Given file does not exist: {}'.format(fname)))
        exit(1)
    while True:
        info = dump_info(fname)
        print('Processing {}: {}'.format(bold(botid), info))
        # Determine bot status
        bot_status = ctl.bot_status(botid)
        if bot_status == 'running':
            print(red('Attention: This bot is currently running!'))
        elif bot_status == 'error':
            print(red('Attention: This bot is not defined!'))

        if info.startswith(str(red)):
            available_opts = [item[0] for item in ACTIONS.values() if item[2]]
            print('Restricted actions.')
        else:
            with open(fname, 'rt') as handle:
                content = json.load(handle)
            meta = load_meta(content)
            available_opts = [item[0] for item in ACTIONS.values()]
            for count, line in enumerate(meta):
                print('{:3}: {} {}'.format(count, *line))
        answer = input(inverted(', '.join(available_opts) + '?') + ' ').split()
        if not answer:
            continue
        if any([answer[0] == char for char in AVAILABLE_IDS]):
            ids = [int(item) for item in answer[1].split(',')]
        queue_name = None
        if answer[0] == 'a':
            # recover all -> recover all by ids
            answer[0] = 'r'
            ids = range(len(meta))
            if len(answer) > 1:
                queue_name = answer[1]
        if answer[0] == 'q':
            break
        elif answer[0] == 'e':
            # Delete entries
            for entry in ids:
                del content[meta[entry][0]]
            save_file(fname, content)
        elif answer[0] == 'r':
            # recover entries
            default = utils.load_configuration(DEFAULTS_CONF_FILE)
            runtime = utils.load_configuration(RUNTIME_CONF_FILE)
            params = utils.load_parameters(default, runtime)
            pipe = pipeline.PipelineFactory.create(params)
            for i, (key, entry) in enumerate([item for (count, item)
                                              in enumerate(content.items()) if count in ids]):
                if entry['message']:
                    msg = entry['message']
                else:
                    print('No message here, deleting entry.')
                    del content[key]
                    save_file(fname, content)
                    continue

                if queue_name is None:
                    if len(answer) == 3:
                        queue_name = answer[2]
                    else:
                        queue_name = entry['source_queue']
                try:
                    pipe.set_queues(queue_name, 'destination')
                    pipe.connect()
                    pipe.send(msg)
                except exceptions.PipelineError:
                    print(red('Could not reinject into queue {}: {}'
                              ''.format(queue_name, traceback.format_exc())))
                else:
                    del content[key]
                    save_file(fname, content)
                    print(green('Recovered dump {}.'.format(i)))
            if not content:
                os.remove(fname)
                print('Deleted empty file {}'.format(fname))
                break
        elif answer[0] == 'd':
            # delete dumpfile
            os.remove(fname)
            print('Deleted file {}'.format(fname))
            break
        elif answer[0] == 's':
            # Show entries by id
            for count, (key, value) in enumerate(content.items()):
                if count not in ids:
                    continue
                print('=' * 100, '\nShowing id {} {}\n'.format(count, key),
                      '-' * 50)
                if isinstance(value['message'], (bytes, str)):
                    value['message'] = json.loads(value['message'])
                    if ('raw' in value['message'] and
                            len(value['message']['raw']) > 1000):
                        value['message']['raw'] = value['message'][
                            'raw'][:1000] + '...[truncated]'
                value['traceback'] = value['traceback'].splitlines()
                pprint.pprint(value)

if __name__ == '__main__':
    main()
