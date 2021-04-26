if comment == 'match1' {
	append! extra.list 'c'
}

if comment == 'match2' {
	append! extra.single 'more'
}

if comment == 'match3' {
	append! extra.nonexistent 'something'
}
