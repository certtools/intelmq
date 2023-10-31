<!-- comment
   SPDX-FileCopyrightText: 2015-2023 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Development Guidelines

## Coding-Rules

Most important: **KEEP IT SIMPLE**! This can not be over-estimated. Feature creep can destroy any good software
project. But if new folks can not understand what you wrote in 10-15 minutes, it is not good. It's not about the
performance, etc. It's about readability.

In general, we follow [PEP8](https://pep8.org/). We recommend reading it before committing code.

There are some exceptions: sometimes it does not make sense to check for every PEP8 error (such as whitespace
indentation when you want to make a dict=() assignment look pretty. Therefore, we do have some exceptions defined in the `setup.cfg` file.

We support Python 3 only.

#### Unicode

- Each internal object in IntelMQ (Event, Report, etc) that has strings, their strings MUST be in UTF-8 Unicode format.
- Any data received from external sources MUST be transformed into UTF-8 Unicode format before add it to IntelMQ
  objects.

#### Back-end independence and Compatibility

Any component of the IntelMQ MUST be independent of the message queue technology (Redis, RabbitMQ, etc...).

#### License Header

Please add a license and copyright header to your bots. There is a Github action that tests
for [reuse compliance](https://reuse.software/) of your code files.

## IntelMQ Data Format Rules

Any component of IntelMQ MUST respect the [IntelMQ Data Format](data-format.md).

## Code Submission Rules

#### Releases, Repositories and Branches

- The main repository is in [github.com/certtools/intelmq](https://github.com/certtools/intelmq).
- We use [semantic versioning](http://semver.org/).
- If you contribute something, please fork the repository, create a separate branch and use this for pull requests, see section below.
- There are a couple of forks which might be regularly merged into the main repository. They are independent and can have incompatible changes and can deviate from the upstream repository.

#### Branching model

- "master" is the stable branch. It hold the latest stable release. Non-developers should only work on this branch. The recommended log level is WARNING. Code is only added by merges from the maintenance branches.
- "maintenance/a.b.x" branches accumulate (cherry-picked) patches for a maintenance release (a.b.x). Recommended for
  experienced users which deploy intelmq themselves. No new features will be added to these branches.
- "develop" is the development branch for the next stable release
  (a.x). New features must go there. Developers may want to work on this branch. This branch also holds all patches from
  maintenance releases if applicable. The recommended log level is DEBUG.
- Separate branches to develop features or bug fixes may be used by any contributor.

#### How to Contribute

- Make separate pull requests / branches on GitHub for changes. This allows us to discuss things via GitHub.
- We prefer one Pull Request per feature or change. If you have a bunch of small fixes, please don't create one PR per fix :)
- Only very small and changes (docs, ...) might be committed directly to development branches without Pull Request by the [core-team](https://github.com/orgs/certtools/teams/core).
- Keep the balance between atomic commits and keeping the amount of commits per PR small. You can use interactive
  rebasing to squash multiple small commits into one (`rebase -i [base-branch]`). Only do rebasing if the code you are rebasing is yet not used by others or is already merged - because then others may need to run into conflicts.
- Make sure your PR is merge able in the develop branch and all tests are successful.
- If possible [sign your commits with GPG](https://help.github.com/articles/signing-commits-using-gpg/).

#### Workflow

We assume here, that origin is your own fork. We first add the upstream repository:

```bash
 git remote add upstream https://github.com/certtools/intelmq.git
```

Syncing develop:

```bash
 git checkout develop
 git pull upstream develop
 git push origin develop
```

You can do the same with the branches `master` and `maintenance`.

Create a separate feature-branch to work on, sync develop with upstream. Create working branch from develop:

```bash
 git checkout develop
 git checkout -b bugfix
# your work
 git commit
```

Or, for bugfixes create a separate bugfix-branch to work on, sync maintenance with upstream. Create working branch from
maintenance:

```bash
git checkout maintenance
git checkout -b new-feature
# your work
git commit
```

Getting upstream's changes for master or any other branch:

```bash
git checkout develop
git pull upstream develop
git push origin develop
```

There are 2 possibilities to get upstream's commits into your branch. Rebasing and Merging. Using rebasing, your history
is rewritten, putting your changes on top of all other commits. You can use this if your changes are not published yet (or only in your fork).

```bash
git checkout bugfix
git rebase develop
```

Using the `-i` flag for rebase enables interactive rebasing. You can then remove, reorder and squash commits, rewrite commit messages, beginning with the given branch, e.g. develop.

Or using merging. This doesn't break the history. It's considered more , but also pollutes the history with merge
commits.

```bash
git checkout bugfix
git merge develop
```

You can then create a PR with your branch `bugfix` to our upstream repository, using GitHub's web interface.

#### Commit Messages

If it fixes an existing issue, please use GitHub syntax, e.g.: `fixes certtools/intelmq#<IssueID>`

#### Prepare for Discussion in GitHub

If we don't discuss it, it's probably not tested.

## License and Author files

License and Authors files can be found at the root of repository.

- License file **MUST NOT** be modified except by the explicit written permission by CNCS/CERT.PT or CERT.at
- Credit to the authors file must be always retained. When a new contributor (person and/or organization) improves in
  some way the repository content (code or documentation), he or she might add his name to the list of contributors.

License and authors must be only listed in an external file but not inside the code files.