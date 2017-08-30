# -*- coding: utf-8 -*-
import argparse
import logging
import os

from textx.exceptions import TextXError
from textx.metamodel import metamodel_from_file


class Validator(object):

    def __init__(self):
        self.logger = logging.getLogger()

        grammarfile = os.path.join(os.path.dirname(__file__), 'sieve.tx')
        if not os.path.exists(grammarfile):
            self.logger.error('Sieve grammar file not found: %r.', grammarfile)
            return

        try:
            self.metamodel = metamodel_from_file(grammarfile)
        except TextXError as e:
            self.logger.error('Could not process sieve grammar file. Error in (%d, %d).', e.line, e.col)
            self.logger.error(str(e))

    def parse(self, filename):
        if not self.metamodel:
            self.logger.error('Metamodel not loaded.')
            return

        if not os.path.exists(filename):
            self.logger.error('File does not exist: %r', filename)
            return

        try:
            self.metamodel.model_from_file(filename)
        except TextXError as e:
            self.logger.error('Could not process sieve file %r.', filename)
            self.logger.error('Error in (%d, %d).', e.line, e.col)
            self.logger.error(str(e))
            return

        self.logger.info('Sieve file %r parsed successfully.', filename)


def main():  # pragma: nocover
    logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)
    parser = argparse.ArgumentParser(description="Validates the syntax of sievebot files.")
    parser.add_argument('sievefile', help='Sieve file')

    args = parser.parse_args()

    validator = Validator()
    validator.parse(args.sievefile)


if __name__ == "__main__":  # pragma: nocover
    main()
