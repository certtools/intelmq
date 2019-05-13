#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
import glob
import json
import os
import traceback

from intelmq.lib.utils import object_pair_hook_bots


def rewrite(fobj, bots=False):
    if not bots:
        text = json.load(fobj)
    else:
        text = json.load(fobj, object_pairs_hook=object_pair_hook_bots)
    if not bots:
        clean = json.dumps(text, indent=4, sort_keys=True, separators=(',', ': ')) + '\n'
    else:
        clean = json.dumps(text, indent=4, separators=(',', ': ')) + '\n'
    fobj.seek(0)
    fobj.write(clean)
    fobj.truncate()


if __name__ == '__main__':  # pragma: no cover
    DESCRIPTION = """
    Rewrites JSON configuration files for developers of intelmq.

    Corrections:
        Indentation, sorting, separators
    """
    parser = argparse.ArgumentParser(prog='rewrite_config_files.py',
                                     description="Test files")
    parser.add_argument('-c', '--config',
                        help='Path to the intelmq directory containing'
                             'bots/BOTS, etc/*.conf',
                        default='.')
    args = parser.parse_args()

    config_file_path = args.config

    try:
        for fn in glob.glob(os.path.join(config_file_path, 'etc/*.conf')):
            with open(fn, 'r+') as f:
                rewrite(f)

        with open(os.path.join(config_file_path, 'bots/BOTS'), 'r+') as f:
            rewrite(f, bots=True)
    except IOError:
        traceback.print_exc()
        print('Could not open files. Wrong directory? Also see the --help.')
