# IntelMQ Ansible Playbooks

A collection of playbooks, which allows you to quickly deploy ansible on your local machine or any server you have ssh-access to.
Can also be used to provision virtual machines, with vagrant, see ../vagrant-ansible

## Usage

Following steps are recommend to adopt this to your needs:

* Fill your inventory (aka. hosts file)
* Set your variables (group_vars/all, ...)
* Customise site.yml, like adding or removing roles
* Run ```ansible-playbook playbook.yml```
* ???
* Profit!

## Configuration

It's recommended to change the default passwords for IntelMQ-Manager and Kibana, which can be edited directly in group_vars/all.
Optionally it's possible to clone the IntelMQ development branch. 


Please feel free to make pull requests, if there's anything you feel could be done better!


Credits to Chris Sidiropoulos the autor of the original intelmq-elk.
