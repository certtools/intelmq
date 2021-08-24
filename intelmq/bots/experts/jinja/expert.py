# SPDX-FileCopyrightText: 2021 Birger Schacht
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from intelmq.lib.bot import Bot
from intelmq.lib.exceptions import MissingDependencyError

import pathlib
import os
from typing import Union, Dict

try:
    from jinja2 import Template, TemplateError
except ImportError:
    Template = None


class JinjaExpertBot(Bot):
    """
    Modify the message using the Jinja templating engine
    Example:
        .. code-block:: yaml

        fields:
          output: The provider is {{ msg['feed.provider'] }}!
          feed.url: "{{ msg['feed.url'] | upper }}"
          extra.somejinjaoutput: file:///etc/intelmq/somejinjatemplate.j2
    """

    fields: Dict[str, Union[str, Template]] = {}
    overwrite: bool = False

    def init(self):
        if not Template:
            raise MissingDependencyError("Library 'jinja2' is required, please install it.")

        for field, template in self.fields.items():
            if template.startswith("file:///"):
                templatefile = pathlib.Path(template[7:])
                if templatefile.exists() and os.access(templatefile, os.R_OK):
                    self.fields[field] = templatefile.read_text()
                else:
                    raise ValueError(f"Jinja Template {templatefile} does not exist or is not readable.")

        for field, template in self.fields.items():
            try:
                self.fields[field] = Template(template)
            except TemplateError as msg:
                raise ValueError(f"Error parsing Jinja Template for '{field}': {msg}")

    def process(self):
        msg = self.receive_message()

        for field, template in self.fields.items():
            msg.add(field, template.render(msg=msg), overwrite=self.overwrite)

        self.send_message(msg)
        self.acknowledge_message()


BOT = JinjaExpertBot
