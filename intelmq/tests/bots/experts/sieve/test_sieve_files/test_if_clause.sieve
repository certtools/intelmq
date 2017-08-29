if comment == 'changeme' {
    modify comment = 'changed'
}

if source.ip == '192.168.0.1' {
    modify source.ip = '192.168.0.2'
}
