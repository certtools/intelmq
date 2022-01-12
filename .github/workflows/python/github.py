"""
github.py
Provide a couple of useful methods for github actions to interact with pull requests

SPDX-FileCopyrightText: 2020 Birger Schacht
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import os
import requests


class Github:
    """ Github class:
    contains a request session object that holds the authorization token
    """
    session = None
    api = 'https://api.github.com/'

    def __init__(self):
        self.github_token = os.getenv('GITHUB_TOKEN', None)
        self.github_repository = os.getenv('GITHUB_REPOSITORY', None)
        self.github_ref = os.getenv('GITHUB_REF', None)

        self.pr_id = int(self.github_ref.split('/')[2])

        if not self.github_token:
            raise AttributeError('GITHUB_TOKEN is not set.')

        self.session = requests.Session()
        self.session.headers['Authorization'] = 'token %s' % self.github_token

    def get_reviews(self):
        """ Get a list of reviews on a Github pull request as json object """
        reviews = self.session.get(self.api + 'repos/{}/pulls/{}/reviews'.format(self.github_repository, self.pr_id))
        reviews.raise_for_status()
        return reviews.json()

    def update_review(self, review_id, body):
        """ Update a review given by `review_id` and set its body to `body` """
        payload = {'body': body}
        resp = self.session.put(self.api + 'repos/{}/pulls/{}/reviews/{}'.format(self.github_repository, self.pr_id, review_id), json=payload)
        resp.raise_for_status()
        return resp.json()

    def post_review(self, body):
        """ Post a pull request review containing `body` and requesting changes """
        payload = {'body': body, 'event': "REQUEST_CHANGES"}
        resp = self.session.post(self.api + 'repos/{}/pulls/{}/reviews'.format(self.github_repository, self.pr_id), json=payload)
        resp.raise_for_status()
        return resp.json()
