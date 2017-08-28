if source.ip << ['192.0.0.0/24', '169.254.0.0/16'] {
    add comment = 'bogon'
}
