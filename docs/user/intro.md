<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Intro

The User Guide provides information on how to use installed IntelMQ and it's components. Let's start with a basic not-so-technical description of how IntelMQ works and the used terminology:

- It consists of small (python) programs called **bots**.
- Bots communicate witch each other (using something called message broker) by passing so called **events** (JSON objects).
- An example event can look like this:

```json
{
    "source.geolocation.cc": "JO",
    "malware.name": "qakbot",
    "source.ip": "82.212.115.188",
    "source.asn": 47887,
    "classification.type": "c2-server",
    "extra.status": "offline",
    "source.port": 443,
    "classification.taxonomy": "malicious-code",
    "source.geolocation.latitude": 31.9522,
    "feed.accuracy": 100,
    "extra.last_online": "2023-02-16",
    "time.observation": "2023-02-16T09:55:12+00:00",
    "source.geolocation.city": "amman",
    "source.network": "82.212.115.0/24",
    "time.source": "2023-02-15T14:19:09+00:00",
    "source.as_name": "NEU-AS",
    "source.geolocation.longitude": 35.939,
    "feed.name": "abusech-feodo-c2-tracker"
  }
```

- Bots are divided into following groups:

    - **Collectors** - bots that collect data from sources such as website, mailbox, api, etc.
    - **Parsers** - bots that split and parse collected data into individual events.
    - **Experts** - bots that can do additional processing of events such as enriching, filtering, etc.
    - **Outputs** - bots that can output events to files, databases, etc.

- Data sources supported by IntelMQ are called **feeds**.
    - IntelMQ provides recommended configuration of collector and parser bot combinations for selected feeds.
- The collection of all configured bots and their communication paths is called **pipeline** (or **botnet**).
- Individual bots as well as the complete pipeline can be configured, managed and monitored via:
    - Web interface called **IntelMQ Manager** (best suited for regular users).
    - Command line tool called **intelmqctl** (best suited for administrators).
    - REST API provided by the **IntelMQ API** extension (best suited for other programs).