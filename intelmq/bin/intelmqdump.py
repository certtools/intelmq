# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import argparse
import base64
import copy
import fcntl
import glob
import json
import os.path
import pprint
import re
import readline
import subprocess
import sys
import tempfile
import traceback
from collections import OrderedDict
from pathlib import Path

from termstyle import bold, green, inverted, red

import intelmq.bin.intelmqctl as intelmqctl
import intelmq.lib.exceptions as exceptions
import intelmq.lib.message as message
import intelmq.lib.pipeline as pipeline
import intelmq.lib.utils as utils
from intelmq import DEFAULT_LOGGING_LEVEL, DEFAULT_LOGGING_PATH

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
- d, Delete entries by IDs
  > d id{,id}
  > d 3,5
  The entries will be deleted from the dump file.
- d, Delete file
  > d
  Delete the opened file as a whole.
- s, Show by IDs
  > s id{,id}
  > s 0,4,5
  Show the selected IP in a readable format. It's still a raw format from
  repr, but with newlines for message and traceback.
- e, Edit by ID
  > e id
  > e 0
  > e 1,2
  Opens an editor (by calling `sensible-editor`) on the message. The modified message is then saved in the dump.
- q, Quit
  > q
"""
USAGE = '''
    intelmqdump [botid]
    intelmqdump [-h|--help]'''
# shortcut: description, takes ids, available for corrupted files
ACTIONS = {'r': ('(r)ecover by ids', True, False),
           'a': ('recover (a)ll', False, False),
           'd': ('(d)elete file or entries by id', True, False),
           's': ('(s)how by ids', True, False),
           'q': ('(q)uit', False, True),
           'e': ('(e)dit by id', True, False),
           }
AVAILABLE_IDS = [key for key, value in ACTIONS.items() if value[1]]


def dump_info(fname, file_descriptor=None):
    info = red('unknown error')
    if not os.path.getsize(fname):
        info = red('empty file')
    else:
        try:
            if file_descriptor is None:
                handle = open(fname)
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            else:
                handle = file_descriptor
        except BlockingIOError:
            info = red('Dump file is locked.')
        except OSError as exc:
            info = red(f'unable to open file: {exc!s}')
        else:
            try:
                content = json.load(handle)
            except ValueError as exc:
                info = red(f'unable to load JSON: {exc!s}')
            else:
                try:
                    info = f"{len(content.keys())!s} dumps"
                except AttributeError as exc:
                    info = red(f"unable to count dumps: {exc!s}")
        finally:
            try:
                if file_descriptor is None:
                    handle.close()
            except NameError:
                pass
    return info


def save_file(handle, content):
    handle.truncate()
    try:
        json.dump(content, handle, indent=4, sort_keys=True)
    except KeyboardInterrupt:
        print('Got KeyboardInterrupt, saving file before exit.', file=sys.stderr)
        json.dump(content, handle, indent=4, sort_keys=True)
        sys.exit(1)
    handle.seek(0)


def load_meta(dump):
    retval = []
    for key, value in dump.items():
        if type(value['traceback']) is not list:
            error = value['traceback'].splitlines()[-1]
        else:
            error = value['traceback'][-1].strip()
        if len(error) > 200:
            error = error[:100] + '...' + error[-100:]
        retval.append((key, error))
    return retval


class Completer():
    state = None
    queues = None

    def __init__(self, possible_values, queues=False):
        self.possible_values = possible_values
        self.queues = queues

    def complete(self, text, state):
        if state == 0:  # generate matches
            self.matches = []
            old_text = ''
            possible_values = self.possible_values
            match = re.search('^(r[ \t]+[0-9]+|a)[ \t]+', text)
            if self.queues and match:
                old_text, text = text[:match.span()[1]], text[match.span()[1]:]
                possible_values = self.queues
            for completion in possible_values:
                if completion.startswith(text):
                    self.matches.append(old_text + completion)
            self.matches.sort()
        try:
            return self.matches[state]
        except IndexError:
            return


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog=APPNAME,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage=USAGE,
        description=DESCRIPTION,
        epilog=EPILOG,
    )

    parser.add_argument('botid', metavar='botid', nargs='?',
                        default=None, help='botid to inspect dumps of')
    parser.add_argument('--truncate', '-t', type=int,
                        default=1000,
                        help='Truncate raw-data with more characters than given. '
                        '0 for no truncating. Default: 1000.')
    args = parser.parse_args(argv)
    if args.truncate < 1:
        args.truncate = None

    # Try to get log_level from defaults_configuration, else use default
    try:
        defaults = utils.get_global_settings()
    except Exception:
        log_level = DEFAULT_LOGGING_LEVEL

    try:
        logger = utils.log('intelmqdump',
                           log_level=defaults.get('logging_level', DEFAULT_LOGGING_LEVEL),
                           log_max_size=defaults.get("logging_max_size", 0),
                           log_max_copies=defaults.get("logging_max_copies", None),
                           log_path=defaults.get("logging_path", DEFAULT_LOGGING_PATH))
    except (FileNotFoundError, PermissionError) as exc:
        logger = utils.log('intelmqdump', log_level=log_level, log_path=False)
        logger.error('Not logging to file: %s', exc)

    ctl = intelmqctl.IntelMQController()
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims('')

    defaults = utils.get_global_settings()
    runtime_config = utils.get_runtime()
    pipeline_pipes = {}
    logging_paths = {defaults.get('logging_path', DEFAULT_LOGGING_PATH)}
    for bot, settings in runtime_config.items():
        pipeline_pipes[settings.get('source_queue', f"{bot}-queue")] = bot
        logging_paths.add(settings.get("parameters", {}).get('logging_path', DEFAULT_LOGGING_PATH))

    if args.botid is None:
        filenames = list()
        for path in logging_paths:
            filenames.extend(glob.glob(os.path.join(path, '*.dump')))

        if not len(filenames):
            print(green('Nothing to recover from, no dump files found!'))
            sys.exit(0)
        filenames = [(fname, Path(fname).name[:-5])
                     for fname in sorted(filenames)]

        length = max(len(value[1]) for value in filenames)
        print(bold("{c:>3}: {s:{length}} {i}".format(c='id', s='name (bot id)',
                                                     i='content',
                                                     length=length)))
        for count, (fname, shortname) in enumerate(filenames):
            info = dump_info(fname)
            print("{c:3}: {s:{length}} {i}".format(c=count, s=shortname, i=info,
                                                   length=length))
        try:
            bot_completer = Completer(possible_values=[f[1] for f in filenames])
            readline.set_completer(bot_completer.complete)
            botid = input(inverted('Which dump file to process (id or name)?') +
                          ' ')
        except EOFError:
            sys.exit(0)
        else:
            botid = botid.strip()
            if botid == 'q' or not botid:
                exit(0)
        try:
            fname, botid = filenames[int(botid)]
        except ValueError:
            fname = [path for path, filename in filenames if filename == botid]
            if len(fname) > 1:
                print(bold('Given filename is not unique, please use number'))
                exit(1)
            fname = fname[0]
    else:
        botid = args.botid
        logging_path = utils.get_bots_settings(botid)["parameters"].get(
            "logging_path", DEFAULT_LOGGING_PATH)
        fname = os.path.join(logging_path, botid) + '.dump'

    if not os.path.isfile(fname):
        print(bold(f'Given file does not exist: {fname}'))
        exit(1)

    answer = None
    delete_file = False
    while True:
        with open(fname, 'r+') as handle:
            try:
                fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                print(red('Dump file is currently locked. Stopping.'))
                break
            info = dump_info(fname, file_descriptor=handle)
            handle.seek(0)
            available_answers = ACTIONS.keys()
            print(f'Processing {bold(botid)}: {info}')

            if info.startswith(str(red)):
                available_opts = [item[0] for item in ACTIONS.values() if item[2]]
                available_answers = [k for k, v in ACTIONS.items() if v[2]]
                print('Restricted actions.')
            else:
                # don't display list after 'show', 'recover' & edit commands
                if not (answer and isinstance(answer, list) and answer[0] in ['s', 'r', 'e']):
                    content = json.load(handle)
                    handle.seek(0)
                    content = OrderedDict(sorted(content.items(), key=lambda t: t[0]))  # sort by key here, #1280
                    meta = load_meta(content)

                    available_opts = [item[0] for item in ACTIONS.values()]
                    for count, line in enumerate(meta):
                        print('{:3}: {} {}'.format(count, *line))

            # Determine bot status
            try:
                bot_status = ctl.bot_status(botid)
                if bot_status[1] == 'running':
                    print(red('This bot is currently running, the dump file is now locked and '
                              'the bot can\'t write it.'))
            except KeyError:
                bot_status = 'error'
                print(red('Attention: This bot is not defined!'))
                available_opts = [item[0] for item in ACTIONS.values() if item[2]]
                available_answers = [k for k, v in ACTIONS.items() if v[2]]
                print('Restricted actions.')

            try:
                possible_answers = list(available_answers)
                for id_action in ['r', 'a']:
                    if id_action in possible_answers:
                        possible_answers[possible_answers.index(id_action)] = id_action + ' '
                action_completer = Completer(possible_answers, queues=pipeline_pipes.keys())
                readline.set_completer(action_completer.complete)
                answer = input(inverted(', '.join(available_opts) + '?') + ' ').split()
            except EOFError:
                break
            else:
                if not answer:
                    continue
            if len(answer) == 0 or answer[0] not in available_answers:
                print('Action not allowed.')
                continue
            if any([answer[0] == char for char in AVAILABLE_IDS]) and len(answer) > 1:
                ids = [int(item) for item in answer[1].split(',')]
            else:
                ids = []
            queue_name = None
            if answer[0] == 'a':
                # recover all -> recover all by ids
                answer[0] = 'r'
                ids = range(len(meta))
                if len(answer) > 1:
                    queue_name = answer[1]
            if answer[0] == 'q':
                break
            elif answer[0] == 'r':
                # recover entries
                params = defaults.copy()
                params.update(runtime_config[botid].get("parameters", {}))
                pipe = pipeline.PipelineFactory.create(logger=logger, pipeline_args=params)
                try:
                    for i, (key, entry) in enumerate([item for (count, item)
                                                      in enumerate(content.items()) if count in ids]):
                        if entry['message']:
                            msg = copy.copy(entry['message'])  # otherwise the message field gets converted
                            if isinstance(msg, dict):
                                msg = json.dumps(msg)
                        else:
                            print('No message here, deleting entry.')
                            del content[key]
                            continue

                        if queue_name is None:
                            if len(answer) == 3:
                                queue_name = answer[2]
                            else:
                                queue_name = entry['source_queue']
                        if queue_name in pipeline_pipes:
                            if runtime_config[pipeline_pipes[queue_name]]['group'] == 'Parser' and json.loads(msg)['__type'] == 'Event':
                                print('Event converted to Report automatically.')
                                msg = message.Report(message.MessageFactory.unserialize(msg)).serialize()
                        else:
                            print(red(f"The given queue '{queue_name}' is not configured. Please retry with a valid queue."))
                            break
                        try:
                            pipe.set_queues(queue_name, 'destination')
                            pipe.connect()
                            pipe.send(msg)
                        except exceptions.PipelineError:
                            print(red('Could not reinject into queue {}: {}'
                                      ''.format(queue_name, traceback.format_exc())))
                        else:
                            del content[key]
                            print(green(f'Recovered dump {i}.'))
                finally:
                    save_file(handle, content)
                if not content:
                    delete_file = True
                    print(f'Deleting empty file {fname}')
                    break
            elif answer[0] == 'd':
                # Delete entries or file
                if ids:
                    # delete entries
                    for entry in ids:
                        del content[meta[entry][0]]
                    save_file(handle, content)
                else:
                    # delete dumpfile
                    delete_file = True
                    print(f'Deleting file {fname}')
                    break
            elif answer[0] == 's':
                # Show entries by id
                for count, (key, orig_value) in enumerate(content.items()):
                    value = copy.copy(orig_value)  # otherwise the raw field gets truncated
                    if count not in ids:
                        continue
                    print('=' * 100, f'\nShowing id {count} {key}\n',
                          '-' * 50)
                    if value.get('message_type') == 'base64':
                        if args.truncate and len(value['message']) > args.truncate:
                            value['message'] = value['message'][:args.truncate] + '...[truncated]'
                    else:
                        if isinstance(value['message'], (bytes, str)):
                            value['message'] = json.loads(value['message'])
                            if (args.truncate and 'raw' in value['message'] and
                                    len(value['message']['raw']) > args.truncate):
                                value['message']['raw'] = value['message'][
                                    'raw'][:args.truncate] + '...[truncated]'
                    if type(value['traceback']) is not list:
                        value['traceback'] = value['traceback'].splitlines()
                    pprint.pprint(value)
            elif answer[0] == 'e':
                # edit given id
                if not ids:
                    print(red('Edit mode needs an id'))
                    continue
                for entry in ids:
                    if content[meta[entry][0]].get('message_type') == 'base64':
                        with tempfile.NamedTemporaryFile(mode='w+b', suffix='.txt') as tmphandle:
                            filename = tmphandle.name
                            tmphandle.write(base64.b64decode(content[meta[entry][0]]['message']))
                            tmphandle.flush()
                            proc = subprocess.run(['sensible-editor', filename])
                            if proc.returncode != 0:
                                print(red('Calling editor failed with exitcode %r.' % proc.returncode))
                            else:
                                tmphandle.seek(0)
                                new_content = tmphandle.read()
                                try:
                                    new_content = new_content.decode()
                                except UnicodeDecodeError as exc:
                                    print(red("Could not write the new message because of the following error:"))
                                    print(red(exceptions.DecodingError(exception=exc)))
                                else:
                                    del content[meta[entry][0]]['message_type']
                                    content[meta[entry][0]]['message'] = new_content
                                    save_file(handle, content)
                    else:
                        with tempfile.NamedTemporaryFile(mode='w+t', suffix='.json') as tmphandle:
                            filename = tmphandle.name
                            utils.write_configuration(configuration_filepath=filename,
                                                      content=json.loads(content[meta[entry][0]]['message']),
                                                      new=True,
                                                      backup=False, useyaml=False)
                            proc = subprocess.run(['sensible-editor', filename])
                            if proc.returncode != 0:
                                print(red('Calling editor failed with exitcode %r.' % proc.returncode))
                            else:
                                tmphandle.seek(0)
                                content[meta[entry][0]]['message'] = tmphandle.read()
                                save_file(handle, content)

    if delete_file:
        os.remove(fname)


if __name__ == '__main__':  # pragma: no cover
    main()
