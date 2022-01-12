if comment == 'match1' && extra.list :setequals ['a', 'c', 'b', 'a'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :setequals ['a', 'b', 'c', 'd'] {
	update comment = 'unreachable'
}
