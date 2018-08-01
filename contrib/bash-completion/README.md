# Bash Completion for intelmq

It completes (sub-)commands and parameters (bots and pipeline names, log levels).

Bash completion for `intelmqctl` and `intelmqdump` can be set up with the following procedure:

## Dependencies

### Ubuntu / Debian

    apt-get install bash-completion jq

### CentOS

    yum install bash-completion jq

### SUSE

    zypper install bash-completion jq

### Fedora

    dnf install bash-completion jq

## Installation

1. Copy ./contrib/bash-completion/intelmq* to '/etc/bash_completion.d/'
2. Load the files directly or open a new shell (the files are loaded automatically).
