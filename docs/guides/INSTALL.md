# Installation
**Table of Contents:**

- [Requirements](#requirements)
- [Install Dependencies](#install-dependencies)
  - [Ubuntu / Debian](#ubuntu--debian)
  - [CentOS 7 / RHEL 7](#centos-7--rhel-7)
  - [openSUSE Leap 15.1](#opensuse-leap-151)
- [Installation](#installation)
  - [Native Packages](#native-packages)
  - [PyPi](#pypi)
- [Additional Information](#additional-information)
- [Afterwards](#afterwards)


Please report any errors you encounter at https://github.com/certtools/intelmq/issues

For upgrade instructions, see [UPGRADING.md](UPGRADING.md).
For setting up a development environment see the [Developer's Guide](Developers-Guide.md#development-environment) section *Development Environment*.
For testing pre-releases see also the [Developer's Guide](Developers-Guide.md#testing-pre-releases) section *Testing Pre-releases*.

## Requirements

The following instructions assume the following requirements. Python versions >= 3.5 are supported.

Supported and recommended operating systems are:
* CentOS 7
* Debian 9 and 10
* OpenSUSE Leap 15.1
* Ubuntu: 16.04, 18.04, 19.10, 20.04

Other distributions which are (most probably) supported include CentOS 8, RHEL, Fedora and openSUSE Tumbleweed.

## Install Dependencies

If you are using native packages, you can simply skip this section as all dependencies are installed automatically.

### Ubuntu / Debian

```bash
apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil
apt install redis-server
```

Optional dependencies:
```bash
apt install bash-completion jq
apt install python3-sleekxmpp python3-pymongo python3-psycopg2
```

### CentOS 7 / RHEL 7

```bash
yum install epel-release
yum install python36 python36-devel python36-requests
yum install gcc gcc-c++
yum install redis
```

### openSUSE 15.1

```bash
zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle
zypper install redis
```

Optional dependencies:
```bash
zypper in bash-completion jq
zypper in python3-psycopg2 python3-pymongo python3-sleekxmpp
```

## Installation

Installation methods available:

* native packages (`.deb`, `.rpm`)
* PyPi (latest releases as python package)

**Note:** installation for development purposes must follow the instructions available on [Developers Guide](https://github.com/certtools/intelmq/blob/develop/docs/Developers-Guide.md#development-environment).

### Native Packages

Supported Operating Systems:

* **CentOS 7** (requires `epel-release`)
* **Debian 8** (requires `python3-typing`)
* **Debian 9**
* **Debian 10**
* **Fedora 29**
* **Fedora 30**
* **RHEL 7**  (requires `epel-release`)
* **openSUSE Leap 15.0**
* **openSUSE Leap 15.1**
* **openSUSE Tumbleweed**
* **Ubuntu 16.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ xenial main`)
* **Ubuntu 18.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ bionic main`)
* **Ubuntu 19.10** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ eoan main`)
* **Ubuntu 20.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ focal main`)

Get the installation instructions for your operating system here: [Installation Native Packages](https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq&package=intelmq).
To import the key on Debian and Ubuntu, use:
```bash
curl https://build.opensuse.org/projects/home:sebix:intelmq/public_key | sudo apt-key add -
```

Please report any errors or improvements at [IntelMQ Issues](https://github.com/certtools/intelmq/issues). Thanks!

### PyPi

```bash
sudo -i

pip3 install intelmq

useradd -d /opt/intelmq -U -s /bin/bash intelmq
sudo intelmqsetup
```
`intelmqsetup` will create all necessary directories, provides a default configuration for new setups. See [the user-guide section on paths](User-Guide.md#opt-and-lsb-paths) for more information on them and how to influence them.

### Additional Information

Following any one of the installation methods mentioned before, will setup the IntelMQ base. However, some bots may have additional dependencies which are mentioned in their own documentation available on in the [Bots documentation](https://github.com/certtools/intelmq/tree/develop/docs/Bots.md).


## Afterwards

Now continue with the [User Guide](User-Guide.md).
