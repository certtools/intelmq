if comment == 'match1' && extra.list :supersetof ['a', 'b'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :supersetof ['a', 'b', 'c', 'd'] {
	update comment = 'unreachable'
}
