if time.observation :before '1 week' {
	append extra.list 'before 1 week'
}

if time.observation :after '1 week' {
	append extra.list 'after 1 week'
}

if time.observation :before '2023-06-01' {
	append extra.list 'before 2023-06-01'
}

if time.observation :after '2023-06-01' {
	# when time is not set, '2023-06-01 00:01' resolves here
	append extra.list 'after 2023-06-01'
}

if time.observation :before '2023-06-01 15:00' {
	append extra.list 'before 2023-06-01 15:00'
}

if time.observation :after '2023-06-01 15:00' {
	append extra.list 'after 2023-06-01 15:00'
}

if extra.str == 'few-hours' && time.observation :after '10 h' {
	append extra.list 'after 10 h'
}
