if comment == 'match1' {
	append extra.list 'c'
}

if comment == 'match2' {
	append extra.single 'unappendable'
}

if comment == 'match3' {
	append extra.nonexistent 'new'
}
