# Please read the notes below and replace them with the description of you pull request

Make sure you follow the instructions in the [Developer Guide](https://intelmq.readthedocs.io/en/latest/dev/guide.html) - it describes how to run the test suite and which coding rules to follow.

# Commits

Please review your commits before creating a pull request. We try to keep our commit history clean.
If you had to fix something in your code and added another commit on top of your existing work, please [squash](https://blog.simontimms.com/2016/02/18/i-squash-my-pull-requests-and-you-should-too/) your commits.
This makes it a lot easier to find out why things work the way they do later on.

But please also keep in mind that one commit should only contain changes that belong together.
> The cardinal rule for creating good commits is to ensure there is only one "logical change" per commit
> - [OpenStack Wiki on GitCommitMessages](https://wiki.openstack.org/wiki/GitCommitMessages#Structural_split_of_changes)

Thus, if your changes affect multiple files and also contains tests and documentation (which it should), it might make sense to have the tests and the documentation in a separate commit.

# Commit Messages

Please explain your changes also in the git commit message.
The commit message should contain a subject that gives an overview of the changes in the commit and is limited to 72 characters.
It should start with a capital letter and it should not end with a period.
Below the subject should be, separated by an empty line, the body of the commit message. The body should explain what the commit changes and why it changes thing the way it does.
Explain your modification and also explain why you didn't chose a different approach.
See also [How To Write a Git Commit Message](https://chris.beams.io/posts/git-commit/).

# Description

If you are following the commit message guidelines above, all the relevant information should already be part of the commit message.
If there is anything else you want to add, feel free to do this here.

