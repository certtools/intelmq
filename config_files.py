#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import argparse
import glob
import os


def rewrite(fobj):
    text = json.load(fobj)
    clean = json.dumps(text, indent=4, sort_keys=True, separators=(',', ': ')) + '\n'
    fobj.seek(0)
    fobj.write(clean)
    fobj.truncate()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Test files")
    parser.add_argument('-c', '--config', help='Path to the home directory.')
    args = parser.parse_args()

    config_file_path = args.config

    for fn in glob.glob(os.path.join(config_file_path, 'intelmq/etc/*.conf')):
        with open(fn, 'r+') as f:
            rewrite(f)

    with open(os.path.join(config_file_path, 'intelmq/bots/BOTS'), 'r+') as f:
        rewrite(f)
