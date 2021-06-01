<!--
SPDX-FileCopyrightText: 2019 Guillermo Rodriguez

SPDX-License-Identifier: AGPL-3.0-or-later
-->

Shadowserver test
==================

All Shadowserver parser tests will be placed in this directory. Files with data
for these tests are located in testdata directory. Besides one test file for
each type of report, there are also the following tests:

* `test_broken.py`: to test errors in the parser
* `test_testdata.py`: to test if the parsing of large original files
* `test_parameters.py`: to test the bot's parameters
