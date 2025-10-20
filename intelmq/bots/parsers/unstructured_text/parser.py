# SPDX-FileCopyrightText: 2025 Aaron Kaplan, Institute for Common Good Technology
#
# SPDX-License-Identifier: AGPL-3.0-or-later

r"""

A unstructred CTI report to IntelMQ IDF parser.
Builds on top of [cti.tools](https://github.com/ctitools)

"""

import os

from intelmq.lib.bot import ParserBot, utils
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.exceptions import MissingDependencyError

from pydantic import BaseModel, ValidationError
from typing import List
from pydantic_ai import Agent

from intelmq.lib.basemodel import IntelMQEventModel

from pprint import pprint


# =====================
# Langfuse
from langfuse import Langfuse

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://cloud.langfuse.com",
)


def extract_data(text: str, model: str, api_key: str, logger, maximum_attempts: int = 5) -> List[IntelMQEventModel]:
    """Use an LLM (part of the config which one) to extract IDF-style events from the raw text.
    We use ai.pydantic.dev for telling the LLM to extract and map all information from the (unstructured) `text` to the IntelMQ Data Format
    (see https://docs.intelmq.org/latest/user/event/) for a description of the IntelMQ Data Format (IDF)
    """
    # Initialize the LLM provider
    logger.info("Using model: %r", model)
    # Initialize Pydantic AI instrumentation
    agent = Agent(model, output_type=List[IntelMQEventModel])

    for attempt in range(maximum_attempts):
        try:
            result = agent.run_sync(text)
        except ValidationError as exc:
            print(f'Got invalid result: ({exc!r}. Trying again ({attempt}/{maximum_attempts}).')
            pass
        else:
            break
    logger.info('Usage: %r', result)
    return result


class UnstructuredText(ParserBot):
    model: str = "openai:gpt-5"
    api_key: str = os.getenv("OPENAI_API_KEY") or ""

    def process(self):
        report = self.receive_message()
        text = utils.base64_decode(report["raw"])
        # here we got a list of dicts which contain data which may be mapped to intelmq data format
        result = extract_data(text, self.model, self.api_key, self.logger)
        events = result.response.parts[0].args_as_dict()['response']

        # now we go over all these dicts
        for e in events:
            # make an empty intelmq event
            event = self.new_event()

            # now map the fields into the intelmq event which map naturally
            event.update(e)
            # keep the raw data
            event.add("raw", text, overwrite=True)

            # for all other key/values in the dict, add them to 'extra.*'
            self.send_message(event)
        self.acknowledge_message()


BOT = UnstructuredText

if __name__ == '__main__':
    with open("intelmq/bots/parsers/unstructured_text/test_data/sample.txt", "r") as f:
        SAMPLE_CONTENT = f.read()

        result = extract_data(SAMPLE_CONTENT, model="openai:gpt-4o", api_key=os.getenv("OPENAI_API_KEY"))
        events = result.response.parts[0].args_as_dict()['response']
        for i, event in enumerate(events):
            print(f'Result {i}:')
            pprint(event)
