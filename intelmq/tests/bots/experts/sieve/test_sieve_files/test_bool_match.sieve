if comment == 'match1' && extra.truthy == true {
	update comment = 'changed1'
}

if comment == 'match2' && extra.falsy == false {
	update comment = 'changed2'
}

if comment == 'match3' && extra.truthy != false {
	update comment = 'changed3'
}

if comment == 'match4' && extra.falsy != true {
	update comment = 'changed4'
}

if comment == 'match5' && extra.truthy == false {
	update comment = 'unreachable'
}

if comment == 'match6' && extra.falsy == true {
	update comment = 'unreachable'
}

if comment == 'match7' && extra.truthy != true {
	update comment = 'unreachable'
}

if comment == 'match8' && extra.falsy != false {
	update comment = 'unreachable'
}
