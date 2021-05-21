if comment == 'continue' {
}

if comment == 'keep' {
  keep
}

if comment :in ['continue', 'keep'] {
  update comment = 'changed'
}
