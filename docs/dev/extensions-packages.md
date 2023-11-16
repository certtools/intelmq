<!-- comment
   SPDX-FileCopyrightText: 2023 CERT.at GmbH
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Creating extensions packages

IntelMQ supports adding additional bots using your own independent packages. You can use this to
add a new integration that is special to you, or cannot be integrated
into the main IntelMQ repository for some reason.

## Building an extension package

A simple example of the package can be found in ``contrib/example-extension-package``. To make your custom
bots work with IntelMQ, you need to ensure that

 - your bot's module exposes a ``BOT`` object of the class inherited from ``intelmq.lib.bot.Bot``
   or its subclasses,
 - your package registers an [entry point](https://packaging.python.org/en/latest/specifications/entry-points/)
   in the ``console_scripts`` group with a name starting with ``intelmq.bots.`` followed by
   the name of the group (collectors, experts, outputs, parsers), and then your original name.
   The entry point must point to the ``BOT.run`` method,
 - the module in which the bot resides must be importable by IntelMQ (e.g. installed in the same
   virtualenv, if you use them).

Apart from these requirements, your package can use any of the usual package features. We strongly
recommend following the same principles and main guidelines as the official bots. This will ensure
the same experience when using official and additional bots.

## Naming convention

Building your own extensions gives you a lot of freedom, but it's important to know that if your
bot's entry point uses the same name as another bot, it may not be possible to use it, or to
determine which one is being used. For this reason, we recommend that you start the name of your
bot with an with an organization identifier and then the bot name.

For example, if I create a collector bot for feed source ``Special`` and run it on behalf of the
organization ``Awesome``, the suggested entry point might be ``intelmq.bots.collectors.awesome.special``.
Note that the structure of your package doesn't matter, as long as it can be imported properly.

For example, I could create a package called ``awesome-bots`` with the following file structure

```text
   awesome_bots
   ├── pyproject.toml
   └── awesome_bots
        ├── __init__.py
        └── special.py
```

The [pyproject.toml](https://packaging.python.org/en/latest/specifications/declaring-project-metadata/#entry-points)
file would then have the following section:

```ini
   [project.scripts]
   intelmq.bots.collectors.awesome.special = "awesome_bots.special:BOT.run"
```

Once you have installed your package, you can run ``intelmqctl list bots`` to check if your bot was
properly registered.