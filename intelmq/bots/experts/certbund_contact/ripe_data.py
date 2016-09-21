#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This file is part of intelMQ RIPE importer.
#
# intelMQ RIPE importer is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# intelMQ RIPE importer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License

import gzip


def parse_file(filename, fields, index_field=None, verbose=False):
    '''Parses a file from the RIPE (split) database set.

    ftp://ftp.ripe.net/ripe/dbase/split/
    :param filename: the gziped filename
    :param fields: the field names to read
    :param index_field: the field that marks the beginning of a dataset.
        If not provided, the first element of 'fields' will be used
    :return: returns a list of lists with the read out values

    NOTE: Does **not** handle "continuation lines" (see rfc2622 section 2).

    NOTE: Preserves the contents of the fields like lower and upper case
          characters, though the RPSL is case insensitive and ASCII only.
          Thus for some fields it makes sense to upper() them (before
          comparing).
    '''
    if verbose:
        print('** Reading file {0}'.format(filename))

    out = []
    tmp = None

    f = gzip.open(filename, 'rt', encoding='latin1')
    if not index_field:
        index_field = fields[0]

    important_fields = list(fields) + [index_field]
    for line in f:

        # Comments and remarks
        if (line.startswith('%') or line.startswith('#')
            or line.startswith('remarks:')):
            continue

        if ":" in line:
            key, value = [x.strip() for x in line.split(":", 1)]

            # Fields we are interested in, plus the index
            if key not in important_fields:
                continue

            # If we reach the index again, we have reached the next dataset, add
            # the previous data and start again
            if key == index_field:
                if tmp: # template is filled, except on the first record
                    out.append(tmp)

                tmp = {}
                for tmp_field in fields:
                    if not tmp.get(tmp_field):
                        tmp[tmp_field] = []

            # Only add the fields we are interested in to the result set
            if key in fields:
                tmp[key].append(value)

    f.close()
    if verbose:
        print('   -> read {0} entries'.format(len(out)))
    return out
