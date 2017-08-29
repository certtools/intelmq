if comment == 'add force new field' {
    add! destination.ip = "150.50.50.10"
}
if comment == 'add force existing fields' {
    add! destination.ip = "200.10.9.7"
    add! source.ip = "10.9.8.7"
}
