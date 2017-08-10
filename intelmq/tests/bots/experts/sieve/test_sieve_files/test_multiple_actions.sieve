if :exists source.ip {
    add comment = 'added'
    modify source.ip = '127.0.0.2'
    remove classification.type
}