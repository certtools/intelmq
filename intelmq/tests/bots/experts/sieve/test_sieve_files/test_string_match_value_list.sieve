if classification.type :in ['infected-system'] {
	add comment = 'infected hosts'
}

if classification.type :in ['c2-server','malware-configuration'] {
	add comment = 'malicious server / service'
}

if source.fqdn :containsany ['.mx', '.zz'] {
	add comment = 'containsany match'
}

if extra.tag :regexin ['ee$', 'ab.d'] {
	add comment = 'regexin match'
}
