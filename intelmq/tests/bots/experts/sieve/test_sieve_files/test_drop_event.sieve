if comment == 'drop' {
  drop
}

if source.ip == '127.0.0.1' {
  update comment = 'changed'
}
