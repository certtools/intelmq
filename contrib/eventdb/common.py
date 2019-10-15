#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug 26 10:09:56 2019

@author: sebastian
"""
import argparse


def create_parser(name, description):
    parser = argparse.ArgumentParser(name, description)
    parser.add_argument('--filename', '-f',
                        help="Path to mapping file name. Will be downloaded if not given.")
    parser.add_argument('--malware-name-column', '-m', default='malware.name',
                        help='Use this column as malware name, default: '
                             "'malware.name'")
    parser.add_argument('--malware-family-column', '-c',
                        default='classification.identifier',
                        help='Apply the mapping to this column, '
                             "default: 'classification.identifier'")
    parser.add_argument('--host', '-H', default='localhost',
                        help="PostgreSQL host, default: 'localhost'")
    parser.add_argument('--port', '-P', default=5432,
                        help='PostgreSQL port, default: 5432')
    parser.add_argument('--username', '-u', default='intelmq',
                        help="PostgreSQL username, default: 'intelmq'")
    parser.add_argument('--database', '-d', default='eventdb',
                        help="PostgreSQL database, default: 'eventdb'")
    parser.add_argument('--password', '-W', action='store_true',
                        help='PostgreSQL password, will be queried on stdin.')
    parser.add_argument('--table', '-t', default='events',
                        help="PostgreSQL table, default: 'events'")
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Do not apply the mapping and instead print the statements.')
    parser.add_argument('--where', '-w',
                        help='Optional additional SQL WHERE statement.')
    return parser
