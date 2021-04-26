if comment == 'match1' && extra.list :supersetof ['a', 'b'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :supersetof ['a', 'b', 'c', 'd'] {
	update comment = 'unreachable'
}

if comment == 'match3' && extra.list ! :supersetof ['a', 'b', 'c', 'd'] {
	update comment = 'changed3'
}

if comment == 'match4' && extra.list ! :supersetof ['a', 'b'] {
	update comment = 'unreachable'
}
