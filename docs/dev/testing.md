<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Testing

## Additional test requirements

Libraries required for tests are listed in the `setup.py` file. You can install them with pip:

```bash
pip3 install -e .[development]
```

or the package management of your operating system.

## Run the tests

All changes have to be tested and new contributions should be accompanied by according unit tests. Please do not run the
tests as root just like any other IntelMQ component for security reasons. Any other unprivileged user is possible.

You can run the tests by changing to the directory with IntelMQ repository and running either `unittest` or
`pytest`. For virtual environment installation, please activate it and omit the `sudo -u` from examples below:

```bash
cd $INTELMQ_REPO
sudo -u intelmq python3 -m unittest {discover|filename}  # or
sudo -u intelmq pytest [filename]
sudo -u intelmq python3 setup.py test  # uses a build environment (no external dependencies)
```

Some bots need local databases to succeed. If you only want to test one explicit test file, give the file path as
argument.

There are multiple [GitHub Action Workflows](https://github.com/certtools/intelmq/actions) setup for automatic testing,
which are triggered on pull requests. You can also easily activate them for your forks.

## Environment variables

There are a bunch of environment variables which switch on/off some tests:

| Environment&nbsp;Variable&nbsp;Name | Description |
|-------------------- | ------------|
| `INTELMQ_TEST_DATABASES`  | databases such as postgres, elasticsearch, mongodb are not tested by default. Set this environment variable to 1 to test those bots. These tests need preparation, e.g. running databases with users and certain passwords etc. Have a look at the `.github/workflows/unittests.yml` and the corresponding `.github/workflows/scripts/setup-full.sh` in IntelMQ's repository for steps to set databases up. |
| `INTELMQ_SKIP_INTERNET`  | tests requiring internet connection will be skipped if this is set to 1. |
| `INTELMQ_SKIP_REDIS`  | redis-related tests are ran by default, set this to 1 to skip those. |
| `INTELMQ_TEST_EXOTIC`  | some bots and tests require libraries which may not be available, those are skipped by default. To run them, set this to 1. |
| `INTELMQ_TEST_REDIS_PASSWORD`  | Set this value to the password for the local redis database if needed. |
| `INTELMQ_LOOKYLOO_TEST`  | Set this value to run the lookyloo tests. Public lookyloo instance will be used as default. |
| `INTELMQ_TEST_INSTALLATION` | Set this value to run tests which require a local IntelMQ installation, such as for testing the command lines tools relying on configuration files, dump files etc. |

For example, to run all tests you can use:

```bash
INTELMQ_TEST_DATABASES=1 INTELMQ_TEST_EXOTIC=1 pytest intelmq/tests/
```

## Configuration test files

The tests use the configuration files in your working directory, not those installed in `/opt/intelmq/etc/` or `/etc/`. You can run the tests for a locally changed intelmq without affecting an installation or requiring root to run them.