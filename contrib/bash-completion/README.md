# Bash Completion for intelmq

It completes (sub-)commands and parameters (bots and pipeline names, log levels).

Bash completion for `intelmqctl` and `intelmqdump` can be set up with the following procedure:

## Dependencies

### Ubuntu 14.04 / Debian 8

    apt-get install bash-completion jq

### CentOS 7

    yum install bash-completion jq

### SUSE

    zypper install bash-completion jq

## Installation

1. Copy intelmq.sh to '/etc/bash_completion.d/'
2. Logout and login to be able to use the bash completion.
