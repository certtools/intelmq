import pathlib
import subprocess
import os
import requests

from github import Github

introtext = '''Hi, thanks for your contribution :blush:! Unfortunately there are a couple of style problems that have to be fixed, before your contribution can be reviewed by humans :sweat_smile:.
Below you\'ll find the output of the `pycodestyle` checker, please try to fix your contribution so that `pycodestyle` doesn't find any more problems.
You can also run the checker yourself using `pycodestyle intelmq/{bots,lib,bin}`. If you have any question don\'t hesitate to ask.\n\n'''
voidtext = '*Void due to subsequent changes.*'

def list_style_errors() -> str:
    repopath = pathlib.Path(__file__).parent.parent.parent
    command = 'pycodestyle intelmq/bots intelmq/lib intelmq/bin'
    res = subprocess.run(command, shell = True, cwd=str(repopath), capture_output=True)
    stylerrors = res.stdout.decode().split('\n')

    return [line for line in stylerrors if line.strip() != '']

def style_error_format(style_errors) -> str:
    ret = ''
    for error in style_errors:
        ret += '* {}\n'.format(error)
    return ret

def main():
    print("Checking pull request for codestyle issues.")
    github_token = os.getenv('GITHUB_TOKEN', None)
    github_repository = os.getenv('GITHUB_REPOSITORY', None)
    github_ref = os.getenv('GITHUB_REF', None)

    pr_id = int(github_ref.split('/')[2])

    style_errors = list_style_errors()

    if not github_token:
        print("Found no GITHUB_TOKEN.")
    if style_errors:
        print("Found {} errors.".format(len(style_errors)))

    if github_token:
        session = requests.Session()
        session.headers['Authorization'] = 'token %s' % github_token
        reviews = session.get('https://api.github.com/repos/{}/pulls/{}/reviews'.format(github_repository, pr_id))
        reviews.raise_for_status()
        for review in reviews.json():
            if review['user']['login'] == 'github-actions[bot]' and review['body'].startswith(introtext):
                endpoint = 'https://api.github.com/repos/{}/pulls/{}/reviews/{}'.format(github_repository, pr_id, review['id'])
                data = '{"body": "'+ voidtext + '" }'
                resp = session.put(endpoint, data = data)
        if len(style_errors) > 0:
            endpoint = 'https://api.github.com/repos/{}/pulls/{}/reviews'.format(github_repository, pr_id)
            body = introtext + style_error_format(style_errors)
            data = '{"body": "' + body + '", "event": "REQUEST_CHANGES"}'
            data = '{"body": "foo", "event": "REQUEST_CHANGES" }'
            resp = session.post(endpoint, data = data)
            print(resp.json())

        #g = Github(github_token)
        #repo = g.get_repo(github_repository)
        #pr = repo.get_pull(pr_id)
        #reviews = pr.get_reviews()
        #for review in reviews:
        #    if review.user.login == 'github-actions[bot]' and review.body.startswith(introtext):
        #        endpoint = 'https://api.github.com/repos/{}/pulls/{}/reviews/{}'.format(github_repository, pr_id, review.id)
        #        print(endpoint)
        #        data = '{"body": "'+ voidtext + '" }'
        #        print(data)
        #        resp = requests.put(endpoint, data = data, headers = {'Authorization': 'token %s' % github_token})
        #        print(resp.content)
        #if len(style_errors) > 0:
        #    body = introtext + style_error_format(style_errors)
        #    pr.create_review(body=body, event='REQUEST_CHANGES')

if __name__ == "__main__":
    main()
