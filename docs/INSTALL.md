**Table of Contents:**
- [Requirements](#requirements)
- [Install Dependencies](#install-dependencies)
  - [Ubuntu 14.04 / Debian 8](#ubuntu-1404-debian-8)
  - [Ubuntu 16.04 / Ubuntu 18.04 / Debian 9](#ubuntu-1604-ubuntu-1804-debian-9)
  - [CentOS 7 / RHEL 7](#centos-7-rhel-7)
  - [openSUSE Leap 42.3 / 15.0](#opensuse-leap-423-150)
- [Installation](#installation)
  - [Native Packages](#native-packages)
  - [PyPi](#pypi)
- [Additional Information](#additional-information)
- [Afterwards](#afterwards)


Please report any errors you encounter at https://github.com/certtools/intelmq/issues

For upgrade instructions, see [UPGRADING.md](UPGRADING.md).
For setting up a development environment see the [Developer's Guide](Developers-Guide.md#development-environment) section *Development Environment*.
For testing pre-releases see also the [Developer's Guide](Developers-Guide.md#testing-pre-releases) section *Testing Pre-releases*.

# Requirements

The following instructions assume the following requirements:

Supported and recommended operating systems are:
* CentOS 7
* Debian 8 and 9
* OpenSUSE Leap 42.3 and 15.0
* Ubuntu: 14.04, 16.04 and 18.04

Other distributions which are (most probably) supported include RHEL, Fedora and openSUSE Tumbleweed.

# Install Dependencies

If you are using native packages, you can simply skip this section as all dependencies are installed automatically.

## Ubuntu 14.04 / Debian 8

```bash
apt-get install python3 python3-pip
apt-get install git build-essential libffi-dev
apt-get install python3-dev
apt-get install redis-server
```

**Special note for Debian 8**:
if you are using Debian 8, you need to install this package extra: ``apt-get install libgnutls28-dev``.
In addition, Debian 8 has an old version of pip3. Please get a current one via:
```bash
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
python3.4 /tmp/get-pip.py
```

## Ubuntu 16.04 / Ubuntu 18.04 / Debian 9

```bash
apt install python3-pip python3-dnspython python3-psutil python3-redis python3-requests python3-termstyle python3-tz python3-dateutil
apt install git redis-server
```

Optional dependencies:
```bash
apt install bash-completion jq
apt install python3-sleekxmpp python3-pymongo python3-psycopg2
```

## CentOS 7 / RHEL 7

```bash
yum install epel-release
yum install python34 python34-devel
yum install git gcc gcc-c++
yum install redis
```

Install the last pip version:
```bash
curl "https://bootstrap.pypa.io/get-pip.py" -o "/tmp/get-pip.py"
python3.4 /tmp/get-pip.py
```

## openSUSE Leap 42.3 / 15.0

```bash
zypper install python3-dateutil python3-dnspython python3-psutil python3-pytz python3-redis python3-requests python3-python-termstyle
zypper install git redis
```

Optional dependencies:
```bash
zypper in bash-completion jq
zypper in python3-psycopg2 python3-pymongo python3-sleekxmpp
```

# Installation

Installation methods available:

* native packages (`.deb`, `.rpm`)
* PyPi (latest releases as python package)

**Note:** installation for development purposes must follow the instructions available on [Developers Guide](https://github.com/certtools/intelmq/blob/develop/docs/Developers-Guide.md#development-environment).

## Native Packages

Supported Operating Systems:

* **CentOS 7** (requires `epel-release`)
* **RHEL 7**  (requires `epel-release`)
* **Debian 8** (requires `python3-typing`)
* **Debian 9**
* **Fedora 27**
* **Fedora 28**
* **Fedora 29**
* **openSUSE Leap 42.3**
* **openSUSE Leap 15.0**
* **openSUSE Tumbleweed**
* **Ubuntu 16.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ xenial main`)
* **Ubuntu 18.04** (enable the universe repositories by appending ` universe` in `/etc/apt/sources.list` to `deb http://[...].archive.ubuntu.com/ubuntu/ bionic main`)

Get the installation instructions for your operating system here: [Installation Native Packages](https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq&package=intelmq).

Please report any errors or improvements at [IntelMQ Issues](https://github.com/certtools/intelmq/issues). Thanks!

## PyPi

```bash
sudo -s

pip3 install intelmq

mv `python3 -c "import site; print(site.getsitepackages()[0] + '/opt/intelmq')"` /opt/

useradd -d /opt/intelmq -U -s /bin/bash intelmq
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

**Note:** the reason why instructions have the `mv` command using python output is because pip3 installation method does not (and cannot) create `/opt/intelmq`, as described in [Issue #189](https://github.com/certtools/intelmq/issues/819).


## Additional Information

Following any one of the installation methods mentioned before setup the IntelMQ base. However, some bots have additional dependencies which are mentioned in their own documentation available on this [directory](https://github.com/certtools/intelmq/tree/develop/intelmq/bots).


# Afterwards

Now continue with the [User Guide](User-Guide.md).
