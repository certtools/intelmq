if comment == 'match1' && extra.list :subsetof ['a', 'b', 'c', 'd'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :subsetof ['b', 'c', 'd', 'e'] {
	update comment = 'unreachable'
}
