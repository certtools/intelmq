if classification.type == ['infected-system','malware','ransomware'] {

add comment='infected hosts'

}

if classification.type == ['c2-server','malware-configuration'] {

add comment='malicious server / service'

}
