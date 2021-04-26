if comment == 'match1' && extra.list :overlaps ['a', 'b', 'd'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :overlaps ['d', 'e', 'f'] {
	update comment = 'unreachable'
}

if comment == 'match3' && extra.list ! :overlaps ['d', 'e', 'f'] {
	update comment = 'changed3'
}

if comment == 'match4' && extra.list ! :overlaps ['a', 'b', 'd'] {
	update comment = 'unreachable'
}
