if extra.list :equals [true, 2.1, 'three', 4] {
	update comment = 'changed'
}

if comment == 'match1' {
	add extra.value = 'string'
}
elif comment == 'match2' {
	add extra.value = 'dummy value'
	add! extra.value = 100
}
elif comment == 'match3' {
	add extra.value = 'dummy value'
	update extra.value = 1.5
}
elif comment == 'match4' {
	add extra.value = true
}
