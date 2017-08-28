if classification.type == ['botnet drone','malware','ransomware'] {

add comment='infected hosts'

}

if classification.type == ['c&c','malware configuration'] {

add comment='malicious server / service'

}
