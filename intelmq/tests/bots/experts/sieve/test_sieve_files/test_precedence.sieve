if source.abuse_contact == 'abuse@example.com' && source.ip == '1.2.3.4' || feed.provider == 'acme' {
    add comment = 'match1'
}

if source.abuse_contact == 'abuse@example.com' && (source.ip == '5.6.7.8' || feed.provider == 'acme') {
    add comment = 'match2'
}
