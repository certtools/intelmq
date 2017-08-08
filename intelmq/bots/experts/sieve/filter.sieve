
if allof ('source.ip' = '192.168.13.13', 'feed.name' :contains 'cymru') { reject;keep }

if source.ip == ['123.123.123.123', '234.234.234.234'] { reject }

if source.ip == '123.123.123.123' || source.ip == '234.234.234.234'

// string equality operator ==
// string inequality operator !=
// regex match =~
// regex not match !~

// or operator: ||
// and operator: &&

if source.ip ~= '['

if anumber == 3 { keep; drop; keep } // watch out for this

if :exists source.asn { .... }
if :!exists source.asn { ... }

if source.ip == '123.123.123.123' {
    add source.asn = 'AS559';               // add key/value only if key not present yet
    add! source.asn = 'AS559';              // force overwrite if exists
    modify source.asn = 'AS559';            // edit key/value only if key is present
    remove source.asn;
}



event = {
 source.ip = '123.123.123.123',
 source.asn = 'AS559'
}

event2 = {
 source.ip = '234.234.234.234'
}


if source.asn == 'AS559' { // do not match if key doesn't exist

}

// simulate ':exists' operator
if source.asn =~ /.*/ { ... } // should only match if key 'source.asn' exists

// simulate ':notexists' operator?
if source.asn !~ /.*/ { ... } // will not match because key does not exist



