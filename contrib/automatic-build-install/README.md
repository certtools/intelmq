# Automatically build and install intemlq (development only)

Using these files, you can setup a watchdog on your intelmq files

`watch.sh` watches for changes in the directory it has been started in
(directory `intelmq` with all the code is useful here). It calls
`/usr/local/sbin/update-intelmq` with sudo to build and install intelmq with
both python2 and python3. Existing files in `/opt/intelmq` will be overwritten!

Add the following rule to your sudoers-file, so you do not need to authenticate
for sudo:

```bash
user ALL = NOPASSWD: /usr/local/sbin/update-intelmq
```
