if comment == 'match1' && extra.list :equals ['a', 'b', 'c'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :equals ['d', 'e', 'f'] {
	update comment = 'unreachable'
}
