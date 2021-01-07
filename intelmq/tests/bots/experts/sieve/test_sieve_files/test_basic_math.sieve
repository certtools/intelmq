if comment == 'add_force' {
    add! time.observation += '1 hour'
}

if comment == 'minus_force' {
    add! time.observation -= '1 hour'
}

if comment == 'minus_normal' {
    add time.observation -= '1 hour'
}

if comment == 'add_normal' {
    add time.observation += '1 hour'
}

if comment == 'add_update' {
    update time.observation += '1 hour'
}

if comment == 'minus_update' {
    update time.observation -= '1 hour'
}
