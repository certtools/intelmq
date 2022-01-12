#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2016 Sebastian Wagner
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-

import argparse
import glob
import json
import os
import traceback


def rewrite(fobj):
    text = json.load(fobj)
    clean = json.dumps(text, indent=4, sort_keys=True, separators=(',', ': ')) + '\n'
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
                             'etc/*.conf',
                        default='.')
    args = parser.parse_args()

    config_file_path = args.config

    try:
        for fn in glob.glob(os.path.join(config_file_path, 'etc/*.conf')):
            with open(fn, 'r+') as f:
                rewrite(f)

    except IOError:
        traceback.print_exc()
        print('Could not open files. Wrong directory? Also see the --help.')
