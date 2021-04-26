if comment == 'match1' && extra.list :setequals ['a', 'c', 'b', 'a'] {
	update comment = 'changed1'
}

if comment == 'match2' && extra.list :setequals ['a', 'b', 'c', 'd'] {
	update comment = 'unreachable'
}

if comment == 'match3' && extra.list ! :setequals ['a', 'b', 'c', 'd'] {
	update comment = 'changed3'
}

if comment == 'match4' && extra.list ! :setequals ['c', 'b', 'a'] {
	update comment = 'unreachable'
}
