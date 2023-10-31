<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Documentation

The documentation is automatically published to <https://docs.intelmq.org> at every push to the develop branch of the repository.

To build the documentation you need additional packages:

```bash
pip3 install .[development]
```

Then use the Makefile to build the documentation using mkdocs:

```bash
make docs
```

Some parts of the documentation are automatically generated using dedicated scripts. You can find them in the Makefile.
