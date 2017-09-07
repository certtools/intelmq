if :exists source.ip {
    add comment = 'added'
    update source.ip = '127.0.0.2'
    remove classification.type
}
