# Installation

  * [Requirements](#requirements)
  * [Install](#install)
    * [Install Dependencies](#install-dependencies)
        * [Ubuntu 14.04 / Debian 8](#ubuntu-1404--debian-8)
        * [CentOS 7](#centos-7)
    * [Installation](#install)


Please report any errors you encounter at https://github.com/certtools/intelmq/issues

For upgrade instructions, see [UPGRADING.md](UPGRADING.md).

## Requirements

The following instructions assume the following requirements:

* **Operating System:** Ubuntu 14.04 and 16.04 LTS, Debian 8, CentOS 7 or OpenSUSE Leap 42.x

## Install

### Install Dependencies

If you are using native packages, you can simply skip this section as all dependencies are installed automatically.

##### Ubuntu 14.04 / Debian 8

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

##### CentOS 7

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

Enable redis on startup:
```bash
systemctl enable redis
systemctl start redis
```

### Installation

There are different methods to install IntelMQ:

* as native deb/rpm package
* from PyPi: to get the latest releases as python package
* from the (local) repository: for developers to get the latest (unstable!) version and/or have local modifications

#### Native packages

Get the install instructions for your operating system here:
https://software.opensuse.org/download.html?project=home%3Asebix%3Aintelmq&package=intelmq

Currently, these operating systems are supported by the packages:
* CentOS 7, install `epel-release` first
* Debian 8
* Fedora 25
* openSUSE Leap 42.2
* openSUSE Tumbleweed
* Ubuntu 16.04

Please report any errors or improvements, thanks!

#### From PyPi

```bash
sudo -s

pip3 install intelmq

useradd -d /opt/intelmq -U -s /bin/bash intelmq
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

Please note that the PyPi / pip3 installation method does not create /opt/intelmq, as described in [Issue #189](/certtools/intelmq/issues/819).
As workaround you need to move /opt/intelmq from the site-packages directory to / manually.
The location of this directory varies, it could be `/usr/lib/python3.4/site-packages`, `/usr/local/lib/python3.5/dist-packages/` or similar.
For example:
```bash
mv /usr/lib/python3.4/site-packages/opt/ /
```

#### From the repository

The `REQUIREMENTS` files define a list of python packages and versions, which are necessary to run most components of IntelMQ. The defined (minimal) versions are recommendations. Some bots have additional dependencies which are mentioned in their documentation and their own `REQUIREMENTS` file (in their source directory).

If your Python version is lower than 3.5 you additionally need the "typing" package:
```bash
pip3 install typing
```

Clone the repository if not already done:
```bash
git clone https://github.com/certtools/intelmq.git /tmp/intelmq
cd /tmp/intelmq
```

If you have a local repository and you have or will do local modification, consider using an editable installation (`pip install -e .`).
```
sudo -s

pip3 install -r REQUIREMENTS
pip3 install .

useradd -d /opt/intelmq -U -s /bin/bash intelmq
chmod -R 0770 /opt/intelmq
chown -R intelmq.intelmq /opt/intelmq
```

## Afterwards

Now continue with the [User Guide](User-Guide.md).
