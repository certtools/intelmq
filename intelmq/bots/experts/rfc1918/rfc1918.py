from intelmq.lib.bot import Bot, sys
from intelmq.lib.message import Event
from intelmq.bots import utils

# Source link : http://en.wikipedia.org/wiki/IPv4
#               http://www.ietf.org/rfc/rfc3849.txt
#               http://www.ietf.org/rfc/rfc4291.txt

ipranges = ("0.0.0.0/8", "10.0.0.0/8", "100.64.0.0/10", "127.0.0.0/8",
    "169.254.0.0/16", "172.16.0.0/12", "192.0.0.0/24", "192.0.2.0/24",
    "192.88.99.0/24", "192.168.0.0/16", "198.18.0.0/15", "198.51.100.0/24",
    "203.0.113.0/24", "224.0.0.0/4", "240.0.0.0/4", "255.255.255.255/32",
    "fe80::/64", "2001:0db8::/32")


class RFC1918Bot(Bot):
#
# RFC 1918 Will Drop Local IP from a given record and a bit more.
#   It Check for RFC1918 IPv4 Host
#   It Check for Localhosts, multicast, test lans
#   It Check for Link Local and Documentation Lan in IPv6
#
# Need only to feed the parameter "fields" to set the name of the field
# parameter designed to be filtered out.
#
# Several parameters could be used, separated by ","
#
# It could sanitize the whole records with the "drop" parameter set to "yes"
#

    def process(self):
        report = self.receive_message()

        banned = []

        # Read the config to see if we should drop or clean
        if self.parameters.drop.upper() == "YES":
            drop = True
            dtext = "drop"
        else:
            drop = False
            dtext = "apply cleanup"

        fields = self.parameters.fields
        self.logger.debug("Will %s on parameter %s" % (dtext, fields))

        if report:
            for field in self.parameters.fields.split(","):
                field = field.strip()  # If not cleanly inputed in parameter
                value = report.value(field)
                if value:
                    found = False
                    for iprange in ipranges:  # for All ranges do the test
                        if utils.is_in_net(value, iprange):
                            self.logger.debug("Found %s in %s in record %s"
                              % (value, iprange, field))
                            found = True
                            if not drop:  # if drop is not required we will
                              # drop only the field
                                self.logger.debug("Value removed from %s"
                                  % (field))
                                report.discard(field, value)
                            break  # We found it exit loop
                else:
                    self.logger.warning("Field %s is non existant" % (field))
            if found:  # If the IP was found
                if not drop:  # and if we don't want the record at all
                    self.send_message(report)  # If we have sanitized, save msg
            else:  # If the IP has not been found
                self.send_message(report)
        self.acknowledge_message()

if __name__ == "__main__":
    bot = RFC1918Bot(sys.argv[1])
    bot.start()
