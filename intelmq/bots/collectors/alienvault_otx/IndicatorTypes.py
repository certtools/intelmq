class IndicatorTypes(object):
    def __init__(self, name, description):
        self.name = name
        self.description = description


IPv4 = IndicatorTypes(name="IPv4",
                      description="An IPv4 address indicating the online location of a server or other computer.")
IPv6 = IndicatorTypes(name="IPv6",
                      description="An IPv6 address indicating the online location of a server or other computer.")
DOMAIN = IndicatorTypes(name="domain",
                        description="A domain name for a website or server. Domains encompass a series of hostnames.")
HOSTNAME = IndicatorTypes(name="hostname", description="The hostname for a server located within a domain.")
EMAIL = IndicatorTypes(name="email", description="An email associated with suspicious activity.")
URL = IndicatorTypes(name="URL",
                     description=" Uniform Resource Location (URL) summarizing"
                                 " the online location of a file or resource.")
URI = IndicatorTypes(name="URI",
                     description="Uniform Resource Indicator (URI) describing"
                                 " the explicit path to a file hosted online.")
FILE_HASH_MD5 = IndicatorTypes(name="FileHash-MD5",
                               description="A MD5-format hash that summarizes"
                                           " the architecture and content of a file.")
FILE_HASH_SHA1 = IndicatorTypes(name="FileHash-SHA1",
                                description="A SHA-format hash that summarizes"
                                            " the architecture and content of a file.")
FILE_HASH_SHA256 = IndicatorTypes(name="FileHash-SHA256",
                                  description="A SHA-256-format hash that summarizes"
                                              " the architecture and content of a file.")
FILE_HASH_PEHASH = IndicatorTypes(name="FileHash-PEHASH",
                                  description="A PEPHASH-format hash that summarizes the"
                                              " architecture and content of a file.")
FILE_HASH_IMPHASH = IndicatorTypes(name="FileHash-IMPHASH",
                                   description="An IMPHASH-format hash that summarizes"
                                               " the architecture and content of a file.")
CIDR = IndicatorTypes(name="CIDR",
                      description="Classless Inter-Domain Routing (CIDR) address, which"
                                  " describes both a server's IP address and the network"
                                  " architecture (routing path) surrounding that server.")
FILE_PATH = IndicatorTypes(name="FilePath", description="A unique location in a file system.")
MUTEX = IndicatorTypes(name="Mutex",
                       description="The name of a mutex resource describing the"
                                   " execution architecture of a file.")
CVE = IndicatorTypes(name="CVE",
                     description="Common Vulnerability and Exposure (CVE) entry"
                                 " describing a software vulnerability that can be"
                                 " exploited to engage in malicious activity.")
all_types = [IPv4,
             IPv6,
             DOMAIN,
             HOSTNAME,
             EMAIL,
             URL,
             URI,
             FILE_HASH_MD5,
             FILE_HASH_SHA1,
             FILE_HASH_SHA256,
             FILE_HASH_PEHASH,
             FILE_HASH_IMPHASH,
             CIDR,
             FILE_PATH,
             MUTEX,
             CVE]


def to_name_list(indicator_type_list):
    return [indicator_type.name for indicator_type in indicator_type_list]
