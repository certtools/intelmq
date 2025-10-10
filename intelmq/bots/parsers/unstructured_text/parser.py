#
# SPDX-License-Identifier: AGPL-3.0-or-later

r"""

A unstructred CTI report to IntelMQ IDF parser.
Builds on top of [cti.tools](https://github.com/ctitools)

"""

import os

from intelmq.lib.bot import ParserBot, utils
from intelmq.lib.exceptions import InvalidArgument
from intelmq.lib.harmonization import ClassificationType
from intelmq.lib.exceptions import MissingDependencyError

from pydantic import BaseModel, AfterValidator
from typing import Annotated, List
from pydantic_ai import Agent

import intelmq.lib.harmonization as harm
from intelmq.lib.utils import load_configuration
from requests import api

from pprint import pprint


# =====================
# Langfuse
from langfuse import Langfuse

langfuse = Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host="https://cloud.langfuse.com",
)

from basemodel import IntelMQEvent


def extract_data(text: str, model: str, api_key: str) -> List[IntelMQEvent]:
    """Use an LLM (part of the config which one) to extract IDF-style events from the raw text.
    We use ai.pydantic.dev for telling the LLM to extract and map all information from the (unstructured) `text` to the IntelMQ Data Format
    (see https://docs.intelmq.org/latest/user/event/) for a description of the IntelMQ Data Format (IDF)
    """
    # Initialize the LLM provider
    print(f"Using model: {model}")
    print(f"Api key: {api_key}...")
    # Initialize Pydantic AI instrumentation
    Agent.instrument_all()
    agent = Agent(model, output_type=IntelMQEvent)

    result = agent.run_sync(text)
    print(result.output)
    print(result.usage())
    pprint(result)
    return [result]


class UnstructuredText(ParserBot):
    model: str = "openai:gpt-5"
    api_key: str = os.getenv("OPENAI_API_KEY") or ""

    def process(self):
        report = self.receive_message()
        text = utils.base64_decode(report["raw"])
        # here we got a list of dicts which contain data which may be mapped to intelmq data format
        events = extract_data(text, self.model, self.api_key)

        # now we go over all these dicts
        for e in events:
            # make an empty intelmq event
            event = self.new_event(e)

            # now map the fields into the intelmq event which map naturally
            event.update(e)
            # keep the raw data
            event.add("raw", text, overwrite=True)

            # for all other key/values in the dict, add them to 'extra.*'
            self.send_message(event)
        self.acknowledge_message()


BOT = UnstructuredText

with open("intelmq/bots/parsers/unstructured_text/test_data/sample.txt", "r") as f:
    SAMPLE_CONTENT = f.read()

    result = extract_data(
        SAMPLE_CONTENT, model="openai:gpt-4o", api_key=os.getenv("OPENAI_API_KEY")
    )
    for r in result:
        print(r)
