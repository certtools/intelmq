# Release procedure

**Table of Contents:**
- [Documentation](#documentation)
- [Commit, push, review and merge](#commit-push-review-and-merge)
- [Tag and release](#tag-and-release)
- [Tarballs and PyPI](#tarballs-and-pypi)
- [Packages](#packages)
- [Announcements](#announcements)
- [Prepare new version](#prepare-new-version)

Make sure the current state is really final ;)
You can test most of the steps described here locally before doing it real.

Assumption: You are working on branch maintenance, the next version is a bug fix release. For feature releaese it is slightly different.

## Documentation

 * CHANGELOG.MD and
 * NEWS.MD: Update the latest header, fix the order, remove empty sections and (re)group the entries if necessary.
 * `intelmq/version.py`: Update the version.
 * `debian/changelog`: Insert a new section for the new version with the tool `dch`.

Eventually adapt the default log levels if necessary. Should be INFO for stable releases. See older releases.

## Commit, push, review and merge
Commit your changes in a separate branch, the final commit's message should start with `REL: `. Push and create a pull request to maintenance and after that from maintenance to master. Someone else should review the changes. Eventually fix them, make sure the `REL: ` is the last commit, you can also push that one at last, after the reviews.

Why a separate branch? Because if problems show up, you can still force-push to that one, keeping the release commit the latest one.

## Tag and release

Tag the commit with `git tag -s version HEAD`, merge it into master, push the branches *and* the tag. The tag is just `a.b.c`, not prefixed with `v` (that was necessary only with SVN a long time ago...).

Go to https://github.com/certtools/intelmq/tags and enter the release notes (changelog) for the new tag, then it's considered a release by github.

## Tarballs and PyPI

 * Build the source and binary (wheel) distribution: `python3 setup.py sdist bdist_wheel`
 * Upload the files including signatures to PyPI with e.g. twine: `twine upload -s dist/intelmq...`

## Packages
We are currently using the public Open Build Service instance of openSUSE: http://build.opensuse.org/project/show/home:sebix:intelmq

First, test all the steps first with the [unstable-repository](http://build.opensuse.org/project/show/home:sebix:intelmq:unstable) and check that at least installations succeed.

 * Create the tarballs with the script `create-archives.sh`.
 * Update the dsc and spec files for new filenames and versions.
 * Update the .changes file
 * Build locally for all distributions.
 * Commit.

## Announcements

Announce the new version at the mailinglists intelmq-users, intelmq-dev.
For bigger releases, probably also at IHAP, Twitter, etc. Ask your favorite social media consultant.

## Prepare new version

Increase the version in `intelmq/version.py` and declare it as alpha version.

Add a new empty changelog and news section. For the changelog:

```
### Core

### Development

### Harmonization

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
And for the news:

```
### Requirements

### Tools

### Harmonization

### Configuration

### Libraries

### Postgres databases
```
