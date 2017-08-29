if comment == 'continue' {
}

if comment == 'keep' {
  keep
}

if comment == ['continue', 'keep'] {
  modify comment = 'changed'
}
