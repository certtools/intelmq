# SPDX-FileCopyrightText: 2019 Tomas Bellus
#
# SPDX-License-Identifier: AGPL-3.0-or-later

# -*- coding: utf-8 -*-
"""
GITHUB contents API Collector bot

PARAMETERS:
    'basic_auth_username': github Basic authentication username (REQUIRED)
    'basic_auth_password': github Basic authentication password (REQUIRED)
    'repository': only one format ('<author>/<repo>') is acceptable (REQUIRED)
    'extra_fields': comma-separated list of fields to extract from file (DEFAULT = [])
    'regex': file regex (DEFAULT = '*.json')
"""
import re

from intelmq.lib.exceptions import InvalidArgument
from intelmq.bots.collectors.github_api._collector_github_api import GithubAPICollectorBot

try:
    import requests
except ImportError:
    requests = None


class GithubContentsAPICollectorBot(GithubAPICollectorBot):
    "Collect files from a GitHub repository via the API. Optionally with GitHub credentials."
    regex: str = None  # TODO: could be re
    repository: str = None
    extra_fields = None

    def init(self):
        super().init()
        if self.repository is not None:
            self.__base_api_url = 'https://api.github.com/repos/{}/contents'.format(self.repository)
        else:
            raise InvalidArgument('repository', expected='string')

        if self.regex is not None:
            try:
                re.compile(self.regex)
            except Exception:
                raise InvalidArgument('regex', expected='string', got=self.regex)
        else:
            raise InvalidArgument('regex', expected='string', got=None)

        if self.extra_fields is not None:
            try:
                self.__extra_fields = [x.strip() for x in self.extra_fields.split(',')]
            except Exception:
                raise InvalidArgument('extra_fields', expected='comma-separated list')
        else:
            self.__extra_fields = []

    def process_request(self):
        try:
            for item in self.__recurse_repository_files(self.__base_api_url):
                report = self.new_report()
                report['raw'] = item['content']
                report['feed.url'] = item['download_url']
                if item['extra'] != {}:
                    report.add('extra.file_metadata', item['extra'])
                self.send_message(report)
        except requests.RequestException as e:
            raise ConnectionError(e)

    def __recurse_repository_files(self, base_api_url: str, extracted_github_files: list = None) -> list:
        if extracted_github_files is None:
            extracted_github_files = []
        data = self.github_api(base_api_url)
        for github_file in data:
            if github_file['type'] == 'dir':
                extracted_github_files = self.__recurse_repository_files(github_file['url'], extracted_github_files)
            elif github_file['type'] == 'file' and bool(re.search(self.regex, github_file['name'])):
                extracted_github_file_data = {
                    'download_url': github_file['download_url'],
                    'content': requests.get(github_file['download_url']).content,
                    'extra': {}
                }
                for field_name in self.__extra_fields:
                    if field_name in github_file:
                        extracted_github_file_data['extra'][field_name] = github_file[field_name]
                    else:
                        self.logger.warning("Field '{}' does not exist in the Github file data.".format(field_name))
                extracted_github_files.append(extracted_github_file_data)

        return extracted_github_files


BOT = GithubContentsAPICollectorBot
