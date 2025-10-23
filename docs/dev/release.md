<!-- comment
   SPDX-FileCopyrightText: 2015-2021 nic.at GmbH, 2022-2025 Institute for Common Good Technology
   SPDX-License-Identifier: AGPL-3.0-or-later
-->

# Release procedure

## Make a pre-release

Consider whether a pre-release would be necessary or good. A pre-release requires less effort than a stable release. It only needs:
- Proper version numbers in `setup.py`, e.g. `1.2.3-alpha1` or `1.2.3-rc1`
- Optional: A git tag and GitHub release (mark it as pre-release)
- Push to PyPI
- Proper version numbers in `debian/changelog`, e.g. `1.2.3~alpha1-1` or `1.2.3~rc1-1`
	- The tilde `~` make sure it is considered older than the final `1.2.3-1`

### Testing Pre-releases

The installation procedures is slightly different for the pre-releases.

#### Installation with packages

For native packages, you can find the unstable packages of the next version here:
[Installation Unstable Native Packages](https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq%3Aunstable&package=intelmq).
The unstable repository only has a limited set of packages, so enable the stable repository in parallel.

#### Installation with pip

For the installation with pip, use the `--pre` parameter as shown here following command:

```bash
pip3 install --pre intelmq
```

#### Testing

All other steps are not different per installation variant.
Please report any issues you find in our [Issue Tracker](https://github.com/certtools/intelmq/issues/new).

## Check before

-   Make sure the current state is really final ;) You can test most of
    the steps described here locally before doing it real.
-   Check the upgrade functions in `intelmq/lib/upgrades.py`.
-   Close the milestone on GitHub and move any open issues to the next
    one.
-   `docs/admin/installation/linux-packages.md`: Update supported operating systems.

## Documentation

These apply to all projects:

- CHANGELOG.MD and NEWS.MD: Update the latest header, fix the order, remove empty sections and (re)group the entries if necessary.
- debian/changelog: Insert a new section for the new version with the tool `dch` or update the version of the existing last item if yet unreleased. Don't forget the revision after the version number!

### IntelMQ

- `intelmq/version.py`: Update the version.

### IntelMQ API

-   `intelmq_api/version.py`: Update the version.

### IntelMQ Manager

-   `intelmq_manager/version.py`: Update the version.
-   `intelmq_manager/static/js/about.js`: Update the version.

## Commit, push, review and merge

Commit your changes in a separate branch, the final commit message should start
with `REL:`. Push and create a pull request to the `develop` branch. Someone
else should review the changes. Eventually fix them, make sure the `REL:` is
the last commit, you can also push that one at last, after the reviews.

Why a separate branch? Because if problems show up, you can still
force-push to that one, keeping the release commit the latest one.

## Tag and release

Tag the commit with `git tag -s version HEAD`, merge it into `develop`,
push the branches *and* the tag. The tag is just `a.b.c`, not prefixed
with `v` (that was necessary only with SVN a long time ago...).

Go to <https://github.com/certtools/intelmq/tags> and enter the release
notes (from the CHANGELOG) for the new tag, then it's considered a
*release* by GitHub.

## Tarballs and PyPI

- Build the source and binary (wheel) distribution:

```bash
rm -r build/
python3 setup.py sdist bdist_wheel
```

* Upload the files including signatures to PyPI with e.g. twine: `twine upload -u __token__ -p $APITOKEN dist/intelmq...` (or set the API Token in `.pypirc`).

## Documentation

Since using mkdocs (see https://docs.intelmq.org) nothing needs to be done anymore.

## Packages

We are currently using the public Open Build Service instance of
openSUSE: <http://build.opensuse.org/project/show/home:sebix:intelmq>

First, test all the steps first with the [unstable-repository](http://build.opensuse.org/project/show/home:sebix:intelmq:unstable) and check that at least installations succeed.

-   Create the tarballs with the script `create-archives.sh`.
-   Update the dsc and spec files for new filenames and versions.
-   Update the .changes file
-   Build locally for all distributions.
-   Commit.

## Docker Image

Releasing a new Docker image is very easy.

-   Clone [IntelMQ Docker Repository](https://github.com/certat/intelmq-docker) with `git clone https://github.com/certat/intelmq-docker.git --recursive` as this repository contains submodules
-   If the `intelmq-docker` repository is not updated yet, use `git pull --recurse-submodules` to pull the latest changes from their respective repository.
-   Run `./build.sh`, check your console if the build was successful.
-   Run `./test.sh` - It will run all tests with the exotic flag. All
    errors/warnings will be displayed.
-   Change the `build_version` in `publish.sh` to the new version you
    want to release.
-   Change the `namespace` variable in `publish.sh`.
-   If no error/warning was shown, you can release with `./publish.sh`.
-   Update the [DockerHub ReadMe](https://hub.docker.com/repository/docker/certat/intelmq-full) and add the latest version.
-   Commit and push the updates to the `intelmq-docker` repository

## Announcements

Announce the new version at the mailinglists [intelmq-users](https://lists.cert.at/mailman3/hyperkitty/list/intelmq-users@lists.cert.at/), [intelmq-dev](https://lists.cert.at/mailman3/hyperkitty/list/intelmq-dev@lists.cert.at/) and on [ossbase.org](https://ossbase.org/).
For bigger releases, also at IHAP, X, etc.

## Prepare new version

Increase the version in `intelmq/version.py` and declare it as alpha version. Add the new version in
`intelmq/lib/upgrades.py`. Add a new entry in `debian/changelog` with `dch -v [version] -c debian/changelog`.

Add new entries to `CHANGELOG.md` and `NEWS.md`.

### IntelMQ

For `CHANGELOG.md`:

```markdown
### Configuration

### Core

### Development

### Data Format

### Bots
#### Collectors

#### Parsers

#### Experts

#### Outputs

### Documentation

### Packaging

### Tests

### Tools

### Contrib

### Known issues
```

And for `NEWS.md`:

```markdown
### Requirements

### Tools

### Data Format

### Configuration

### Libraries

### Postgres databases
```

### IntelMQ API

An empty section of `CHANGELOG.rst`.

### IntelMQ Manager

For `CHANGELOG.md`:

```markdown
### Pages

#### Landing page

#### Configuration

#### Management

#### Monitor

#### Check

### Documentation

### Third-party libraries

### Packaging

### Known issues
```

And an empty section in the `NEWS.md` file.
