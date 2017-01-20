#!/usr/bin/awk -f

function rand_ip(n) {
    # Return IP from TEST-NET-2 (RFC 5737) address block
    rand_int = int(n * rand())
    return sprintf("198.51.100.%d", rand_int)
}

BEGIN {
    FS=","
    OFS=FS
    srand()
    ipv4 = rand_ip(254)
    ipv6 = "2001:0db8:abcd:0012:0000:0000:0000:0000"
    mac  = "[00:00:00:00:00:00]"
    md5  = "1C:96:78:29:AA:E2:2E:11:AC:61:E5:AA:56:E1:91:BE"
    sha1 = "14:09:8C:6E:64:5F:50:C9:E9:A3:62:5E:02:BB:33:67:E1:05:D3:D2"
    sha256 = "57:7A:FC:7C:A1:0F:79:11:67:E0:31:AC:66:F5:84:22:28:4E:AC:9D:27:A6:3E:93:84:D9:65:8C:FC:21:BF:A1"
    sha512 = "E9:AE:EE:6C:D1:D1:9C:08:A5:8E:00:07:40:39:60:A0:CF:6D:A0:14:F0:A4:4C:47:28:9D:43:2E:A5:F6:45:66:3A:6F:5A:A4:CC:20:9A:FC:93:88:9B:BD:0B:EF:79:AF:EA:17:0A:08:6A:8A:98:9C:16:EC:94:1E:E7:C4:C7:87"
    printf("#                                  ATTENTION\n" \
           "# ==============================================================================\n" \
           "# While some sensitive information has been removed from this file, you will\n" \
           "# have to take additional measures to make it suitable for distribution.\n" \
           "# Please, manually review and edit the data below!\n\n" \
           )
}
NR == 1 { print; next; } # print header
{
    for (i = 1; i <= NF; i++) {
        # Remove quotes from CSV fields if they exist; remember in is_quoted to
        # add them back as a last step:
        is_quoted = 0
        if ($i ~ /^\".*\"$/) {
            is_quoted = 1
            $i = substr($i, 2, length($i) - 2) # text within the two quotes
        }
        # IPv4
        # IPv4s may appear multiple times per field, e.g., in Shadowserver's
        # Open mDNS Servers Report, column workstation_ipv4; therefore, use
        # global substitution:
        if ($i ~ /[0-9]{1,3}(\.[0-9]{1,3}){3}/) {
            ipv4 = rand_ip(254)
            gsub(/[0-9]{1,3}(\.[0-9]{1,3}){3}/, ipv4, $i)
        }
        # IPv6
        if ($i ~ /^([a-f0-9]{1,4}:){7}[a-f0-9]{1,4}$/) $i = ipv6
        # Hostname
        if ($i ~ /[0-9a-zA-Z\-]+\.[a-z]{2,}$/) {
            hostname_ip = gensub(/\./, "-", "g", ipv4)
            $i = sprintf("%s.example.net", hostname_ip)
        }
        # local Hostnames
        if ($i ~ /[a-zA-Z0-9\-_]+\.local/) {
            gsub(/[a-zA-Z0-9\-_]+\.local/, "examplehostname.local", $i)
        }
        # URLs, e.g., index.php
        if ($i ~ /^\/.+/) $i = "/example-index.php"
        # DOS
        if ($i ~ /^\\\\.+/) $i = "\\\\EXAMPLEURL"
        # MAC
        if ($i ~ /\[([0-9a-f]{2}:){5}[0-9a-f]{2}\]/) $i = mac
        # Hashes (cert fingerprints)
        # MD5
        if ($i ~ /^[0-9A-F]{2}(:[0-9A-F]{2}){15}$/) $i = md5
        # SHA1
        if ($i ~ /^[0-9A-F]{2}(:[0-9A-F]{2}){19}$/) $i = sha1
        # SHA256
        if ($i ~ /^[0-9A-F]{2}(:[0-9A-F]{2}){31}$/) $i = sha256
        # SHA512
        if ($i ~ /^[0-9A-F]{2}(:[0-9A-F]{2}){63}$/) $i = sha512
        # END: Re-add quotes
        if (is_quoted) $i = sprintf("\"%s\"", $i)
    }
    print
}
