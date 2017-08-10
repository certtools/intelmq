if ( source.abuse_contact == "abuse@example.com" || comment == "I am TRUE in OR clause" ) {
    modify source.ip = "10.9.8.7"
}
