if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <github_account>"
    exit
fi

echo "Installing dependencies"
apt-get update
apt-get install python-pip git
apt-get install build-essential python-dev
apt-get install redis-server

echo "Installing IntelMQ"
useradd -M -U -s /bin/bash intelmq
pip install git+https://$1@github.com/certtools/intelmq.git

echo "Fixing folder permissions"
chmod -R 770 /etc/intelmq/
chmod -R 700 /var/run/intelmq
chmod -R 700 /var/lib/intelmq
chmod -R 700 /usr/local/bin/intelmqctl
chmod -R 700 /var/log/intelmq

chown -R intelmq.intelmq /etc/intelmq/
chown -R intelmq.intelmq /var/run/intelmq
chown -R intelmq.intelmq /var/lib/intelmq
chown -R intelmq.intelmq /usr/local/bin/intelmqctl
chown -R intelmq.intelmq /var/log/intelmq
