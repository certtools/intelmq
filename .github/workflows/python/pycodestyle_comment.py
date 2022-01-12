"""
pycodestyle_comment.py
Post output of pycodestyle as a review to a github PR

SPDX-FileCopyrightText: 2020 Birger Schacht
SPDX-License-Identifier: AGPL-3.0-or-later
"""
import os
import subprocess

import github

INTROTEXT_IDENTIFIER = '<!-- Introtext. -->'
INTROTEXT = INTROTEXT_IDENTIFIER + '''\nHi, thanks for your contribution :blush:!
Unfortunately there are a couple of style problems that have to be fixed, before your contribution can be reviewed by humans :sweat_smile:.
Below you\'ll find the output of the `pycodestyle` checker, please try to fix your contribution so that `pycodestyle` doesn't find any problems.
You can also run the checker yourself using `pycodestyle intelmq/{bots,lib,bin}`. If you have any question don\'t hesitate to ask!\n\n'''

VOIDTEXT_IDENTIFIER = '<!-- Voidtext. -->'
VOIDTEXT = VOIDTEXT_IDENTIFIER + '\n*Void due to subsequent changes.*'


def list_style_errors() -> str:
    """ Run pycodestyle on the relevant directories and return the output as a list of strings."""
    repopath = os.getenv('GITHUB_WORKSPACE')
    command = 'pycodestyle intelmq/bots intelmq/lib intelmq/bin'
    res = subprocess.run(command, shell=True, cwd=repopath, capture_output=True, check=False)
    stylerrors = res.stdout.decode().split('\n')

    return [line for line in stylerrors if line.strip() != '']


def style_error_format(style_error_list) -> str:
    """ Format the list of pycodestyle errors and return them a one string. """
    ret = ''
    for error in style_error_list:
        ret += '* {}\n'.format(error)
    return ret


if __name__ == "__main__":
    # We use the GITHUB_HEAD_REF environment variable to verify
    # if this action really runs on a PR:
    if os.getenv('GITHUB_HEAD_REF', None):
        style_errors = list_style_errors()

        if style_errors:
            print("Found {} errors.".format(len(style_errors)))

        gh = github.Github()

        if gh:
            reviews = gh.get_reviews()
            for review in reviews:
                if review['user']['login'] == 'github-actions[bot]' and review['body'].startswith(INTROTEXT_IDENTIFIER):
                    gh.update_review(review['id'], VOIDTEXT)
            if len(style_errors) > 0:
                body = INTROTEXT + '```\n' + style_error_format(style_errors) + '```'
                gh.post_review(body)
    else:
        print("Not a pull request, therefore skipping this run.")
