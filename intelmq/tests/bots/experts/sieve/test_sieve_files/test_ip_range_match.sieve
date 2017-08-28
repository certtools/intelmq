if source.ip << '192.0.0.0/24' {
    add! comment = 'bogon1'
    keep
}

if source.ip << '192.0.0.0/16' {
    add! comment = 'bogon2'
    keep
}

if source.ip << '2001:620:0:0:0:0:0:0/29' {
    add comment = 'SWITCH'
    keep
}

if comment << '10.0.0.0/8' {
    add comment = 'valid'
}
