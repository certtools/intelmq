// '{"extra.some_dict": { "key": [] }}'

if :notexists extra.some_dict {
 drop
}
if extra.some_dict !~ '"key": ' {
 drop
}
if extra.some_dict =~ '"key": \[\]' {
 drop
}
