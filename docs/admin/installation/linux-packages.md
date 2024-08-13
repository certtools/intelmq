<!-- comment
   SPDX-FileCopyrightText: 2015-2024 Sebastian Wagner, Filip Pokorný
   SPDX-License-Identifier: AGPL-3.0-or-later
-->


# Installation as Linux package

This guide provides instructions on how to install IntelMQ and it's components from Linux distribution's package repository.

!!! note
    Some bots may have additional dependencies which are mentioned in their own documentation.

## Supported OS

Native packages are currently provided for the following Linux distributions:

- **Debian 11** (bullseye)
- **Debian 12** (bookworm)
- **openSUSE Tumbleweed**
- **openSUSE Leap 15.5**
- **Ubuntu 20.04** (focal fossa)
- **Ubuntu 22.04** (jammy jellyfish)

### Debian 11 and 12

Add the repository to the package manager and install IntelMQ (packages `intelmq-api` and `intelmq-manager` are optional):

```bash
echo "deb http://download.opensuse.org/repositories/home:/sebix:/intelmq/Debian_$(lsb_release -rs)/ /" | sudo tee /etc/apt/sources.list.d/intelmq.list
curl -fsSL "https://download.opensuse.org/repositories/home:sebix:intelmq/Debian_$(lsb_release -rs)/Release.key" | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/intelmq.gpg > /dev/null
sudo apt update
sudo apt install intelmq intelmq-api intelmq-manager
```

### openSUSE Tumbleweed

Add the repository to the package manager and install IntelMQ (packages `intelmq-api` and `intelmq-manager` are optional):

```bash
zypper addrepo https://download.opensuse.org/repositories/home:sebix:intelmq/openSUSE_Tumbleweed/home:sebix:intelmq.repo
zypper refresh
zypper install intelmq intelmq-api intelmq-manager
```

### Ubuntu 20.04 and 22.04

For Ubuntu you must enable the Universe repository which provides community-maintained free and open-source software.

Add the repository to the package manager and install IntelMQ (packages `intelmq-api` and `intelmq-manager` are optional):

1. Open the file `/etc/apt/sources.list` in an editor of your choice. Use `sudo` or the `root` user.

2. Append `universe` to this line:
```
deb http://[...].archive.ubuntu.com/ubuntu/ focal main universe
```

3. Update the list of available packages and install IntelMQ:
```bash
sudo apt update
sudo apt install intelmq intelmq-api intelmq-manager
```
