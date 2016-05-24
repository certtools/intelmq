# Virtual Machine provision for test IntelMQ and IntelMQ-Manger
***

## Information
On this directory exists a Vagrantfile to create a ubuntu/trusty64 virtualbox Virtual Machine (VM) and using *bootstrap.sh* script will install IntelMQ (v1.0-beta branch) and IntelMQ-Manager.

The VM can be acessed from the host machine on the IP: 192.168.33.10 .

## Dependencies
This project requires that [VirtualBox][vb] and [Vagrant][vg] is installed on the host machine.

## How to use it
* If you have not yet cloned this repository:

git clone https://github.com/certtools/intelmq.git

* Then go to this script directory:

cd intelmq/scripts/vagrant

* The script is configured to clone the v1.0-beta branch. If you what other branch, you should change the variable *INTELMQ_BRANCH* on the *bootstrap.sh* script.  
* Fire up vagrant
vagrant up

* During this process the base image is downloaded and the provision script *bootsrap.sh* is runned to install IntelMQ and IntelMQ-Manager. 

* Access virtual machine via ssh:

vagrant ssh

* Test acess to the IntelMQ-Manager
    - Point the browser on the host machine to http://192.168.33.10

* To halt machine van use the command:

  vagrant halt

* To delete the machine:

  vagrant destroy

## Credits

[vb]: https://www.virtualbox.org/wiki/Downloads "VirtualBox"
[vg]: http://www.vagrantup.com/downloads.html  "Vagrant"

## Todos
