#!/usr/bin/env bash
# SPDX-FileCopyrightText: 2020 Birger Schacht
# SPDX-License-Identifier: AGPL-3.0-or-later
#
apt-get update -qq
apt-get install ansible python python3-apt -y
ansible-playbook --connection=local -i /src/intelmq-vagrant/ansible/inventory.yml /src/intelmq/.github/workflows/scripts/ansible-playbook.yml
