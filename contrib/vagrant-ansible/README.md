# Virtual Machine provisioning using ansible playbooks

Setting up IntelMQ plus the whole elasticsearch stack with a single 'vagrant up'

## Dependencies
- vagrant
- virtualbox 
- ansible

## How-to install

1. ```vagrant up```

## How-to use
The folder /opt/intelmq gets mounted directly under ./intelmq, where you find all of the intelmq configuration files, logs and so on...

The intelmq dashboard can be accessed under http://192.168.33.10:8080.

You can access the kibana dashboard by visiting
http://192.168.33.10:80 in your browser.

Use ``vagrant ssh``` to get direct access to the system.

## Known issues
Make sure that you are using up-to-date software, although I had some problems with ansible 1.9.1, because of:
https://github.com/ansible/ansible-modules-core/issues/1170

