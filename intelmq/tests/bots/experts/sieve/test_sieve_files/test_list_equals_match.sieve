if comment == 'match1' && extra.list :equals ['a', 'b', 'c'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :equals ['d', 'e', 'f'] {
	update comment = 'unreachable'
}

if comment == 'match3' && extra.list ! :equals ['d', 'e', 'f'] {
	update comment = 'changed3'
}

if comment == 'match4' && extra.list ! :equals ['a', 'b', 'c'] {
	update comment = 'unreachable'
}
