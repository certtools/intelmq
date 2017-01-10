#!/usr/bin/env bash

#Declare Variables
#IntelMQ
INTELMQ_REPO="https://github.com/certtools/intelmq.git"
#BRANCH="master"
INTELMQ_BRANCH="v1.0-final"
#IntelMQ-Manager
INTELMQ_MANAGER_REPO="https://github.com/certtools/intelmq-manager.git"

function intelmq_install {
	#Install Dependencies
	apt-get update
	apt-get -y install python-pip git build-essential python-dev redis-server
    #Dependencies for pyhton REQUIREMENTS
    apt-get -y install libcurl4-gnutls-dev

	#Install IntelMQ
	git clone -b $INTELMQ_BRANCH $INTELMQ_REPO intelmq
	cd intelmq/
	# If branch v1.0-beta install deps using REQUIREMENTS file
	if [[ $INTELMQ_BRANCH == "v1.0-final" ]]
	then
	    pip install -r REQUIREMENTS;
	fi
	#Install
	python setup.py install
	useradd -d /opt/intelmq -U -s /bin/bash intelmq
	chmod -R 0770 /opt/intelmq
	chown -R intelmq.intelmq /opt/intelmq
    #Change owner of git clone files
    chown -R vagrant.vagrant /home/vagrant/intelmq
}

function intelmq_manager_install {
	#Install Dependencies
	apt-get -y install git apache2 php5 libapache2-mod-php5
	#Install Manager
	git clone $INTELMQ_MANAGER_REPO /tmp/intelmq-manager
	cp -R /tmp/intelmq-manager/intelmq-manager/* /var/www/
	chown -R www-data.www-data /var/www/
	#Configure
	usermod -a -G intelmq www-data
	echo "www-data ALL=(intelmq) NOPASSWD: /opt/intelmq/bin/intelmqctl" >> /etc/sudoers
	sed -i -e 's#DocumentRoot /var/www/html#DocumentRoot /var/www#' /etc/apache2/sites-available/000-default.conf
	/etc/init.d/apache2 restart

}
intelmq_install
intelmq_manager_install
