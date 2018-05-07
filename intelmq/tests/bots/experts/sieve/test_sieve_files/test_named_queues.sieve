if comment == "keep without path" {
    keep
}

if comment == "keep with path" {
    path "other-way"
    keep
}

if comment == "drop" {
    drop
}