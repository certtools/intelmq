<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Intro

This guide is for developers of IntelMQ. It explains the code architecture, coding guidelines as well as ways you can contribute code or documentation. If you have not done so, please read the
User Guide and the Administrator Guide first. Once you feel comfortable running IntelMQ with open source bots and you feel adventurous enough to contribute to the project, this guide is for you. It does not matter if you are an experienced Python programmer or just a beginner. There is a lot of examples to help you out.

However, before we go into the details, it is important to observe and internalize some overall project goals.

## Goals

It is important, that all developers agree and stick to these meta-guidelines. IntelMQ tries to:

- Be well tested. For developers this means, we expect you to write unit tests for bots. Every time.
- Reduce the complexity of system administration.
- Reduce the complexity of writing new bots for new data feeds.
- Make your code easily and pleasantly readable.
- Reduce the probability of events lost in all process with persistence functionality (even system crash).
- Strictly adhere to the existing format for keys and values in events.
- Always use JSON format for all messages internally.
- Help and support the interconnection between IntelMQ and existing tools like AbuseHelper, CIF, etc. or new tools (in other words: we will not accept data-silos!).
- Provide an easy way to store data into log collectors such as ElasticSearch or Splunk.
- Provide an easy way to create your own black-lists.
- Provide easy to understand interfaces with other systems via HTTP RESTFUL API.

The main take away point from the list above is: things **MUST** stay _intuitive_ and _easy_. How do you ultimately test if things are still easy? Let them new programmers test-drive your features and if it is not understandable in 15 minutes, go back to the drawing board.

Similarly, if code does not get accepted upstream by the main developers, it is usually only because of the ease-of-use argument. Do not give up, go back to the drawing board, and re-submit again.

## Mailing list

There is a separate mailing list for developers to discuss development topics:
The [IntelMQ-DevArchive](https://lists.cert.at/pipermail/intelmq-dev/) is public as well.

## GitHub

The ideal way to propose changes and additions to IntelMQ is to open
a [Pull Request](https://github.com/certtools/intelmq/pulls) on GitHub.