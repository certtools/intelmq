if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <github_account>"
    exit
fi

pip uninstall intelmq
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
