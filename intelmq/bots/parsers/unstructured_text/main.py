#!/usr/bin/env python3
# SPDX-FileCopyrightText: 2025 Aaron Kaplan
#
# SPDX-License-Identifier: AGPL-3.0-or-later
"""IntelMQ CTI Extractor - Extract security events from threat intelligence reports"""

import os
import sys
import json
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from pydantic_ai import Agent
from intelmq.lib.basemodel import IntelMQEventModel

load_dotenv()

SYSTEM_PROMPT = """Extract complete IntelMQ-formatted security events with ALL indicators of compromise (IOCs).

RULES:
1. Extract EVERY malware hash, IP, domain, URL as separate events
2. Malware samples: classification.taxonomy='malicious-code', type='malware', use malware.sha256/sha1/md5
3. Infrastructure: type='c2-server' or 'malware-distribution', extract to source fields
4. Normalize defanged indicators (hxxp→http, [.]→.)
5. Add feed.name, TLP levels, campaign names to classification.identifier
6. Add a short summary of the report into the field "event_description.text"
7. Be comprehensive - one event per unique IOC"""


def extract(text: str, model: str = None, quiet: bool = False, maximum_attempts: int = 5) -> list:
    """Extract IntelMQ events from text"""
    model = model or os.getenv('PYDANTIC_AI_MODEL', 'openrouter:google/gemini-2.5-flash')

    if not quiet:
        print(f'Model: {model}\nAnalyzing {len(text)} chars...\n')

    agent = Agent(model, output_type=List[IntelMQEventModel], system_prompt=SYSTEM_PROMPT, retries=maximum_attempts)
    result = agent.run_sync(text)

    if not quiet:
        print(f"✅ Extracted {len(result.output)} events")
        print(f"📊 Tokens: {result.usage()}\n")

    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: extract.py <input_file> [output.json]")
        print("\nEnvironment:")
        print("  PYDANTIC_AI_MODEL - Model to use (default: google/gemini-2.5-flash)")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2]) if len(sys.argv) > 2 else input_file.with_suffix('.json')

    if not input_file.exists():
        print(f"Error: {input_file} not found")
        sys.exit(1)

    # Extract events
    text = input_file.read_text()
    result = extract(text)
    events = result.response.parts[0].args_as_dict()['response']

    # Export to JSON
    output_file.write_text(json.dumps(events, indent=2))

    print(f"✅ Saved {len(events)} events to {output_file}")


if __name__ == "__main__":
    main()
