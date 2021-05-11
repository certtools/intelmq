if comment == 'match1' {
	if extra.text == 'test1' {
		update comment = 'changed1'
	}
	elif extra.text == 'test2' {
		update comment = 'changed2'
	}
	else {
		update comment = 'changed3'
	}
}
elif comment == 'match2' {
	if extra.text == 'test4' {
		update comment = 'changed4'
	}
	elif extra.text == 'test5' {
		update comment = 'changed5'
	}
	else {
		update comment = 'changed6'
	}
}
else {
	if extra.text == 'test7' {
		update comment = 'changed7'
	}
	elif extra.text == 'test8' {
		update comment = 'changed8'
	}
	else {
		update comment = 'changed9'
	}
}
