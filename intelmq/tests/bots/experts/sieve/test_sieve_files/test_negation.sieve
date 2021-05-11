if comment == 'match1' && ! extra.text == 'test' {
	update comment = 'changed1'
}

if comment == 'match2' && ! ( extra.text == 'test' ) {
	update comment = 'changed2'
}

if comment == 'match3' && ( ! extra.text != 'test1' || ! extra.text != 'test2' ) {
	update comment = 'changed3'
}

if comment == 'match4' &&  ( ! extra.text == 'test1' && ! extra.text == 'test2' ) {
	update comment = 'changed4'
}
